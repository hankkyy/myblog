/**
 * Admin API — Read chat logs from CloudBase NoSQL via HTTP API
 * Password-protected with brute-force protection
 */

const CLOUDBASE_ENV = 'hanoi-d4gj8vd2q1e7a3dc0';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD;
if (!ADMIN_PASSWORD) {
  console.error('CRITICAL: ADMIN_PASSWORD environment variable is not configured. Admin API will reject all requests.');
}
const CLOUDBASE_API_KEY = process.env.CLOUDBASE_API_KEY || '';

const BASE_URL = `https://${CLOUDBASE_ENV}.api.tcloudbasegateway.com/v1/database/instances/(default)/databases/(default)`;

// --- Brute-force protection ---
// NOTE: This resets on serverless cold starts. For production-grade protection,
// consider using Vercel Edge Config or an external key-value store.
const attemptMap = new Map();
const MAX_ATTEMPTS = 5;
const LOCKOUT_BASE_MS = 30_000;
const CLEANUP_INTERVAL_MS = 300_000;

function getClientIp(req) {
  return req.headers['x-forwarded-for']?.split(',')[0]?.trim()
    || req.headers['x-real-ip']
    || req.socket?.remoteAddress
    || 'unknown';
}

function checkBruteForce(ip) {
  const now = Date.now();
  const entry = attemptMap.get(ip);
  if (!entry) return { blocked: false };

  const lockoutDuration = LOCKOUT_BASE_MS * Math.pow(2, Math.max(0, entry.failures - MAX_ATTEMPTS));
  const blockedUntil = entry.lastAttempt + lockoutDuration;

  if (now < blockedUntil) {
    const waitSec = Math.ceil((blockedUntil - now) / 1000);
    return { blocked: true, waitSec };
  }

  if (entry.failures >= MAX_ATTEMPTS) {
    attemptMap.set(ip, { failures: 0, lastAttempt: now });
  }
  return { blocked: false };
}

function recordFailedAttempt(ip) {
  const now = Date.now();
  const entry = attemptMap.get(ip) || { failures: 0, lastAttempt: now };
  entry.failures++;
  entry.lastAttempt = now;
  attemptMap.set(ip, entry);
}

function recordSuccess(ip) {
  attemptMap.delete(ip);
}

function cleanupStaleEntries() {
  const now = Date.now();
  for (const [ip, entry] of attemptMap) {
    if (now - entry.lastAttempt > CLEANUP_INTERVAL_MS) attemptMap.delete(ip);
  }
}

// Convert EJSON $date to ISO string for frontend compatibility
// Also filters out welcome/greeting messages from the admin view
function normalizeMessages(messages) {
  if (!Array.isArray(messages)) return [];
  return messages
    .filter(m => {
      if (m.role !== 'assistant') return true;
      const c = (m.content || '').trim();
      // Filter out AI welcome messages
      if (c.includes('数字分身') || c.includes("digital avatar")) return false;
      return true;
    })
    .map(m => ({
      role: m.role,
      content: m.content,
    }));
}

function parseEjsonDate(val) {
  if (val && typeof val === 'object' && val.$date) {
    const ms = val.$date.$numberLong
      ? Number(val.$date.$numberLong)
      : Number(val.$date);
    return new Date(ms).toISOString();
  }
  return val;
}

function normalizeLog(doc) {
  return {
    id: doc._id?.$oid || doc._id,
    sessionId: doc.sessionId,
    timestamp: parseEjsonDate(doc.timestamp),
    messages: normalizeMessages(doc.messages),
  };
}

async function cloudbaseRequest(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      'Authorization': `Bearer ${CLOUDBASE_API_KEY}`,
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`CloudBase API error ${res.status}: ${text}`);
  }
  return res.json();
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const clientIp = getClientIp(req);
  cleanupStaleEntries();

  const { blocked, waitSec } = checkBruteForce(clientIp);
  if (blocked) {
    return res.status(429).json({
      error: `Too many attempts. Please wait ${waitSec} seconds.`,
      retryAfter: waitSec,
    });
  }

  try {
    if (!ADMIN_PASSWORD) {
      return res.status(500).json({ error: 'Admin password not configured on server.' });
    }

    const { password, page = 1, pageSize = 20 } = req.body || {};

    if (!password || password !== ADMIN_PASSWORD) {
      recordFailedAttempt(clientIp);
      return res.status(401).json({ error: 'Unauthorized' });
    }

    recordSuccess(clientIp);

    // Count total documents
    const countResult = await cloudbaseRequest(
      `/collections/chat_logs/documents?count=true`
    );
    const total = countResult.total || 0;

    // Fetch logs with ordering and pagination
    const order = JSON.stringify([{ field: 'timestamp', direction: 'desc' }]);
    const offset = (page - 1) * pageSize;
    const queryResult = await cloudbaseRequest(
      `/collections/chat_logs/documents?order=${encodeURIComponent(order)}&limit=${pageSize}&offset=${offset}`
    );

    const logs = (queryResult.list || []).map(normalizeLog);

    return res.json({
      logs,
      total,
      page,
      pageSize,
      totalPages: Math.ceil(total / pageSize),
    });
  } catch (error) {
    console.error('Admin API error:', error.message);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

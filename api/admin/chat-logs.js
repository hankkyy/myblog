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

    const { password, page = 1, pageSize = 20, action, sessionId, sort = 'recent', filterRel } = req.body || {};

    if (!password || password !== ADMIN_PASSWORD) {
      recordFailedAttempt(clientIp);
      return res.status(401).json({ error: 'Unauthorized' });
    }

    recordSuccess(clientIp);

    // --- User Profiles mode ---
    if (action === 'profiles') {
      // Build order based on sort parameter
      let orderField;
      switch (sort) {
        case 'recent':    orderField = 'lastSeen'; break;
        case 'first':     orderField = 'timestamp'; break;
        case 'sessions':  orderField = 'sessionCount'; break;
        case 'messages':  orderField = 'totalMessages'; break;
        default:          orderField = 'lastSeen';
      }
      const order = JSON.stringify([{ field: orderField, direction: 'desc' }]);
      const offset = (page - 1) * pageSize;

      // Build filter for relationship type
      let filterStr = '';
      if (filterRel && filterRel !== 'all') {
        const filter = JSON.stringify({ 'profile.relationship_to_hank': filterRel });
        filterStr = `&filter=${encodeURIComponent(filter)}`;
      }

      const queryResult = await cloudbaseRequest(
        `/collections/user_profiles/documents?order=${encodeURIComponent(order)}&limit=${pageSize}&offset=${offset}${filterStr}`
      );

      const profiles = (queryResult.list || []).map(doc => ({
        id: doc._id?.$oid || doc._id,
        userId: doc.userId,
        sessionId: doc.lastSessionId || doc.sessionId,
        timestamp: parseEjsonDate(doc.lastSeen || doc.timestamp),
        firstSeen: parseEjsonDate(doc.timestamp),
        profile: doc.profile,
        sessionCount: doc.sessionCount || 1,
        totalMessages: doc.totalMessages || doc.messageCount || 0,
        history: doc.history || [],
      }));

      return res.json({
        profiles,
        page,
        pageSize,
        totalPages: Math.ceil((queryResult.total || 0) / pageSize),
      });
    }

    // --- Insights mode — aggregate stats across all profiles ---
    if (action === 'insights') {
      const queryResult = await cloudbaseRequest(
        `/collections/user_profiles/documents?order=${encodeURIComponent(JSON.stringify([{field:'lastSeen',direction:'desc'}]))}&limit=200`
      );

      const docs = queryResult.list || [];
      const profiles = docs.map(doc => doc.profile).filter(Boolean);

      // Relationship type distribution
      const relCounts = {};
      profiles.forEach(p => {
        const rel = (p && p.relationship_to_hank) || 'unknown';
        relCounts[rel] = (relCounts[rel] || 0) + 1;
      });

      // Top interests across all users
      const interestCounts = {};
      profiles.forEach(p => {
        (p && p.interests || []).forEach(i => {
          interestCounts[i] = (interestCounts[i] || 0) + 1;
        });
      });
      const topInterests = Object.entries(interestCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 20)
        .map(([name, count]) => ({ name, count }));

      // Session statistics
      const totalSessions = docs.reduce((sum, doc) => sum + (doc.sessionCount || 0), 0);
      const avgSessions = docs.length > 0 ? (totalSessions / docs.length).toFixed(1) : 0;

      return res.json({
        insights: {
          totalProfiles: queryResult.total || docs.length,
          totalSessions,
          avgSessions,
          relationshipDistribution: relCounts,
          topInterests,
        },
      });
    }

    // --- Chat Logs mode (default) ---
    // If sessionId is provided, return matching log (for profile → chat navigation)
    if (sessionId) {
      const filter = JSON.stringify({ sessionId });
      const queryResult = await cloudbaseRequest(
        `/collections/chat_logs/documents?filter=${encodeURIComponent(filter)}&limit=1`
      );
      const logs = (queryResult.list || []).map(normalizeLog);
      return res.json({
        logs,
        total: logs.length,
        page: 1,
        pageSize: 1,
        totalPages: logs.length > 0 ? 1 : 0,
      });
    }

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

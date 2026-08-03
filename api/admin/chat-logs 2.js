/**
 * Admin API — Read chat logs from CloudBase NoSQL
 * Password-protected with brute-force protection
 */

const cloudbase = require('@cloudbase/node-sdk');

const ENV_ID = 'hanoi-d4gj8vd2q1e7a3dc0';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'hankyky';

const app = cloudbase.init({ env: ENV_ID });
const db = app.database();

// --- Brute-force protection ---
const attemptMap = new Map();
const MAX_ATTEMPTS = 5;           // lock out after this many failures
const LOCKOUT_BASE_MS = 30_000;   // 30s base lockout
const CLEANUP_INTERVAL_MS = 300_000; // clean stale entries every 5 min

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

  // Exponential backoff: 30s, 60s, 120s, 240s...
  const lockoutDuration = LOCKOUT_BASE_MS * Math.pow(2, Math.max(0, entry.failures - MAX_ATTEMPTS));
  const blockedUntil = entry.lastAttempt + lockoutDuration;

  if (now < blockedUntil) {
    const waitSec = Math.ceil((blockedUntil - now) / 1000);
    return { blocked: true, waitSec };
  }

  // Lockout expired — reset if they've waited long enough
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

// Cleanup stale entries inside handler to avoid serverless timer issues
function cleanupStaleEntries() {
  const now = Date.now();
  for (const [ip, entry] of attemptMap) {
    if (now - entry.lastAttempt > CLEANUP_INTERVAL_MS) attemptMap.delete(ip);
  }
}


export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const clientIp = getClientIp(req);
  cleanupStaleEntries();

  // Check brute-force lockout
  const { blocked, waitSec } = checkBruteForce(clientIp);
  if (blocked) {
    return res.status(429).json({
      error: `Too many attempts. Please wait ${waitSec} seconds.`,
      retryAfter: waitSec,
    });
  }

  try {
    const { password, page = 1, pageSize = 20 } = req.body || {};

    if (!password || password !== ADMIN_PASSWORD) {
      recordFailedAttempt(clientIp);
      return res.status(401).json({ error: 'Unauthorized' });
    }

    recordSuccess(clientIp);

    // Count total
    const countResult = await db.collection('chat_logs').count();
    const total = countResult.total;

    // Fetch logs, newest first, paginated
    const result = await db.collection('chat_logs')
      .orderBy('timestamp', 'desc')
      .skip((page - 1) * pageSize)
      .limit(pageSize)
      .get();

    const logs = result.data.map(item => ({
      id: item._id,
      sessionId: item.sessionId,
      timestamp: item.timestamp,
      messages: item.messages,
    }));

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

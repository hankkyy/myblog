/**
 * Admin API — Read chat logs from CloudBase NoSQL via HTTP API
 * Password-protected with brute-force protection
 *
 * Optimizations applied (2026-08-06):
 * - New 'cleanup' action — delete chat logs older than N days
 * - Insights now includes topLocations and avgMessagesPerSession
 * - Profiles query now supports count=true for accurate pagination
 * - Cleanup uses batch delete (not one-by-one)
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
function normalizeMessages(messages) {
  if (!Array.isArray(messages)) return [];
  return messages
    .filter(m => {
      if (m.role !== 'assistant') return true;
      const c = (m.content || '').trim();
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

function parseEjsonNumber(val) {
  if (val && typeof val === 'object') {
    if (val.$numberInt) return Number(val.$numberInt);
    if (val.$numberLong) return Number(val.$numberLong);
    if (val.$numberDouble) return Number(val.$numberDouble);
  }
  // Salvage corrupted string values (e.g., "[object Object]111" from old bug)
  if (typeof val === 'string') {
    var n = Number(val);
    if (!isNaN(n)) return n;
    var match = val.match(/(\d+)$/);
    if (match) return Number(match[1]);
    return 0;
  }
  return Number(val) || 0;
}

function normalizeLog(doc) {
  return {
    id: doc._id?.$oid || doc._id,
    sessionId: doc.sessionId,
    userId: doc.userId || null,
    timestamp: parseEjsonDate(doc.timestamp),
    messages: normalizeMessages(doc.messages),
  };
}

async function cloudbaseRequest(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  const { notFoundFallback, ...fetchOptions } = options;
  const res = await fetch(url, {
    ...fetchOptions,
    headers: {
      'Authorization': `Bearer ${CLOUDBASE_API_KEY}`,
      'Content-Type': 'application/json',
      ...(fetchOptions.headers || {}),
    },
  });
  if (!res.ok) {
    if (notFoundFallback && res.status === 404) {
      return { list: [], total: 0 };
    }
    const text = await res.text();
    throw new Error(`CloudBase API error ${res.status}: ${text}`);
  }
  return res.json();
}

// Delete a single document by ID
async function cloudbaseDelete(collection, docId) {
  const url = `${BASE_URL}/collections/${collection}/documents/${docId}`;
  const res = await fetch(url, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${CLOUDBASE_API_KEY}`,
      'Content-Type': 'application/json',
    },
  });
  return res.ok;
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

    const {
      password, page = 1, pageSize = 20, action,
      sessionId, sort = 'recent', filterRel,
      olderThanDays, // for cleanup action
    } = req.body || {};

    if (!password || password !== ADMIN_PASSWORD) {
      recordFailedAttempt(clientIp);
      return res.status(401).json({ error: 'Unauthorized' });
    }

    recordSuccess(clientIp);

    // ===================================================================
    // CLEANUP — delete chat logs older than N days
    // ===================================================================
    if (action === 'cleanup') {
      const days = parseInt(olderThanDays) || 90; // default: 90 days
      if (days < 7) {
        return res.status(400).json({ error: 'Minimum retention is 7 days.' });
      }

      const cutoffDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString();

      // Fetch old documents (limit to prevent timeout)
      const queryResult = await cloudbaseRequest(
        `/collections/chat_logs/documents?limit=100&order=${encodeURIComponent(JSON.stringify([{ field: 'timestamp', direction: 'asc' }]))}`
      );

      const oldDocs = (queryResult.list || []).filter(doc => {
        const ts = parseEjsonDate(doc.timestamp);
        return ts && ts < cutoffDate;
      });

      if (oldDocs.length === 0) {
        return res.json({ cleaned: 0, message: 'No logs older than threshold found.' });
      }

      // Delete in parallel batches (CloudBase HTTP API deletes one at a time)
      let deleted = 0;
      const batchSize = 10;
      for (let i = 0; i < oldDocs.length; i += batchSize) {
        const batch = oldDocs.slice(i, i + batchSize);
        const results = await Promise.all(
          batch.map(doc => cloudbaseDelete('chat_logs', doc._id?.$oid || doc._id))
        );
        deleted += results.filter(Boolean).length;
      }

      return res.json({
        cleaned: deleted,
        cutoff: cutoffDate,
        message: `Deleted ${deleted} chat logs older than ${days} days.`,
      });
    }

    // ===================================================================
    // PROFILES — paginated, sortable, filterable
    // ===================================================================
    if (action === 'profiles') {
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

      let filterStr = '';
      if (filterRel && filterRel !== 'all') {
        const filter = JSON.stringify({ 'profile.relationship_to_hank': filterRel });
        filterStr = `&filter=${encodeURIComponent(filter)}`;
      }

      // Fetch count + data in parallel for accurate pagination
      const [countResult, queryResult] = await Promise.all([
        cloudbaseRequest(
          `/collections/user_profiles/documents?count=true${filterStr}`,
          { notFoundFallback: true }
        ),
        cloudbaseRequest(
          `/collections/user_profiles/documents?order=${encodeURIComponent(order)}&limit=${pageSize}&offset=${offset}${filterStr}`,
          { notFoundFallback: true }
        ),
      ]);

      const total = countResult.total || 0;

      const profiles = (queryResult.list || []).map(doc => ({
        id: doc._id?.$oid || doc._id,
        userId: doc.userId,
        sessionId: doc.lastSessionId || doc.sessionId,
        timestamp: parseEjsonDate(doc.lastSeen || doc.timestamp),
        firstSeen: parseEjsonDate(doc.timestamp),
        profile: doc.profile,
        sessionCount: parseEjsonNumber(doc.sessionCount) || 1,
        totalMessages: parseEjsonNumber(doc.totalMessages || doc.messageCount) || 0,
        history: doc.history || [],
      }));

      return res.json({
        profiles,
        page,
        pageSize,
        total,
        totalPages: Math.ceil(total / pageSize),
      });
    }

    // ===================================================================
    // INSIGHTS — aggregate stats across all profiles
    // OPTIMIZATION: uses count query + parallel fetching, adds more stats
    // ===================================================================
    if (action === 'insights') {
      // Fetch count + data in parallel
      const [countResult, queryResult] = await Promise.all([
        cloudbaseRequest(
          `/collections/user_profiles/documents?count=true`,
          { notFoundFallback: true }
        ),
        cloudbaseRequest(
          `/collections/user_profiles/documents?order=${encodeURIComponent(JSON.stringify([{field:'lastSeen',direction:'desc'}]))}&limit=200`,
          { notFoundFallback: true }
        ),
      ]);

      const docs = queryResult.list || [];
      const totalProfiles = countResult.total || docs.length;
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

      // Top locations
      const locCounts = {};
      profiles.forEach(p => {
        const loc = (p && p.location) || null;
        if (loc) locCounts[loc] = (locCounts[loc] || 0) + 1;
      });
      const topLocations = Object.entries(locCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([name, count]) => ({ name, count }));

      // Session statistics (parse EJSON numbers from CloudBase NoSQL)
      const totalSessions = docs.reduce((sum, doc) => sum + (parseEjsonNumber(doc.sessionCount) || 0), 0);
      const totalMessages = docs.reduce((sum, doc) => sum + (parseEjsonNumber(doc.totalMessages || doc.messageCount) || 0), 0);
      const avgSessions = docs.length > 0 ? (totalSessions / docs.length).toFixed(1) : 0;
      const avgMessagesPerSession = totalSessions > 0 ? (totalMessages / totalSessions).toFixed(1) : 0;

      return res.json({
        insights: {
          totalProfiles,
          totalSessions,
          totalMessages,
          avgSessions,
          avgMessagesPerSession,
          relationshipDistribution: relCounts,
          topInterests,
          topLocations,
        },
      });
    }

    // ===================================================================
    // CHAT LOGS — default mode (paginated)
    // ===================================================================
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

    // Fetch count + data in parallel
    const [countResult, queryResult] = await Promise.all([
      cloudbaseRequest(`/collections/chat_logs/documents?count=true`),
      cloudbaseRequest(
        `/collections/chat_logs/documents?order=${encodeURIComponent(JSON.stringify([{ field: 'timestamp', direction: 'desc' }]))}&limit=${pageSize}&offset=${(page - 1) * pageSize}`
      ),
    ]);

    const total = countResult.total || 0;
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

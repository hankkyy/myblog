// eBay Account Deletion Notification Endpoint
// Handles both endpoint verification (GET) and deletion notifications (POST)

const VERIFICATION_TOKEN = process.env.EBAY_ACCOUNT_DELETION_VERIFICATION_TOKEN;

export default async function handler(req, res) {
  // CORS headers for eBay
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Verify the token from query param or Authorization header
  const tokenFromQuery = req.query.token || req.query.verification_token;
  const authHeader = req.headers.authorization || '';
  const tokenFromHeader = authHeader.startsWith('Bearer ')
    ? authHeader.slice(7)
    : authHeader;

  const providedToken = tokenFromQuery || tokenFromHeader;

  if (!VERIFICATION_TOKEN) {
    return res.status(500).json({ error: 'Server not configured' });
  }

  if (providedToken !== VERIFICATION_TOKEN) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  // GET: Endpoint verification — return the challenge code
  if (req.method === 'GET') {
    const challengeCode = req.query.challenge_code || req.query.challengeCode || '';
    return res.status(200).json({ challengeResponse: challengeCode });
  }

  // POST: Account deletion notification
  if (req.method === 'POST') {
    // Log the deletion notification (you can extend this)
    console.log('eBay account deletion notification received:', JSON.stringify(req.body));
    return res.status(200).json({ status: 'acknowledged' });
  }

  return res.status(405).json({ error: 'Method not allowed' });
}

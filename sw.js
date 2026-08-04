// Service Worker for Hank's Blog — offline support & PWA install
const CACHE = 'hankblog-v2';
const MAX_CACHE_ITEMS = 200;
const STATIC_ASSETS = [
  '/',
  '/css/style.css',
  '/favicon.png',
  '/icon-192x192.png',
  '/icon-512x512.png',
  '/apple-touch-icon.png',
  '/manifest.json',
];

// Install: pre-cache static assets
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: network-first for HTML, cache-first for static assets
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);

  // Only handle same-origin GET requests
  if (url.origin !== self.location.origin || e.request.method !== 'GET') return;

  // Skip API/chat requests — always go to network
  if (url.pathname.startsWith('/api/')) return;

  const isPage = e.request.mode === 'navigate' || url.pathname.endsWith('/') || !url.pathname.includes('.');

  if (isPage) {
    // Network-first for pages: try network, fall back to cache, then offline page
    e.respondWith(
      fetch(e.request)
        .then((res) => {
          const clone = res.clone();
          caches.open(CACHE).then((cache) => {
            cache.put(e.request, clone);
            trimCache(cache);
          });
          return res;
        })
        .catch(() =>
          caches.match(e.request).then((cached) => cached || caches.match('/'))
        )
    );
  } else {
    // Cache-first for static assets (CSS, JS, images, fonts)
    e.respondWith(
      caches.match(e.request).then((cached) => {
        const fetched = fetch(e.request).then((res) => {
          const clone = res.clone();
          caches.open(CACHE).then((cache) => {
            cache.put(e.request, clone);
            trimCache(cache);
          });
          return res;
        });
        return cached || fetched;
      })
    );
  }
});

// Trim oldest entries when cache exceeds limit
async function trimCache(cache) {
  const keys = await cache.keys();
  if (keys.length > MAX_CACHE_ITEMS) {
    const toDelete = keys.slice(0, keys.length - MAX_CACHE_ITEMS + 50);
    for (const req of toDelete) {
      await cache.delete(req);
    }
  }
}

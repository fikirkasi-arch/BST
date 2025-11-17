// Service Worker - BST Eğitim Portalı Offline Desteği
const CACHE_NAME = 'bst-cache-v1';
const OFFLINE_PAGE = '/offline.html';

// Önbelleğe alınacak dosyalar
const CACHE_FILES = [
    '/',
    '/index.html',
    '/scripts/storage.js',
    '/scripts/analytics.js',
    '/scripts/badge-system.js',
    '/scripts/search.js',
    '/scripts/dark-mode.js',
    '/scripts/daily-challenges.js',
    '/scripts/notification.js',
    '/scripts/recent-items.js',
    '/scripts/daily-goals.js',
    '/scripts/progress-tracker.js'
];

// Service Worker yüklendiğinde
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Yükleniyor...');

    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[Service Worker] Dosyalar önbelleğe alınıyor');
            return cache.addAll(CACHE_FILES);
        })
    );

    // Yeni service worker'ı hemen aktifleştir
    self.skipWaiting();
});

// Service Worker aktif olduğunda
self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Aktif');

    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[Service Worker] Eski cache siliniyor:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );

    // Tüm istemcileri kontrol et
    return self.clients.claim();
});

// Fetch olayları - Network-first stratejisi
self.addEventListener('fetch', (event) => {
    // Sadece HTTP/HTTPS istekleri için
    if (!event.request.url.startsWith('http')) {
        return;
    }

    event.respondWith(
        fetch(event.request)
            .then((response) => {
                // Başarılı yanıt - cache'e kopyala
                const responseClone = response.clone();

                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(event.request, responseClone);
                });

                return response;
            })
            .catch(() => {
                // Network başarısız - cache'den dön
                return caches.match(event.request).then((cachedResponse) => {
                    if (cachedResponse) {
                        return cachedResponse;
                    }

                    // Offline sayfasını göster
                    if (event.request.mode === 'navigate') {
                        return caches.match(OFFLINE_PAGE);
                    }
                });
            })
    );
});

// Sync event - background sync
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-progress') {
        event.waitUntil(syncProgressData());
    }
});

// İlerleme verilerini senkronize et
async function syncProgressData() {
    console.log('[Service Worker] İlerleme verileri senkronize ediliyor...');
    // Burada API'ye ilerleme verisi gönderimi yapılabilir
}

// Push notification desteği (gelecek için hazır)
self.addEventListener('push', (event) => {
    const data = event.data ? event.data.json() : {};

    const options = {
        body: data.body || 'Yeni bildirim',
        icon: '/icon-192.png',
        badge: '/badge-72.png',
        vibrate: [200, 100, 200],
        data: {
            url: data.url || '/'
        }
    };

    event.waitUntil(
        self.registration.showNotification(data.title || 'BST Eğitim', options)
    );
});

// Bildirime tıklanınca
self.addEventListener('notificationclick', (event) => {
    event.notification.close();

    event.waitUntil(
        clients.openWindow(event.notification.data.url)
    );
});

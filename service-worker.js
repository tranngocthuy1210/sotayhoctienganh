/* Service worker cho PWA "Sổ tay học tiếng Anh"
   - Cache app để chạy offline
   - Trang + file mã/dữ liệu (.js, .html): ƯU TIÊN MẠNG — online luôn lấy bản mới,
     mất mạng mới dùng bản đã lưu. (Trước đây .js dùng cache-first nên người dùng
     hay thấy bản cũ sau khi cập nhật — đã sửa.)
   - Ảnh / manifest: dùng bản lưu ngay + âm thầm cập nhật (nhanh, ít đổi)
   - Bỏ qua yêu cầu khác nguồn (vd CDN Supabase, audio Tatoeba) để không chặn */
var CACHE = "sotay-v10";
var CORE = [
  "./", "./index.html", "./data-vocab.js", "./data-vocab-plus.js", "./data-vocab-oxford.js", "./data-dictation-tatoeba.js", "./data-sentence-vn.js", "./config.js", "./manifest.json",
  "./icon-192.png", "./icon-512.png", "./icon-maskable-512.png", "./apple-touch-icon.png"
];

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      return c.addAll(CORE).catch(function () {});
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) { if (k !== CACHE) return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;
  var url;
  try { url = new URL(req.url); } catch (err) { return; }
  if (url.origin !== self.location.origin) return;

  var path = url.pathname;
  // Trang + mã + dữ liệu: ưu tiên mạng để luôn có bản mới nhất
  var freshFirst = req.mode === "navigate" || path.endsWith("/") || /\.(js|html|json)$/.test(path);

  if (freshFirst) {
    e.respondWith(
      fetch(req).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
        return res;
      }).catch(function () {
        return caches.match(req).then(function (m) { return m || caches.match("./index.html"); });
      })
    );
    return;
  }

  // Ảnh / tài nguyên tĩnh khác: dùng bản lưu ngay, cập nhật ngầm
  e.respondWith(
    caches.match(req).then(function (cached) {
      var net = fetch(req).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
        return res;
      }).catch(function () { return cached; });
      return cached || net;
    })
  );
});

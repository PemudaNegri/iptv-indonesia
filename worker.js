// ==============================================================================
// CLOUDFLARE WORKER: SISTEM TOKEN & ANTI-CACHE (MULTI-PLAYLIST)
// Repository: https://github.com/PemudaNegri/iptv-indonesia
// ==============================================================================

// 1. DAFTAR PELANGGAN & TANGGAL KADALUARSA (Format: YYYY-MM-DD)
const USERS = {
  "demo": "2026-12-31",        // Akun demo sampai akhir tahun
  "budi": "2026-09-25",        // Pelanggan Pak Budi (aktif s/d 25 Sep 2026)
  "andi": "2026-09-30",        // Pelanggan Mas Andi (aktif s/d 30 Sep 2026)
  "stb01": "2026-09-25",       // STB Unit 01
};

// 2. URL SUMBER MASTER DARI GITHUB ANDA
const GITHUB_LIVE_URL = "https://raw.githubusercontent.com/PemudaNegri/iptv-indonesia/main/live.m3u";
const GITHUB_VOD_URL = "https://raw.githubusercontent.com/PemudaNegri/iptv-indonesia/main/vod.m3u";
const GITHUB_ALL_URL = "https://raw.githubusercontent.com/PemudaNegri/iptv-indonesia/main/playlist.m3u";

// 3. PESAN JIKA PELANGGAN EXPIRED / BELUM BAYAR
const EXPIRED_M3U = `#EXTM3U
#EXTINF:-1 tvg-logo="https://i.imgur.com/8QG4kQ6.png" group-title="INFORMASI PENTING",⚠️ MASA AKTIF ANDA SUDAH HABIS
https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4
#EXTINF:-1 tvg-logo="https://i.imgur.com/8QG4kQ6.png" group-title="INFORMASI PENTING",Silakan Hubungi WhatsApp Admin Untuk Perpanjang
https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4
`;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const user = url.searchParams.get("user") || url.searchParams.get("id");
    const type = (url.searchParams.get("type") || "all").toLowerCase();

    // 1. Cek apakah user terdaftar
    if (!user || !USERS[user]) {
      return new Response(
        "#EXTM3U\n#EXTINF:-1 group-title=\"ERROR\",❌ AKUN TIDAK TERDAFTAR / SALAH LINK\nhttps://example.com/error.mp4", 
        { headers: { "Content-Type": "audio/x-mpegurl; charset=utf-8" } }
      );
    }

    // 2. Cek tanggal kadaluarsa pelanggan
    const expiryDateStr = USERS[user];
    const expiryDate = new Date(expiryDateStr + "T23:59:59Z");
    const now = new Date();

    // Jika sudah lewat tanggal kadaluarsa (Expired)
    if (now > expiryDate) {
      return new Response(EXPIRED_M3U, {
        headers: { "Content-Type": "audio/x-mpegurl; charset=utf-8" }
      });
    }

    // 3. Tentukan Playlist yang diminta
    let targetUrl = GITHUB_ALL_URL;
    if (type === "live" || type === "tv") {
      targetUrl = GITHUB_LIVE_URL;
    } else if (type === "vod" || type === "film" || type === "movie") {
      targetUrl = GITHUB_VOD_URL;
    }

    // 4. TRIK ANTI-CACHE: Tambahkan timestamp acak agar GitHub tidak mengirim file cache lama
    const cacheBusterUrl = targetUrl + "?t=" + Date.now();

    const response = await fetch(cacheBusterUrl, {
      headers: { 
        "User-Agent": "Mozilla/5.0",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache"
      }
    });

    const m3uContent = await response.text();

    // 5. Kirim respon dengan header NO-CACHE agar OTT Navigator selalu membaca data paling baru
    return new Response(m3uContent, {
      headers: {
        "Content-Type": "audio/x-mpegurl; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0"
      }
    });
  }
};

# 📺 Multi-Playlist IPTV & Sistem Langganan Bulanan

Repository resmi playlist TV Indonesia dengan sistem **Multi-Playlist** (Pemisahan TV Live & VOD Bioskop) serta dilengkapi script **Cloudflare Worker** untuk sistem langganan bulanan / expired otomatis.

---

## 📂 Daftar File Playlist (Multi-Playlist):

### 1. 📡 Playlist TV Live (`live.m3u`)
* **Khusus:** 214 Channel Siaran Langsung (TV Nasional, TV Daerah, Sports, Bioskop TV, Kids).
* **Karakteristik:** **Super Ringan & Cepat**, sangat cocok untuk STB RAM 1GB / nonton harian.
* **Link Raw:**
  ```text
  https://raw.githubusercontent.com/PemudaNegri/iptv-indonesia/main/live.m3u
  ```

### 2. 🍿 Playlist Bioskop VOD (`vod.m3u`)
* **Khusus:** Koleksi Film Bioskop Indonesia & Box Office.
* **Link Raw:**
  ```text
  https://raw.githubusercontent.com/PemudaNegri/iptv-indonesia/main/vod.m3u
  ```

### 3. 📦 Master Playlist Lengkap (`playlist.m3u`)
* **Khusus:** Menggabungkan TV Live + VOD dalam satu file.
* **Link Raw:**
  ```text
  https://raw.githubusercontent.com/PemudaNegri/iptv-indonesia/main/playlist.m3u
  ```

---

## ⚙️ Sistem Langganan Bulanan (Cloudflare Worker)

Gunakan file **`worker.js`** untuk memasang sistem token & expired date di Cloudflare Workers gratis:

1. Buka dashboard [Cloudflare Workers](https://dash.cloudflare.com) $\rightarrow$ Create Worker.
2. Salin isi kode dari file **`worker.js`** $\rightarrow$ Klik Save and Deploy.
3. Link untuk pelanggan Anda menjadi:
   * **Paket TV Live:** `https://nama-worker.workers.dev/?user=budi&type=live`
   * **Paket VOD Film:** `https://nama-worker.workers.dev/?user=budi&type=vod`
   * **Paket Lengkap:** `https://nama-worker.workers.dev/?user=budi`

# 📺 Playlist IPTV Channel Indonesia (Auto Update)

Repository resmi playlist TV Indonesia yang sudah disaring rapi, lengkap dengan kategori, logo jernih, jadwal TV (EPG), dan sistem auto-update otomatis via GitHub Actions.

---

## 🔗 Link Playlist untuk STB & IPTV Player

Gunakan **Link Raw** di bawah ini untuk dimasukkan ke aplikasi player (TiviMate, OTT Navigator, IPTV Smarters, VLC):

### 1. Link Raw Asli (GitHub):
```text
https://raw.githubusercontent.com/PemudaNegri/iptv-indonesia/main/playlist.m3u
```

### 2. Link Pendek (Rekomendasi untuk Remote STB):
> *Buat link pendek kustom Anda sendiri di [TinyURL.com](https://tinyurl.com) agar mudah diketik dengan remote:*
> Contoh: `tinyurl.com/tv-pemudanegri`

---

## 📂 Struktur File Repository

* **`playlist.m3u`**: Master playlist TV Indonesia lengkap (Nasional, Berita, Olahraga, Edukasi, Religi, Daerah).
* **`updater.py`**: Script Python untuk memvalidasi dan memperbarui playlist.
* **`.github/workflows/update.yml`**: Robot GitHub Actions yang otomatis berjalan setiap 6 jam untuk memperbarui file `playlist.m3u`.

---

## 🚀 Cara Memasang di STB Pelanggan

1. Buka aplikasi **TiviMate** atau **OTT Navigator** di STB.
2. Masuk ke **Settings** $\rightarrow$ **Playlists** $\rightarrow$ **Add Playlist**.
3. Pilih **M3U Playlist URL** dan masukkan link:
   `https://raw.githubusercontent.com/PemudaNegri/iptv-indonesia/main/playlist.m3u` (atau link TinyURL Anda).
4. Aktifkan opsi **"Reload on app start"** agar playlist selalu otomatis sinkron setiap TV dinyalakan.

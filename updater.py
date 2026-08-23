import urllib.request
import re
import os
from datetime import datetime

# ==========================================
# AUTO UPDATER & GENERATOR M3U INDONESIA
# Repository: https://github.com/PemudaNegri/iptv-indonesia
# ==========================================

M3U_FILE = "playlist.m3u"

def check_link(url, timeout=5):
    """Mengecek apakah stream link masih aktif (status code 200/302)"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status in [200, 301, 302]
    except Exception:
        return False

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Memulai pengecekan & update playlist...")
    
    if not os.path.exists(M3U_FILE):
        print(f"Error: {M3U_FILE} tidak ditemukan!")
        return

    with open(M3U_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Hitung jumlah channel yang ada
    channels = re.findall(r"#EXTINF:-1.*?,(.*?)\n", content)
    print(f"Total Channel Terdaftar: {len(channels)}")

    # Update timestamp header
    header_comment = f"# Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
    if "# Last Updated:" in content:
        content = re.sub(r"# Last Updated:.*?\n", header_comment, content)
    else:
        content = content.replace("#EXTM3U", f"#EXTM3U\n{header_comment}")

    with open(M3U_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print("Berhasil memperbarui playlist.m3u!")

if __name__ == "__main__":
    main()

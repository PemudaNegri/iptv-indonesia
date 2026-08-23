import urllib.request
import re
import concurrent.futures
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

M3U_PATH = r"C:\Users\NIRVANA\.gemini\antigravity\scratch\iptv-indonesia\playlist.m3u"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*'
}

def test_url(item):
    extinf, tags, url = item
    clean_url = url.split('|')[0].strip()
    
    # Deteksi VOD / file unduhan (pixeldrain, dropbox, mp4) selalu anggap aktif jika bisa di-ping
    try:
        req = urllib.request.Request(clean_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=4) as response:
            if response.status in [200, 206, 301, 302]:
                return item, True
    except Exception:
        pass
        
    return item, False

def run_health_check():
    print("[+] Membaca file playlist.m3u...")
    with open(M3U_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [l.strip() for l in f if l.strip()]

    items = []
    current_extinf = ""
    current_tags = []

    for line in lines:
        if line.startswith('#EXTM3U'):
            continue
        if line.startswith('#EXTINF:'):
            current_extinf = line
            current_tags = []
        elif line.startswith('#EXT') or line.startswith('#KODI'):
            current_tags.append(line)
        elif line.startswith('http'):
            if current_extinf:
                items.append((current_extinf, current_tags, line))
                current_extinf = ""
                current_tags = []

    print(f"[+] Memeriksa {len(items)} channel secara live (50 threads)...")

    working_items = []
    category_counts = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(test_url, items)
        for item, is_active in results:
            name = item[0].split(',')[-1]
            # Cari nama kategori
            g_match = re.search(r'group-title="(.*?)"', item[0])
            grp = g_match.group(1) if g_match else "Lainnya"
            
            if is_active:
                print(f" [V] AKTIF: [{grp}] {name}")
                working_items.append(item)
                category_counts[grp] = category_counts.get(grp, 0) + 1
            else:
                print(f" [X] DIBUANG: [{grp}] {name}")

    print("\n--- HASIL CHANNEL AKTIF PER KATEGORI ---")
    for cat, count in category_counts.items():
        print(f"* {cat}: {count} channel aktif")

    print(f"\n[+] Total channel yang aktif: {len(working_items)}/{len(items)}")

    # Tulis ulang playlist.m3u hanya dengan channel aktif
    clean_playlist = [
        '#EXTM3U url-tvg="https://iptv-org.github.io/epg/guides/id/useetv.com.epg.xml"\n'
    ]
    for extinf, tags, url in working_items:
        clean_playlist.append(extinf)
        for t in tags:
            clean_playlist.append(t)
        clean_playlist.append(url)

    with open(M3U_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(clean_playlist))

    print(f"[V] Sukses! File {M3U_PATH} telah diperbarui hanya dengan channel yang 100% hidup.")

if __name__ == '__main__':
    run_health_check()

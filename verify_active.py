import urllib.request
import re
import concurrent.futures
import sys

# Atur output agar aman dari masalah encoding di Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SOURCE_FILE = "playlist.m3u"
OUTPUT_FILE = "playlist.m3u"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*'
}

def test_stream(channel):
    extinf, url = channel
    clean_url = url.split('|')[0].strip()
    
    req_headers = HEADERS.copy()
    if 'http-referrer=' in extinf:
        ref = re.search(r'http-referrer="(.*?)"', extinf)
        if ref:
            req_headers['Referer'] = ref.group(1)

    try:
        req = urllib.request.Request(clean_url, headers=req_headers)
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status in [200, 301, 302]:
                return channel, True
    except Exception:
        pass
        
    return channel, False

def filter_only_working():
    print("[+] Membaca daftar channel...")
    with open(SOURCE_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [l.strip() for l in f if l.strip()]

    channels = []
    current_extinf = None
    
    for line in lines:
        if line.startswith('#EXTINF:'):
            current_extinf = line
        elif line.startswith('http'):
            if current_extinf:
                channels.append((current_extinf, line))
                current_extinf = None

    print(f"[+] Memeriksa {len(channels)} channel secara live...")
    
    working_channels = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        results = executor.map(test_stream, channels)
        for ch, is_active in results:
            name = ch[0].split(',')[-1]
            if is_active:
                print(f"[AKTIF] {name}")
                working_channels.append(ch)
            else:
                print(f"[DIBUANG] {name}")

    print(f"\n[+] Hasil: {len(working_channels)} channel 100% AKTIF & DAPAT DIAKSES.")

    # Buat ulang playlist hanya berisi channel yang hidup
    new_playlist = [
        '#EXTM3U url-tvg="https://iptv-org.github.io/epg/guides/id/useetv.com.epg.xml"\n'
    ]
    for extinf, url in working_channels:
        if '|' not in url:
            url_with_header = f"{url}|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        else:
            url_with_header = url
        new_playlist.append(extinf)
        new_playlist.append(url_with_header)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_playlist))

    print(f"[V] Berhasil memperbarui {OUTPUT_FILE} hanya dengan channel aktif!")

if __name__ == '__main__':
    filter_only_working()

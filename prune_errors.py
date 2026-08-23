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

def check_stream_block(block):
    """Menguji apakah siaran di dalam blok benar-benar aktif dan tidak error"""
    url = ""
    req_headers = HEADERS.copy()
    
    for line in block:
        if line.startswith('http://') or line.startswith('https://'):
            url = line.split('|')[0].strip()
        elif 'http-user-agent=' in line:
            ua = re.search(r'http-user-agent=(.*)', line)
            if ua:
                req_headers['User-Agent'] = ua.group(1).strip()
        elif 'http-referrer=' in line:
            ref = re.search(r'http-referrer=(.*)', line)
            if ref:
                req_headers['Referer'] = ref.group(1).strip()

    if not url:
        return block, False

    try:
        req = urllib.request.Request(url, headers=req_headers)
        with urllib.request.urlopen(req, timeout=4) as response:
            if response.status in [200, 206, 301, 302]:
                return block, True
    except Exception:
        pass
        
    return block, False

def remove_error_channels():
    print("[+] Membaca playlist.m3u...")
    with open(M3U_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [l.strip() for l in f if l.strip()]

    blocks = []
    current_block = []

    for line in lines:
        if line.startswith('#EXTM3U'):
            continue
        current_block.append(line)
        if line.startswith('http://') or line.startswith('https://'):
            blocks.append(current_block)
            current_block = []

    print(f"[+] Memeriksa {len(blocks)} channel secara live...")

    working_blocks = []
    category_summary = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(check_stream_block, blocks)
        for block, is_working in results:
            # Ambil nama channel dan group
            extinf_line = next((l for l in block if l.startswith('#EXTINF:')), "")
            name = extinf_line.split(',')[-1] if extinf_line else "Unknown"
            g_match = re.search(r'group-title="(.*?)"', extinf_line)
            grp = g_match.group(1) if g_match else "Lainnya"

            if is_working:
                print(f" [V] AKTIF: [{grp}] {name}")
                working_blocks.append(block)
                category_summary[grp] = category_summary.get(grp, 0) + 1
            else:
                print(f" [X] HAPUS (ERROR): [{grp}] {name}")

    print("\n--- HASIL CHANNEL AKTIF & BEBAS ERROR ---")
    for grp, count in category_summary.items():
        print(f"* {grp}: {count} channel")

    print(f"\n[+] Total siaran sehat yang dipertahankan: {len(working_blocks)}/{len(blocks)}")

    # Buat ulang playlist.m3u
    clean_content = [
        '#EXTM3U url-tvg="https://iptv-org.github.io/epg/guides/id/useetv.com.epg.xml"\n'
    ]
    for block in working_blocks:
        clean_content.extend(block)

    with open(M3U_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(clean_content))

    print(f"[V] Berhasil! File {M3U_PATH} sekarang 100% bersih dari siaran error.")

if __name__ == '__main__':
    remove_error_channels()

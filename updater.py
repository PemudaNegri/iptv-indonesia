import urllib.request
import re
import os

# ==============================================================================
# SCRIPT AUTO-UPDATER KHUSUS FULL CHANNEL INDONESIA
# Repository: https://github.com/PemudaNegri/iptv-indonesia
# ==============================================================================

SOURCE_URL = "https://iptv-org.github.io/iptv/countries/id.m3u"
OUTPUT_FILE = "playlist.m3u"

def update_indonesia_only():
    print(f"[+] Mengunduh data siaran murni Indonesia dari {SOURCE_URL}...")
    
    req = urllib.request.Request(
        SOURCE_URL, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        raw_text = response.read().decode('utf-8', errors='ignore')

    lines = raw_text.split('\n')
    master_playlist = [
        '#EXTM3U url-tvg="https://iptv-org.github.io/epg/guides/id/useetv.com.epg.xml"\n'
    ]

    current_extinf = None
    total_channels = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#EXTM3U'):
            continue

        if line.startswith('#EXTINF:'):
            # Pengelompokan kategori rapi bahasa Indonesia
            if any(k in line.lower() for k in ['relig', 'islam', 'dakwah', 'aliman', 'quran']):
                extinf_clean = re.sub(r'group-title=".*?"', 'group-title="Religi dan Dakwah"', line)
            elif any(k in line.lower() for k in ['news', 'berita', 'antara', 'cnn', 'cnbc']):
                extinf_clean = re.sub(r'group-title=".*?"', 'group-title="Berita dan Informasi"', line)
            elif any(k in line.lower() for k in ['sport', 'olahraga']):
                extinf_clean = re.sub(r'group-title=".*?"', 'group-title="Olahraga"', line)
            elif any(k in line.lower() for k in ['music', 'musik', 'dangdut']):
                extinf_clean = re.sub(r'group-title=".*?"', 'group-title="Musik dan Budaya"', line)
            else:
                extinf_clean = re.sub(r'group-title=".*?"', 'group-title="TV Nasional dan Daerah"', line)
            current_extinf = extinf_clean

        elif line.startswith('#EXTVLCOPT') or line.startswith('#EXTHTTP'):
            master_playlist.append(line)

        elif line.startswith('http'):
            if current_extinf:
                master_playlist.append(current_extinf)
                current_extinf = None
            master_playlist.append(line)
            total_channels += 1

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(master_playlist))

    print(f"[V] Berhasil! Playlist murni Indonesia ({total_channels} channel) disimpan ke {OUTPUT_FILE}")

if __name__ == '__main__':
    update_indonesia_only()

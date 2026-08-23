import urllib.request
import re
import os

# ==============================================================================
# SCRIPT MULTI-SOURCE IPTV MERGER & AGGREGATOR
# Menggabungkan channel dari berbagai sumber database menjadi 1 playlist rapi
# ==============================================================================

# 1. Masukkan semua link database / sumber playlist yang Anda miliki di sini:
SOURCES = [
    # Sumber 1: Database Publik Indonesia
    "https://iptv-org.github.io/iptv/countries/id.m3u",
    
    # Sumber 2: Database Kategori Berita Internasional / Global
    "https://iptv-org.github.io/iptv/categories/news.m3u",
    
    # Sumber 3: Database Kategori Musik Dunia
    "https://iptv-org.github.io/iptv/categories/music.m3u",
    
    # Sumber 4: (Contoh jika punya link sumber lain / GitHub orang lain)
    # "https://raw.githubusercontent.com/user_lain/repo/main/tv.m3u",
    
    # Sumber 5: (Contoh sumber kelima)
    # "https://example.com/playlist_khusus.m3u"
]

OUTPUT_FILE = r"C:\Users\NIRVANA\.gemini\antigravity\scratch\iptv-indonesia\playlist.m3u"

def fetch_m3u(url):
    """Mengunduh isi file M3U dari internet"""
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"[-] Gagal mengambil dari {url}: {e}")
        return ""

def parse_and_merge():
    print("[+] Memulai penggabungan multi-sumber...")
    
    seen_channels = set()  # Untuk mencegah duplikasi channel yang sama
    master_playlist = [
        '#EXTM3U url-tvg="https://iptv-org.github.io/epg/guides/id/useetv.com.epg.xml"\n'
    ]
    
    total_added = 0

    for idx, source_url in enumerate(SOURCES, start=1):
        if not source_url.startswith("http"):
            continue
            
        print(f"[+] Mengambil data dari Sumber {idx}: {source_url}...")
        raw_text = fetch_m3u(source_url)
        if not raw_text:
            continue

        lines = raw_text.split('\n')
        current_extinf = None
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#EXTM3U'):
                continue
                
            if line.startswith('#EXTINF:'):
                current_extinf = line
            elif line.startswith('http'):
                if current_extinf:
                    # Ambil nama channel untuk cek duplikat
                    channel_name = current_extinf.split(',')[-1].strip().lower()
                    
                    # Jika channel belum ada di daftar, tambahkan ke master playlist
                    if channel_name not in seen_channels:
                        seen_channels.add(channel_name)
                        
                        # Rapikan kategori
                        if any(k in current_extinf.lower() for k in ['relig', 'islam', 'dakwah']):
                            extinf_clean = re.sub(r'group-title=".*?"', 'group-title="Religi dan Dakwah"', current_extinf)
                        elif any(k in current_extinf.lower() for k in ['news', 'berita']):
                            extinf_clean = re.sub(r'group-title=".*?"', 'group-title="Berita dan Informasi"', current_extinf)
                        elif any(k in current_extinf.lower() for k in ['sport', 'olahraga']):
                            extinf_clean = re.sub(r'group-title=".*?"', 'group-title="Olahraga"', current_extinf)
                        elif any(k in current_extinf.lower() for k in ['music', 'musik']):
                            extinf_clean = re.sub(r'group-title=".*?"', 'group-title="Musik"', current_extinf)
                        else:
                            extinf_clean = re.sub(r'group-title=".*?"', 'group-title="TV Nasional dan Daerah"', current_extinf)

                        master_playlist.append(extinf_clean)
                        master_playlist.append(line)
                        total_added += 1
                        
                    current_extinf = None

    # Simpan ke file playlist.m3u
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(master_playlist))
        
    print(f"\n[V] SUKSES! Total {total_added} channel unik berhasil digabungkan ke {OUTPUT_FILE}")

if __name__ == '__main__':
    parse_and_merge()

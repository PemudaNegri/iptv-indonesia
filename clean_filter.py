import urllib.request
import re

def process_iptv_org():
    url = 'https://iptv-org.github.io/iptv/countries/id.m3u'
    print(f"Mengunduh data dari {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as r:
        raw_data = r.read().decode('utf-8')

    lines = raw_data.split('\n')
    clean_m3u = ['#EXTM3U url-tvg="https://iptv-org.github.io/epg/guides/id/useetv.com.epg.xml"\n']

    current_extinf = ''
    total_channels = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#EXTM3U'):
            continue
        elif line.startswith('#EXTINF:'):
            # Format kategori agar rapi dan mudah dibaca di STB
            if 'Religious' in line or 'Religi' in line:
                line = re.sub(r'group-title=".*?"', 'group-title="Religi dan Dakwah"', line)
            elif 'News' in line or 'Berita' in line:
                line = re.sub(r'group-title=".*?"', 'group-title="Berita dan Informasi"', line)
            elif 'Sports' in line or 'Olahraga' in line:
                line = re.sub(r'group-title=".*?"', 'group-title="Olahraga"', line)
            elif 'Music' in line or 'Musik' in line:
                line = re.sub(r'group-title=".*?"', 'group-title="Musik dan Hiburan"', line)
            else:
                line = re.sub(r'group-title=".*?"', 'group-title="TV Nasional dan Daerah"', line)
            current_extinf = line
        elif line.startswith('#EXTVLCOPT') or line.startswith('#EXTHTTP'):
            clean_m3u.append(line)
        elif line.startswith('http'):
            if current_extinf:
                clean_m3u.append(current_extinf)
                current_extinf = ''
            clean_m3u.append(line)
            total_channels += 1

    output_path = r'C:\Users\NIRVANA\.gemini\antigravity\scratch\iptv-indonesia\playlist.m3u'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(clean_m3u))

    print(f"Sukses! Berhasil memfilter {total_channels} channel Indonesia dan disimpan ke {output_path}")

if __name__ == '__main__':
    process_iptv_org()

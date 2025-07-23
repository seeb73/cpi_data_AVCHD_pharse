import os
import struct

def pts_to_timecode(pts, fps=50):
    total_seconds = pts / 90000
    hh = int(total_seconds // 3600)
    mm = int((total_seconds % 3600) // 60)
    ss = int(total_seconds % 60)
    ff = int((total_seconds - int(total_seconds)) * fps)
    return f"{hh:02}:{mm:02}:{ss:02}:{ff:02}"

def main(directory):
    offset = 0xB10
    for root, dirs, files in os.walk(directory):
        for file in sorted(files):
            if file.lower().endswith('.cpi'):
                path = os.path.join(root, file)
                with open(path, 'rb') as f:
                    f.seek(offset)
                    data = f.read(8)
                if len(data) < 4:
                    print(f"{file}: brak danych na offsetcie 0xB10")
                    continue
                pts = struct.unpack('>I', data[:4])[0]  # big-endian
                tc = pts_to_timecode(pts, fps=50)
                print(f"{file}: PTS={pts}  Timecode={tc}  HEX={' '.join(f'{b:02x}' for b in data[:4])}")

if __name__ == '__main__':
    katalog = input('Podaj ścieżkę do katalogu z plikami CPI: ')
    main(katalog)

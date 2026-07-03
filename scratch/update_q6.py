import codecs
import re

file_path = r"c:\Users\Fuad Nugraha\Documents\GitHub\Machine-Learning-TA\Anomaly Detection BMKG\jawaban_laporan.txt"

with codecs.open(file_path, "r", "utf-8") as f:
    content = f.read()

replacement = """6. Apakah semua atribut digunakan atau hanya sebagian? Mengapa?
Hanya sebagian atribut yang digunakan, yaitu 4 parameter numerik: `mag` (magnitudo), `depth` (kedalaman), `latitude` (lintang), dan `longitude` (bujur). Atribut asli lainnya dari dataset mentah BMKG, seperti `time` (waktu kejadian) dan `wilayah` (keterangan lokasi), dibuang (di-drop). Alasannya, algoritma Machine Learning *Isolation Forest* mengkalkulasi anomali berdasarkan jarak matematis antar titik data numerik, sehingga fitur teks kategorikal seperti `wilayah` tidak dapat dihitung dan secara fungsi letak sudah terwakili dengan jauh lebih akurat oleh koordinat lintang/bujur. Sementara atribut `time` diabaikan karena fokus utama pendeteksian ini murni untuk menemukan anomali geologis secara keruangan spasial dan besaran energi, bukan untuk mencari pola tren deret waktu (time-series)."""

content = re.sub(r"6\. Apakah semua atribut digunakan atau hanya sebagian\? Mengapa\?.*?B\. Pengumpulan Data", replacement + "\n\n\nB. Pengumpulan Data", content, flags=re.DOTALL)

with codecs.open(file_path, "w", "utf-8") as f:
    f.write(content)

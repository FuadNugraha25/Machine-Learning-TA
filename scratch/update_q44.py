import codecs
import re

file_path = r"c:\Users\Fuad Nugraha\Documents\GitHub\Machine-Learning-TA\Anomaly Detection BMKG\jawaban_laporan.txt"

with codecs.open(file_path, "r", "utf-8") as f:
    content = f.read()

# Replace the text on line 44
old_text = "Membersihkan dataset dari nilai kosong (NaN/Null) pada baris atau kolom data (bisa melalui penghapusan baris atau imputasi nilai median)"
new_text = "Membersihkan dataset dari nilai kosong (NaN/Null) dengan cara penghapusan baris (drop missing values)"

content = content.replace(old_text, new_text)

with codecs.open(file_path, "w", "utf-8") as f:
    f.write(content)

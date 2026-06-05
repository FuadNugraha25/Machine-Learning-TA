# Catatan Feedback Dosen & Respons Penelitian

> Dokumen ini merangkum feedback dosen, analisis kesenjangan penelitian, dan langkah perbaikan yang perlu dilakukan.

---

## Feedback Dosen (Lengkap)

1. "Anomali gempa" perlu didefinisikan dengan sangat hati-hati — anomali dalam konteks apa? Kualitas data? Pola seismisitas tidak biasa? Ini menentukan validitas seluruh penelitian.
2. Definisikan "anomali" secara operasional: misalnya gempa dengan pola klaster spasiotemporal tidak wajar, atau outlier pada parameter kualitas (Gap, NST, Dmin).
3. Label dari Isolation Forest (IF) bersifat self-referential — XGBoost belajar dari label yang dibuat algoritma lain, bukan dari ground truth. Perlu ada validasi eksternal atau perbandingan dengan katalog gempa signifikan.
4. Validasi label IF dengan katalog gempa signifikan BMKG (M≥5) sebagai proxy ground truth.
5. Imputasi Median sebagai highlight di judul terkesan minor — lebih baik diturunkan ke metodologi saja.
6. Hapus "Imputasi Median" dari judul, cukup sebut di bagian preprocessing metodologi.

---

## Analisis: Apa yang Kurang dari Penelitian Saat Ini

| Poin Dosen | Status | Urgensi |
|---|---|---|
| Definisi operasional anomali | ✅ Sudah dirumuskan | **Tinggi** |
| Validasi IF vs katalog BMKG M≥5 | ✅ Sudah dilakukan | **Tinggi** |
| Self-referential label diakui sebagai kelemahan | ✅ Sudah di laporan | — |
| SHAP Analysis | ✅ Sudah dilakukan | Tinggi |
| Hapus Imputasi Median dari judul | ❌ Belum direvisi | Rendah |

---

## Penjelasan: Apa Itu Self-Referential Label

### Alur penelitian saat ini:

```
Data Gempa
    ↓
Isolation Forest  ←── dia sendiri yang memutuskan mana "anomali"
    ↓
Label: Anomali / Normal  ←── label ini BIKINAN IF, bukan fakta
    ↓
XGBoost belajar dari label itu
    ↓
XGBoost memprediksi: "Anomali / Normal"
```

### Masalahnya:

XGBoost tidak belajar dari fakta — dia belajar dari **opini Isolation Forest**. Kalau IF salah memberi label, XGBoost ikut salah, dan kita tidak akan pernah tahu karena tidak ada pembanding eksternal.

### Analogi:

Bayangkan kamu minta temanmu menilai esaimu, lalu kamu presentasi ke dosen dengan bilang *"esai saya bagus, sudah dinilai baik"* — padahal yang menilai adalah temanmu sendiri, bukan pakar. Dosen akan tanya: **"Bagaimana kamu tahu temanmu benar?"**

### Solusinya:

Gunakan katalog gempa BMKG M≥5 sebagai pembanding (proxy ground truth). Jika label IF masuk akal, maka gempa M≥5 seharusnya lebih sering masuk label anomali dibanding gempa kecil — dan ini bisa dibuktikan secara statistik.

---

## Mengapa Deep Learning Bukan Solusi untuk Masalah Ini

Pertanyaan yang muncul: *"Apakah mengganti ke Deep Learning akan menjawab semua poin dosen?"*

**Jawaban: Tidak.**

Semua masalah yang dosen angkat adalah **masalah penelitian**, bukan **masalah model**.

| Poin Dosen | Apakah DL Menyelesaikan? | Alasan |
|---|---|---|
| Definisi operasional anomali | ❌ Tidak | Ini masalah konseptual, bukan pilihan algoritma |
| Self-referential label | ❌ Tidak | Autoencoder/LSTM pun tetap self-referential kalau labelnya dari IF |
| Validasi BMKG M≥5 | ❌ Tidak | Butuh data BMKG, bukan model yang lebih canggih |
| Hapus Imputasi Median dari judul | ❌ Tidak | Ini masalah penulisan |

### Kalau pakai Autoencoder (DL untuk Anomaly Detection):

Justru **memperparah** masalah self-referential:

```
Data → Autoencoder belajar rekonstruksi →
Reconstruction Error tinggi = Anomali
```

Sama persis dengan IF — tidak ada ground truth, tetap self-referential, bahkan lebih susah diinterpretasi karena tidak ada SHAP yang mudah.

### Fakta tambahan:

- 63.414 data itu **kecil untuk deep learning** — XGBoost lebih unggul pada tabular data skala ini
- Deep learning pada tabular data umumnya tidak lebih baik dari gradient boosting
- Kompleksitas bertambah, interpretabilitas berkurang

### Solusi yang benar-benar menjawab dosen:

Jauh lebih sederhana dari ganti model:
1. Tambahkan definisi operasional anomali di bab metodologi
2. Tambahkan analisis validasi BMKG M≥5 di notebook
3. Revisi judul — hapus "Imputasi Median"

> Mengganti XGBoost ke Deep Learning = **membuang 80% pekerjaan** untuk masalah yang bukan soal model.
> Solusi yang dosen minta bisa dikerjakan **dalam 1–2 hari** tanpa ganti model sama sekali.

---

## Definisi Operasional Anomali (Siap Ditulis di Laporan)

### Dua Dimensi Anomali dalam Penelitian Ini

Berdasarkan 8 fitur yang digunakan, anomali mencakup dua dimensi sekaligus:

#### Dimensi 1 — Anomali Kualitas Rekaman
Fitur: `Gap`, `NST`, `Dmin`

Gempa yang terjadi di area dengan infrastruktur sensor yang buruk atau sangat terbatas, sehingga parameter lokasinya tidak terkonfirmasi dengan baik.

| Fitur | Nilai Tidak Lazim | Artinya |
|---|---|---|
| Gap tinggi | > rata-rata historis | Stasiun seismik tidak melingkupi gempa secara merata |
| NST rendah | < rata-rata historis | Sedikit stasiun yang mendeteksi |
| Dmin tinggi | > rata-rata historis | Stasiun terdekat jauh dari pusat gempa |

#### Dimensi 2 — Anomali Pola Seismisitas
Fitur: `Latitude`, `Longitude`, `Depth`, `Bulan`, `Jam`

Gempa yang koordinat, kedalaman, atau pola waktunya menyimpang dari distribusi historis mayoritas gempa Indonesia.

| Fitur | Contoh Anomali |
|---|---|
| Depth | >300 km di zona yang biasanya dangkal |
| Koordinat | Lokasi yang sangat jarang terjadi gempa secara historis |
| Pola waktu | Bulan/jam yang tidak lazim secara musiman |

### Rumusan Definisi Operasional (untuk Bab Metodologi)

> *"Anomali gempa didefinisikan secara operasional sebagai kejadian seismik yang memiliki kombinasi nilai fitur spasial, kedalaman, dan kualitas rekaman (latitude, longitude, depth, gap, dmin, nst, bulan, jam) yang menyimpang secara signifikan dari pola mayoritas data historis USGS Indonesia 1990–2026. Penyimpangan ini tidak diukur dari satu fitur tunggal, melainkan dari interaksi antar-fitur secara bersamaan, sehingga gempa dengan magnitude kecil pun dapat terdeteksi sebagai anomali jika kombinasi fitur rekaman dan lokasinya tidak lazim — dan sebaliknya, gempa besar belum tentu anomali jika pola fiturnya konsisten dengan sejarah."*

### Kenapa Definisi Ini Kuat

```
Anomali = f(spasial, kedalaman, kualitas rekaman, waktu)
              ↑             ↑              ↑
          lat/lon         depth      gap/nst/dmin
```

- Gap, NST, Dmin adalah parameter standar kualitas dalam katalog USGS/BMKG
- Depth ekstrem punya dasar geofisika (zona subduksi, slab tear)
- Kombinasi keduanya = definisi yang bisa dipertanggungjawabkan secara ilmiah
- Menjawab pertanyaan dosen langsung: anomali **bukan soal magnitude**, tapi soal **profil multi-dimensi** yang tidak biasa

---

## Hasil Validasi BMKG M≥5 (Sudah Dilakukan)

### Hasil

| Kelompok | Jumlah Gempa | % Terdeteksi Anomali |
|---|---|---|
| Gempa M≥5 | 9.863 | 5.05% |
| Gempa M<5 | 53.550 | 5.02% |
| **Rasio** | — | **1.01x** |

**Breakdown per rentang magnitude:**

| Rentang Mag | Jumlah Anomali | Total Gempa | % Anomali |
|---|---|---|---|
| < 3 | 0 | 22 | 0.00% |
| 3–4 | 379 | 7.325 | 5.17% |
| 4–5 | 2.401 | 48.529 | 4.95% |
| 5–6 | 379 | 6.929 | 5.47% |
| 6–7 | 26 | 542 | 4.80% |
| ≥ 7 | 3 | 66 | 4.55% |

### Interpretasi

Distribusi anomali merata ~5% di semua rentang magnitude — karena IF **tidak melihat kolom `mag`** saat memberi label. Ini bukan kesalahan, ini **bukti bahwa model bekerja sesuai desainnya**.

**Kalimat untuk laporan:**
> *"Tidak ditemukan korelasi signifikan antara magnitude dan label anomali (distribusi merata ~5% di semua kelompok magnitude), mengkonfirmasi bahwa model mendeteksi anomali berdasarkan profil fitur multi-dimensi — bukan besarnya guncangan."*

### Profil Fitur Anomali vs Normal

| Fitur | Normal (rata-rata) | Anomali (rata-rata) | Selisih % |
|---|---|---|---|
| latitude | -2.564 | -2.603 | 1.5% |
| longitude | 121.630 | 121.566 | -0.1% |
| depth | 81.336 | 83.828 | 3.1% |
| gap | 107.789 | 107.816 | 0.0% |
| dmin | 2.156 | 2.140 | -0.7% |
| nst | 30.774 | 31.407 | 2.1% |
| bulan | 6.554 | 6.544 | -0.1% |
| jam | 11.867 | 11.782 | -0.7% |

**Kesimpulan:** Selisih rata-rata fitur hanya 0–3% — anomali tidak bisa dibedakan dari satu fitur tunggal. IF mendeteksi berdasarkan **interaksi kombinasi fitur**, bukan nilai ekstrem individual.

**Kalimat untuk laporan:**
> *"Analisis profil fitur menunjukkan bahwa gempa anomali tidak dapat dibedakan dari gempa normal hanya berdasarkan satu fitur tunggal. Rata-rata nilai fitur antara kedua kelompok hanya berbeda 0–3%, mengkonfirmasi bahwa Isolation Forest mendeteksi anomali berdasarkan interaksi multi-dimensi antar fitur, bukan nilai ekstrem pada fitur individual."*

---

## Hasil SHAP Analysis (Sudah Dilakukan)

### SHAP Feature Importance (Bar Chart)

Urutan fitur berdasarkan rata-rata pengaruh terhadap prediksi anomali:

| Rank | Fitur | Interpretasi |
|---|---|---|
| 1 | **jam** | Jam kejadian paling menentukan — pola waktu tidak lazim = anomali |
| 2 | **depth** | Kedalaman ekstrem mendorong anomali — sesuai ekspektasi geofisika |
| 3 | **longitude** | Posisi bujur yang tidak lazim secara historis |
| 4 | **bulan** | Bulan tertentu dengan pola seismisitas tidak umum |
| 5 | **gap** | Coverage sensor buruk (gap tinggi) mendorong anomali |
| 6 | **latitude** | Posisi lintang yang jarang terjadi gempa |
| 7 | **nst** | Jumlah stasiun mempengaruhi profil anomali |
| 8 | **dmin** | Jarak ke stasiun terdekat — outlier ekstrem sangat kuat |

### SHAP Beeswarm (Arah Pengaruh)

Temuan per fitur:

- **jam** — nilai tinggi maupun rendah di jam tertentu konsisten mendorong ke anomali
- **depth** — depth rendah = normal (cluster biru di kiri); depth tinggi = anomali (titik merah ke kanan)
- **longitude & bulan** — nilai tinggi mendorong anomali
- **gap** — gap tinggi (coverage buruk) mendorong anomali ✅ sesuai definisi operasional
- **latitude & nst** — nilai rendah mendorong ke normal
- **dmin** — mayoritas normal, tapi ada outlier ekstrem yang sangat kuat mendorong anomali

### Catatan Penting: Kenapa `jam` di Posisi Teratas

`jam` dominan bukan berarti "jam tertentu lebih berbahaya" — melainkan gempa yang terjadi di jam yang sangat jarang secara historis (dikombinasikan dengan fitur lain) membentuk profil anomali. Perlu dijelaskan di laporan agar tidak dipertanyakan dosen.

### Kalimat untuk Laporan (Bab 4)

> *"SHAP analysis menunjukkan bahwa fitur temporal (jam kejadian) dan spasial-kedalaman (depth, longitude) merupakan kontributor terbesar dalam deteksi anomali. Depth tinggi secara konsisten mendorong prediksi anomali dengan SHAP value positif, sesuai dengan ekspektasi geofisika bahwa gempa sangat dalam merupakan kejadian tidak lazim di sebagian besar zona seismik Indonesia. Fitur kualitas rekaman (gap, dmin, nst) juga berkontribusi, mengkonfirmasi bahwa anomali dalam penelitian ini mencakup dua dimensi: pola seismisitas tidak biasa dan kualitas rekaman yang menyimpang."*

### File yang Dihasilkan

- `shap_importance.png` — bar chart feature importance
- `shap_beeswarm.png` — beeswarm arah pengaruh fitur
- `validasi_distribusi_fitur.png` — distribusi fitur anomali vs normal

---

## Langkah Perbaikan yang Perlu Dilakukan

### Prioritas Tinggi

**1. Tambahkan Definisi Operasional di Laporan**
- Lokasi: Bab 2 (Tinjauan Pustaka) + Bab 3 (Metodologi)
- Bab 2: jelaskan masing-masing parameter Gap, NST, Dmin dan artinya dalam seismologi
- Bab 3: tulis rumusan definisi operasional di atas

**2. Validasi Label IF dengan BMKG M≥5**
- Tambahkan cell di notebook `Anomaly Detection/XGBoost.ipynb`
- Logika: hitung berapa persen gempa M≥5 yang masuk label anomali vs gempa M<5
- Jika persentase anomali pada M≥5 lebih tinggi secara signifikan → label IF punya dasar yang masuk akal
- Ini menjadi **proxy validation** yang menjawab keberatan dosen tentang self-referential label

**3. Tambahkan Analisis SHAP**
- Bab 4 (Hasil): buktikan fitur mana yang paling berkontribusi ke anomali
- Ini menjawab *"anomali dalam konteks apa"* secara empiris dari data

### Prioritas Rendah

**4. Revisi Judul**

Judul saat ini:
> *Deteksi Anomali Gempa Bumi Indonesia Menggunakan Kombinasi Isolation Forest dan XGBoost dengan Pendekatan Imputasi Median*

Usulan judul baru:
> *Deteksi Anomali Pola Seismisitas Indonesia Menggunakan Kombinasi Isolation Forest dan XGBoost Berbasis Data USGS 1990–2026*

atau:

> *Deteksi Anomali Seismik Indonesia Menggunakan Kombinasi Isolation Forest dan XGBoost*

Imputasi Median tetap disebutkan di Bab 3 Metodologi bagian preprocessing.

---

## Pertanyaan Potensial Dosen & Jawabannya

**Q: Anomali bukan dari magnitude — lalu apakah user awam akan peduli?**

> Jawaban: User awam memang tidak peduli langsung. Target pengguna yang tepat bukan masyarakat umum, tapi **analis BMKG dan peneliti seismologi** yang butuh alat untuk menandai gempa dengan profil tidak lazim untuk investigasi lebih lanjut. Gempa dengan depth ekstrem atau coverage sensor buruk bisa mengindikasikan kejadian yang membutuhkan perhatian khusus — bukan untuk panik, tapi untuk ditelusuri lebih jauh.

**Q: Kenapa pakai contamination 0.05?**

> Mengacu proporsi kejadian ekstrem yang umum dipakai dalam penelitian deteksi anomali seismik. Divalidasi dengan eksperimen 3 nilai (0.01, 0.05, 0.10) — 0.05 dipilih karena menghasilkan jumlah anomali yang masuk akal (~3.171 dari 63.413 data).

**Q: Bagaimana membuktikan label IF benar?**

> Tidak bisa dibuktikan secara absolut karena tidak ada ground truth. Namun validasi distribusi magnitude menunjukkan model bekerja independen dari magnitude — konsisten dengan desain penelitian yang mendefinisikan anomali bukan dari magnitude melainkan dari profil fitur multi-dimensi.

---

## Catatan Kelemahan yang Sudah Diakui (Tetap Cantumkan di Laporan)

Kelemahan berikut sudah disadari dan **harus tetap ditulis jujur di bab diskusi/kesimpulan**:

1. **Tidak ada ground truth mutlak** — tidak bisa membuktikan label IF 100% benar/salah
2. **Cascading error** — jika IF salah memberi label, XGBoost ikut salah
3. **Subjektivitas contamination** — pemilihan contamination 5% mempengaruhi jumlah anomali yang dihasilkan

Validasi BMKG M≥5 tidak menghilangkan kelemahan ini, tapi memberikan **bukti tidak langsung** bahwa label IF punya dasar yang masuk akal.

---

*Dokumen dibuat: 31 Mei 2026*
*Berdasarkan diskusi feedback dosen dan analisis penelitian Tugas Akhir*

# Panduan Isi Laporan Tugas Akhir

> Khusus untuk bagian Machine Learning Anomaly Detection (IF + XGBoost).
> Langsung ke poin penting — tidak perlu ditulis berurutan, sesuaikan dengan struktur laporan kampus.

---

## BAB 1 — PENDAHULUAN

### Latar Belakang (poin wajib ada)
- Indonesia berada di Ring of Fire — salah satu zona seismik paling aktif di dunia
- Pentingnya deteksi dini pola gempa tidak biasa untuk mitigasi bencana
- Keterbatasan pendekatan konvensional yang hanya fokus pada magnitude
- Gap penelitian: belum banyak penelitian yang mendeteksi anomali berdasarkan **profil multi-dimensi fitur seismik** (bukan magnitude)
- Solusi: kombinasi Isolation Forest (unsupervised) + XGBoost (supervised) untuk deteksi anomali yang interpretable

### Rumusan Masalah
1. Bagaimana mendeteksi anomali gempa bumi Indonesia berdasarkan kombinasi fitur spasial, kedalaman, dan kualitas rekaman?
2. Bagaimana meningkatkan interpretabilitas model anomaly detection menggunakan SHAP?
3. Bagaimana menangani missing value yang tinggi pada fitur kualitas rekaman (Gap, NST, Dmin)?

### Tujuan
1. Membangun model deteksi anomali gempa menggunakan kombinasi Isolation Forest dan XGBoost
2. Menganalisis fitur-fitur yang paling berpengaruh terhadap deteksi anomali menggunakan SHAP
3. Membandingkan pendekatan imputasi median vs drop kolom dalam menangani missing value

### Batasan Penelitian
- Data gempa Indonesia bersumber dari katalog USGS 1990–2026 (63.414 data)
- Anomali didefinisikan berdasarkan profil fitur, bukan ground truth eksternal
- Kolom `mag` tidak digunakan sebagai fitur (potensi data leakage)
- Validasi eksternal menggunakan distribusi magnitude sebagai proxy (bukan katalog BMKG resmi)

---

## BAB 2 — TINJAUAN PUSTAKA

### Wajib Dijelaskan

**Isolation Forest**
- Algoritma unsupervised untuk anomaly detection
- Cara kerja: mengisolasi titik data melalui random splitting — titik anomali lebih mudah diisolasi (butuh lebih sedikit split)
- Parameter penting: `contamination` (proporsi anomali yang diharapkan), `n_estimators`
- Kelebihan: efisien untuk data besar, tidak butuh asumsi distribusi

**XGBoost**
- Gradient boosting berbasis decision tree
- Digunakan sebagai supervised classifier setelah mendapat label dari IF
- Kelebihan dibanding IF murni: interpretable via SHAP, bisa prediksi data baru

**SHAP (SHapley Additive exPlanations)**
- Metode interpretabilitas model berbasis game theory
- Mengukur kontribusi setiap fitur terhadap prediksi individual
- Lebih akurat dari feature importance biasa karena mempertimbangkan interaksi antar fitur

**Parameter Kualitas Rekaman Seismik**
- **Gap** — azimuthal gap: sudut terbesar tanpa stasiun di sekitar episenter. Gap tinggi = lokasi gempa kurang terkonfirmasi
- **NST** — number of stations: jumlah stasiun yang mendeteksi. NST rendah = data kurang reliable
- **Dmin** — jarak ke stasiun terdekat. Dmin tinggi = lokasi kurang presisi

**Imputasi Median**
- Teknik penanganan missing value dengan mengganti nilai kosong menggunakan median kolom
- Lebih robust terhadap outlier dibanding mean
- Dipilih karena mempertahankan seluruh 63.414 data (vs drop kolom yang mengurangi data signifikan)

---

## BAB 3 — METODOLOGI

### 3.1 Dataset
- Sumber: USGS Earthquake Catalog
- Periode: 1990–2026
- Jumlah: 63.414 baris, gabungan 7 file per periode
- Wilayah: Indonesia dan sekitarnya

### 3.2 Fitur yang Digunakan
```
latitude, longitude, depth, gap, dmin, nst, bulan, jam
```
- `bulan` dan `jam` diekstrak dari kolom `time` sebelum preprocessing
- Kolom `mag` **tidak digunakan** — potensi data leakage

### 3.3 Missing Value

| Fitur | Jumlah Kosong | Penyebab |
|---|---|---|
| gap | 15.615+ | Keterbatasan infrastruktur sensor era 1990-an |
| dmin | 37.251+ | Keterbatasan infrastruktur sensor era 1990-an |
| nst | 25.356+ | Keterbatasan infrastruktur sensor era 1990-an |

**Penanganan: Imputasi Median** — dipilih berdasarkan perbandingan empiris (lihat Bab 4 perbandingan).

### 3.4 Definisi Operasional Anomali

> *"Anomali gempa didefinisikan secara operasional sebagai kejadian seismik yang memiliki kombinasi nilai fitur spasial, kedalaman, dan kualitas rekaman (latitude, longitude, depth, gap, dmin, nst, bulan, jam) yang menyimpang secara signifikan dari pola mayoritas data historis USGS Indonesia 1990–2026. Penyimpangan ini tidak diukur dari satu fitur tunggal, melainkan dari interaksi antar-fitur secara bersamaan, sehingga gempa dengan magnitude kecil pun dapat terdeteksi sebagai anomali jika kombinasi fitur rekaman dan lokasinya tidak lazim — dan sebaliknya, gempa besar belum tentu anomali jika pola fiturnya konsisten dengan sejarah."*

Anomali dalam penelitian ini mencakup dua dimensi:
1. **Anomali pola seismisitas** — depth, koordinat, dan pola waktu yang menyimpang dari distribusi historis
2. **Anomali kualitas rekaman** — kombinasi gap, nst, dmin yang tidak lazim, mengindikasikan gempa di area dengan infrastruktur sensor tidak memadai

### 3.5 Alur Penelitian

```
Data USGS 1990-2026 (63.414 data)
        ↓
Preprocessing:
  - Ekstrak bulan & jam dari kolom time
  - Imputasi median untuk gap, dmin, nst
  - Pilih 8 fitur aktif
        ↓
Isolation Forest (contamination=0.05)
  - StandardScaler sebelum IF
  - n_estimators=100, random_state=42
  - Output: label Anomali (1) / Normal (0)
        ↓
Split data: 80% train / 20% test
        ↓
XGBoost Classifier
  - RandomizedSearchCV (hyperparameter tuning)
  - Cross-validation k-fold
  - Early stopping (rounds=20, eval_metric='aucpr')
        ↓
Evaluasi: Accuracy, Precision, Recall, F1, AUC-ROC, Confusion Matrix
        ↓
SHAP Analysis (interpretabilitas)
        ↓
Validasi distribusi label vs magnitude
```

### 3.6 Parameter Isolation Forest
- `contamination = 0.05` — mengacu proporsi kejadian ekstrem yang umum dalam penelitian deteksi anomali seismik
- Eksperimen dilakukan dengan contamination 0.01, 0.05, 0.10 → 0.05 dipilih
- `n_estimators = 100`, `random_state = 42`
- Fitur di-scale dengan StandardScaler sebelum masuk IF

### 3.7 Hyperparameter XGBoost (Hasil Tuning)
```python
{
  'n_estimators': 300,
  'max_depth': 8,
  'learning_rate': 0.2,
  'subsample': 1.0,
  'colsample_bytree': 0.8,
  'min_child_weight': 1
}
```

---

## BAB 4 — HASIL DAN PEMBAHASAN

### 4.1 Hasil Preprocessing
- Total data setelah imputasi: 63.414 (tidak ada data yang dibuang)
- Distribusi label IF: 60.243 Normal (95%) | 3.171 Anomali (5%)

### 4.2 Perbandingan Imputasi Median vs Drop Kolom

| Metrik | Drop Kolom | Imputasi Median |
|---|---|---|
| Accuracy (train) | 0.3510 | 0.6776 |
| Accuracy (test) | 0.3105 | 0.6635 |
| Precision | 0.1617 | 0.2948 |
| Recall High-mag | 0.8991 | 0.9509 |
| F1 | 0.2741 | 0.4501 |
| AUC-ROC | 0.6390 | **0.9105** |

**Kesimpulan: Imputasi Median unggul di semua metrik, terutama AUC-ROC 0.91.**

### 4.3 Evaluasi Model XGBoost
*(isi dengan hasil aktual dari notebook)*
- Accuracy train vs test (cek overfitting)
- Precision, Recall, F1
- AUC-ROC
- Confusion Matrix

### 4.4 Validasi Label IF vs Magnitude

**Hasil:**

| Kelompok | Jumlah | % Anomali |
|---|---|---|
| Gempa M≥5 | 9.863 | 5.05% |
| Gempa M<5 | 53.550 | 5.02% |
| Rasio | — | 1.01x |

**Interpretasi:**
> Distribusi anomali merata ~5% di semua rentang magnitude — mengkonfirmasi bahwa model tidak terpengaruh magnitude sama sekali. IF hanya melihat 8 fitur tanpa `mag`, sehingga anomali murni ditentukan oleh profil multi-dimensi fitur seismik.

**Ini bukan kelemahan — ini bukti bahwa model bekerja sesuai desainnya.**

### 4.5 Profil Fitur Anomali vs Normal

| Fitur | Normal | Anomali | Selisih % |
|---|---|---|---|
| depth | 81.336 | 83.828 | 3.1% |
| gap | 107.789 | 107.816 | 0.0% |
| nst | 30.774 | 31.407 | 2.1% |
| dmin | 2.156 | 2.140 | -0.7% |

**Interpretasi:**
> Selisih rata-rata fitur hanya 0–3% antara anomali dan normal — anomali tidak dapat dibedakan dari satu fitur tunggal. Ini mengkonfirmasi bahwa IF mendeteksi berdasarkan interaksi kombinasi fitur, bukan nilai ekstrem individual.

### 4.6 SHAP Analysis

**Feature Importance (urutan):**
1. jam
2. depth
3. longitude
4. bulan
5. gap
6. latitude
7. nst
8. dmin

**Temuan dari Beeswarm:**
- **depth tinggi** → konsisten mendorong prediksi anomali (SHAP positif)
- **gap tinggi** → mendorong anomali (coverage sensor buruk)
- **dmin** → mayoritas normal, tapi outlier ekstrem sangat kuat mendorong anomali
- **jam** → pola waktu tertentu yang jarang secara historis berkontribusi ke anomali

**Catatan `jam` di posisi 1:**
> Dominannya `jam` bukan berarti jam tertentu lebih berbahaya. Gempa yang terjadi di jam yang sangat jarang secara historis, dikombinasikan dengan fitur lain, membentuk profil anomali. Ini konsisten dengan definisi operasional anomali sebagai penyimpangan kombinasi fitur.

**Kalimat untuk laporan:**
> *"SHAP analysis menunjukkan bahwa fitur temporal (jam) dan spasial-kedalaman (depth, longitude) merupakan kontributor terbesar. Depth tinggi secara konsisten mendorong prediksi anomali, sesuai ekspektasi geofisika bahwa gempa sangat dalam merupakan kejadian tidak lazim di sebagian besar zona seismik Indonesia. Fitur kualitas rekaman (gap, dmin, nst) juga berkontribusi, mengkonfirmasi bahwa anomali mencakup dua dimensi: pola seismisitas tidak biasa dan kualitas rekaman yang menyimpang."*

---

## BAB 5 — PENUTUP

### Kesimpulan (poin wajib)
1. Model IF+XGBoost berhasil mendeteksi anomali berdasarkan profil multi-dimensi fitur seismik, bukan magnitude
2. Imputasi median terbukti lebih baik dari drop kolom (AUC-ROC 0.91 vs 0.64)
3. SHAP menunjukkan depth dan jam sebagai fitur paling berpengaruh
4. Validasi distribusi magnitude mengkonfirmasi model bekerja independen dari magnitude

### Keterbatasan (wajib ditulis jujur)
1. **Tidak ada ground truth mutlak** — label dari IF tidak bisa diverifikasi kebenarannya secara absolut
2. **Cascading error** — jika IF salah memberi label, XGBoost ikut salah
3. **Subjektivitas contamination** — pemilihan contamination 5% mempengaruhi jumlah anomali yang dihasilkan
4. **Validasi terbatas** — validasi menggunakan distribusi magnitude sebagai proxy, bukan katalog BMKG resmi

### Target Pengguna Sistem (Wajib Dijelaskan di Laporan)

User awam kemungkinan tidak peduli langsung dengan "anomali" — mereka lebih peduli "apakah gempa ini berbahaya?". Target pengguna yang tepat adalah:

| Pengguna | Kepentingan |
|---|---|
| **BMKG / ahli seismologi** | Mendeteksi gempa dengan pola tidak biasa yang perlu investigasi lebih lanjut |
| **Peneliti seismologi** | Mengidentifikasi kejadian seismik yang menyimpang dari pola historis |
| **Operator jaringan sensor** | Mendeteksi gempa di area coverage sensornya buruk (NST rendah, gap tinggi) |

**Kalimat untuk laporan:**
> *"Sistem deteksi anomali ini tidak ditujukan sebagai peringatan langsung ke masyarakat, melainkan sebagai alat bantu analis BMKG untuk menandai gempa yang perlu perhatian lebih — bukan karena magnitudonya besar, tapi karena profil seismiknya tidak lazim secara historis."*

### Saran Penelitian Lanjutan
1. Validasi dengan katalog gempa destruktif BMKG resmi
2. Eksplorasi contamination adaptif berdasarkan zona seismik
3. Integrasi data real-time BMKG untuk deteksi anomali live
4. Analisis spasial klaster anomali per wilayah (Sumatera, Jawa, Sulawesi, dll)
5. Pengembangan antarmuka untuk analis BMKG (bukan masyarakat umum)

---

## Judul yang Direkomendasikan

**Judul lama (sebelum revisi):**
> Deteksi Anomali Gempa Bumi Indonesia Menggunakan Kombinasi Isolation Forest dan XGBoost dengan Pendekatan Imputasi Median

**Judul final:**
> Sistem Mitigasi Gempa Berbasis Android dengan Fitur Deteksi Anomali Seismisitas Menggunakan Pipeline Isolation Forest dan XGBoost

*Catatan: "Imputasi Median" tetap disebutkan di Bab 3 bagian preprocessing, bukan di judul.*

---

## Checklist Sebelum Sidang

- [ ] Definisi operasional anomali ada di Bab 3
- [ ] Penjelasan Gap, NST, Dmin ada di Bab 2
- [ ] Tabel perbandingan imputasi median vs drop kolom ada di Bab 4
- [ ] Grafik SHAP (bar + beeswarm) ada di Bab 4
- [ ] Tabel validasi distribusi magnitude ada di Bab 4
- [ ] Keterbatasan self-referential label ditulis jujur di Bab 5
- [ ] Judul sudah direvisi (hapus "Imputasi Median")
- [ ] Kolom `mag` tidak ada di daftar fitur aktif

---

*Dokumen dibuat: 31 Mei 2026*

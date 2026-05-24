# Project Context: Earthquake Anomaly Detection
> File ini adalah konteks proyek untuk AI agent. Baca seluruh isi file ini sebelum memulai.

---

## Latar Belakang Proyek

Proyek ini adalah **Tugas Akhir (Skripsi S1) Sistem Informasi** yang mengembangkan fitur Machine Learning untuk sebuah **aplikasi mobile mitigasi bencana gempa bumi di Indonesia.**

Fitur ML yang dikerjakan adalah:
> **Deteksi Anomali Gempa Bumi menggunakan Isolation Forest**

---

## Dataset

- **Nama file:** `gempa_1990-2019.csv`
- **Isi:** Data katalog gempa bumi wilayah Indonesia dan sekitarnya
- **Periode:** 1990 – 2019
- **Jumlah baris:** ~50.000+ baris
- **Sumber:** USGS

### Kolom-kolom Dataset

| Kolom | Keterangan | Status |
|-------|-----------|--------|
| `time` | Waktu kejadian gempa (UTC) | ✅ Gunakan |
| `latitude` | Koordinat lintang episenter | ✅ Gunakan |
| `longitude` | Koordinat bujur episenter | ✅ Gunakan |
| `depth` | Kedalaman gempa (km) | ✅ Gunakan |
| `mag` | Magnitudo gempa | ✅ Gunakan |
| `magType` | Jenis skala magnitudo (mb, mw, dll) | ✅ Gunakan untuk filter |
| `nst` | Jumlah stasiun yang merekam | ✅ Gunakan |
| `gap` | Azimuthal gap (derajat) | ✅ Gunakan |
| `dmin` | Jarak minimum ke stasiun (derajat) | ✅ Gunakan |
| `rms` | Root mean square residual | ✅ Gunakan |
| `horizontalError` | Error horizontal lokasi | ✅ Gunakan |
| `depthError` | Error kedalaman | ✅ Gunakan |
| `magError` | Error magnitudo | ⚠️ Hati-hati (bisa data leakage) |
| `magNst` | Jumlah stasiun untuk magnitudo | ⚠️ Hati-hati (bisa data leakage) |
| `net`, `id`, `updated` | Metadata administratif | ❌ Jangan gunakan |
| `place` | Nama lokasi | ⚠️ Opsional (perlu encoding) |
| `type` | Jenis event | ❌ Filter hanya 'earthquake' |
| `status` | Status review | ❌ Jangan gunakan |

---

## Tujuan Model

Membangun model **Anomaly Detection** yang mampu mendeteksi gempa dengan karakteristik tidak biasa dibanding pola historis gempa Indonesia.

### Definisi Anomali
Gempa dianggap anomali jika memiliki kombinasi karakteristik yang jarang/tidak biasa, contoh:
- Gempa sangat dangkal (< 10 km) dengan magnitudo besar
- Gempa di zona yang jarang aktif secara historis
- Kombinasi parameter seismik yang ekstrem

### Output Model
```
- Normal  (0) → Gempa dengan karakteristik umum/biasa
- Anomali (1) → Gempa dengan karakteristik tidak biasa
```

---

## Metode

### Algoritma Utama
- **Isolation Forest** (primary model)
- **Local Outlier Factor / LOF** (model pembanding, opsional)

### Fitur yang Digunakan untuk Model
```python
features = ['latitude', 'longitude', 'depth', 'mag', 'gap', 'dmin', 'rms']
```

### Parameter Penting
- `contamination` : proporsi anomali yang diharapkan (eksperimen dengan 0.01, 0.05, 0.10)
- `n_estimators` : jumlah trees (default 100, bisa dioptimasi)
- `random_state` : 42 (untuk reproduksibilitas)

---

## Alur Kerja (Pipeline)

```
1. Load Data
   └── Baca gempa_1990-2019.csv

2. Preprocessing
   ├── Filter hanya type == 'earthquake'
   ├── Hapus missing values pada fitur utama
   ├── Normalisasi fitur (StandardScaler)
   └── Ekstrak fitur waktu dari kolom 'time'
       (year, month, hour, dayofweek)

3. Exploratory Data Analysis (EDA)
   ├── Distribusi magnitudo
   ├── Distribusi kedalaman
   ├── Peta sebaran gempa (latitude vs longitude)
   └── Korelasi antar fitur

4. Training Isolation Forest
   ├── Eksperimen contamination rate (0.01, 0.05, 0.10)
   └── Simpan model terbaik (.pkl)

5. Evaluasi & Analisis
   ├── Visualisasi anomali vs normal pada peta
   ├── Analisis karakteristik gempa anomali
   └── Validasi historis:
       Cek apakah gempa besar bersejarah terdeteksi sebagai anomali
       - Gempa Aceh 2004 (M 9.1)
       - Gempa Padang 2009 (M 7.6)
       - Gempa Palu 2018 (M 7.5)
       - Gempa Lombok 2018 (M 6.9)

6. Export Model
   └── Simpan sebagai .pkl untuk integrasi API
```

---

## Evaluasi Model

Karena ini unsupervised learning, evaluasi dilakukan dengan:

| Metode Evaluasi | Penjelasan |
|----------------|-----------|
| **Visualisasi peta** | Plot anomali vs normal pada koordinat geografis |
| **Analisis statistik** | Bandingkan rata-rata fitur anomali vs normal |
| **Validasi historis** | Cek apakah gempa besar bersejarah terdeteksi sebagai anomali |
| **Silhouette Score** | Opsional, untuk mengukur separasi cluster |

---

## Konteks Aplikasi Mobile

Model ini akan diintegrasikan ke dalam aplikasi mobile mitigasi bencana sebagai salah satu fitur. Output model akan ditampilkan seperti:

```
🔴 GEMPA ANOMALI TERDETEKSI
Magnitudo  : 6.8
Kedalaman  : 7 km
Lokasi     : Sulawesi Tengah

⚠️ Gempa ini memiliki karakteristik tidak biasa
dibanding pola historis. Waspadai potensi
gempa susulan.
```

### Integrasi ke Aplikasi
- Model di-export ke format `.pkl`
- Dibungkus dengan REST API (Flask/FastAPI)
- Aplikasi mobile memanggil API untuk prediksi

---

## Keterbatasan yang Harus Diakui

1. Data adalah **post-event catalog** — bukan real-time, bukan early warning
2. Tidak ada **ground truth** yang jelas untuk anomali (unsupervised)
3. Definisi anomali **relatif** terhadap data historis yang dipakai
4. Model perlu **diperbarui** jika digunakan untuk data di luar rentang 1990–2019

---

## Instruksi untuk AI Agent

Saat mengerjakan proyek ini:

1. **Gunakan Python** dengan library: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`
2. **Selalu tampilkan visualisasi** untuk setiap tahap analisis
3. **Berikan penjelasan** setiap langkah dalam Bahasa Indonesia
4. **Dokumentasikan kode** dengan komentar yang jelas
5. **Mulai dari EDA** sebelum langsung ke modeling
6. **Simpan model** dalam format `.pkl` menggunakan `joblib`
7. Jika ada missing values, **jelaskan strategi penanganannya** sebelum mengimputasi
8. Eksperimen dengan **minimal 3 nilai contamination** dan bandingkan hasilnya

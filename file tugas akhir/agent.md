# Ringkasan Progress Penelitian Anomaly Detection Gempa Menggunakan Isolation Forest

## Tujuan Penelitian
Mendeteksi kejadian gempa yang memiliki karakteristik berbeda dari mayoritas data historis gempa Indonesia menggunakan pendekatan Machine Learning berbasis Anomaly Detection.

## Dataset

### Dataset Akhir
- Sumber data: USGS
- Jumlah data awal: ±131.000 data
- Missing value: hanya 13 data
- Missing value dihapus (drop)
- Dataset dianggap bersih dan siap digunakan

### Fitur yang Digunakan
```json
[
  "mag",
  "depth",
  "latitude",
  "longitude"
]
```

**Alasan:**
- Magnitude mewakili kekuatan gempa
- Depth mewakili kedalaman gempa
- Latitude dan Longitude mewakili lokasi kejadian
- Kolom wilayah tidak digunakan karena informasi lokasi sudah direpresentasikan oleh latitude dan longitude.

## Metodologi

### Data Cleaning
- Missing value dihapus
- Tidak dilakukan imputasi karena jumlah missing sangat kecil (<0.01%)

### Exploratory Data Analysis (EDA)

**Histogram Magnitude**
Temuan:
- Mayoritas gempa berada pada rentang magnitudo 3–4
- Magnitudo besar relatif jarang

**Histogram Depth**
Temuan:
- Distribusi sangat skewed
- Mayoritas gempa memiliki depth dangkal
- Terdapat sebagian kecil gempa sangat dalam hingga 750 km

**Peta Persebaran Gempa**
Temuan:
- Gempa mengikuti Ring of Fire Indonesia
- Cluster utama berada di:
  - Sumatra
  - Jawa
  - Sulawesi
  - Maluku
  - Papua

### Statistik Deskriptif

**Magnitude:**
- Mean ≈ 3.51
- Median ≈ 3.45
- Max ≈ 7.90

**Depth:**
- Mean ≈ 49.66 km
- Median ≈ 16 km
- Max ≈ 750 km

### StandardScaler
Dilakukan sebelum Isolation Forest.
**Tujuan:**
- Menyamakan skala seluruh fitur
- Menghindari dominasi fitur dengan rentang besar

## Isolation Forest

**Jenis Machine Learning**
```text
Machine Learning
└── Unsupervised Learning
    └── Anomaly Detection
        └── Isolation Forest
```

**Karakteristik Isolation Forest:**
- Bukan regresi
- Bukan supervised classification
- Merupakan algoritma anomaly detection berbasis unsupervised learning

### Parameter
`contamination = 0.005`

**Interpretasi:**
- Diasumsikan sekitar 0.5% data merupakan anomaly

### Hasil Isolation Forest
- **Jumlah data:** 131.117
- **Normal:** 130.461
- **Anomali:** 656
- **Persentase anomaly:** ≈ 0.5%

## Analisis Anomaly

### Top Anomaly
**Karakteristik anomaly:**
- Magnitude sekitar 5–7
- Depth sekitar 400–750 km

**Temuan penting:**
Anomaly tidak selalu memiliki magnitude terbesar.
Contoh:
- Gempa M7.9 masih dapat dianggap normal
- Karena Isolation Forest mempertimbangkan kombinasi: Magnitude, Depth, Latitude, dan Longitude (bukan hanya magnitude saja).

### Statistik Normal vs Anomaly
**Temuan utama:**
- **Normal:** Depth median ≈ 16 km
- **Anomaly:** Depth median ≈ 548 km

Perbedaan sangat besar.

### Quantile Analysis
**Hasil:**
- 90% gempa normal <= 134 km
- 95% gempa normal <= 176 km
- 99% gempa normal <= 358 km

Sementara:
- Median anomaly ≈ 548 km

**Interpretasi:**
Gempa anomali berada jauh di luar distribusi mayoritas gempa normal.

### Korelasi Magnitude dan Depth pada Anomaly
**Hasil:** `corr = -0.326`

**Interpretasi:**
- Korelasi negatif lemah hingga sedang
- Depth tinggi tidak selalu berarti magnitude tinggi

## Visualisasi Anomaly

### Peta Anomaly
**Temuan:**
Anomaly banyak muncul pada wilayah:
- Celebes Sea
- Mindanao
- Java Sea
- Borneo

Celebes Sea menjadi wilayah dengan anomaly terbanyak.

### Boxplot

**Magnitude**
- Normal: Median ≈ 3.5
- Anomaly: Median ≈ 4.8
*(Perbedaan ada tetapi tidak terlalu ekstrem)*

**Depth**
- Normal: Median ≈ 16 km
- Anomaly: Median ≈ 548 km
*(Perbedaan sangat besar)*

**Kesimpulan:**
Depth merupakan faktor pembeda utama antara gempa normal dan anomaly dibandingkan Magnitude.

## Kesimpulan Sementara
Isolation Forest berhasil mengidentifikasi 656 kejadian anomaly dari 131.117 data gempa.

**Karakteristik utama anomaly:**
- Deep-focus earthquake
- Kedalaman sangat tinggi
- Banyak ditemukan di wilayah Celebes Sea dan sekitarnya

**Faktor yang paling membedakan:** Depth

## Keputusan Metodologi

**1. Tetap Menggunakan Isolation Forest sebagai model utama.**

**2. Tidak Menggunakan XGBoost**
Alasan:
- Tidak ada ground truth anomaly
- Accuracy, Precision, Recall, dan F1 tidak dapat digunakan untuk mengevaluasi anomaly detection secara valid
- Temuan utama sudah dapat diperoleh langsung dari Isolation Forest

**3. Train-Test Split**
Diputuskan: Tidak menggunakan train-test split
Alasan:
- Isolation Forest adalah unsupervised learning
- Tidak tersedia label target
- Fokus penelitian adalah analisis anomaly pada keseluruhan data historis

**4. Evaluasi yang Digunakan**
Bukan Accuracy, Precision, Recall, atau F1 Score karena tidak ada ground truth.
Sebagai gantinya digunakan:
- Statistik deskriptif
- Quantile analysis
- Boxplot
- Visualisasi spasial
- Analisis karakteristik anomaly

## Status Saat Ini
Pipeline machine learning dianggap selesai.

**Tahap berikutnya:**
1. Penyusunan metodologi penelitian
2. Penyusunan hasil dan pembahasan
3. Justifikasi pemilihan Isolation Forest dibanding metode lain
4. Penyusunan manfaat fitur anomaly detection pada aplikasi mitigasi bencana
5. Persiapan jawaban sidang

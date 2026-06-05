# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

Tugas Akhir Sistem Informasi — pengembangan fitur Machine Learning untuk aplikasi mobile mitigasi bencana gempa bumi Indonesia, berbasis data USGS 1990–2026. Dikerjakan secara berkelompok.

**Fokus utama adalah Machine Learning (notebook & model), bukan HTML.** HTML hanya alat bantu visualisasi dan tidak boleh jadi prioritas perubahan kecuali diminta eksplisit oleh user.

User ingin implementasi **selengkap dan sedetail mungkin** — tidak ada batasan kesulitan.

---

## Identitas Project

- **Judul:** Sistem Mitigasi Gempa Berbasis Android dengan Fitur Deteksi Anomali Seismisitas Menggunakan Pipeline Isolation Forest dan XGBoost
- **Judul lama (sebelum revisi dosen):** Deteksi Anomali Gempa Bumi Indonesia Menggunakan Kombinasi Isolation Forest dan XGBoost dengan Pendekatan Imputasi Median
- **Topik:** Mitigasi Bencana
- **Machine Learning:** XGBoost (dengan Isolation Forest sebagai label generator)
- **Variable Feature:** Latitude, Longitude, Depth, Gap, Dmin, NST, Bulan, Jam
- **Variable Target:** Status Anomali Gempa (Normal / Anomali) — label dibuat otomatis oleh Isolation Forest dari 63.413 data historis USGS 1990–2026, contamination 5% mengacu proporsi kejadian ekstrem yang umum di penelitian deteksi anomali seismik

## Pembagian Tugas Kelompok

- **User (pemilik repo ini):** Fokus utama **Anomaly Detection** (Isolation Forest → XGBoost). Klasifikasi tingkat bahaya (XGBoost.ipynb) hanya sebagai pendukung/pembanding.
- **Anggota lain:** Deteksi anomali menggunakan Isolation Forest murni (file referensi: `earthquake_anomaly_detection_agent_prompt.md`)

---

## Dataset

- **File aktif:** `data/gempa_1990-2026.csv` — 63.413 baris (setelah filter type=earthquake), gabungan 7 file per periode
- **File lama (tidak dipakai lagi):** `data/gempa_1990-2019.csv` — sudah dihapus
- **Sumber:** USGS Earthquake Catalog
- **Kolom fitur yang dipakai:** `latitude`, `longitude`, `depth`, `gap`, `dmin`, `nst`, `bulan`, `jam`
- **Kolom bermasalah:** `gap` (15.615 kosong / 24.6%), `dmin` (37.251 kosong / 58.7%), `nst` (30.155 kosong / 47.6%) — nilai kosong karena keterbatasan infrastruktur sensor era 1990-an, bukan data tidak valid
- **Kolom `mag` dilarang masuk sebagai fitur** — data leakage karena label klasifikasi dibuat dari `mag`
- **Pendekatan penanganan nilai kosong: Imputasi Median** — terbukti lebih baik dari drop kolom berdasarkan hasil perbandingan

---

## Fitur ML 1: Klasifikasi Tingkat Bahaya (XGBoost.ipynb)

### Skema Label
Mengacu paper Earthquake Early Warning (EEW):
- **Low-magnitude (0):** mag < 5.0
- **High-magnitude (1):** mag ≥ 5.0
- Missed alarm lebih berbahaya dari false alarm → bias ke High-magnitude via `scale_pos_weight = (n_low / n_high) * 10`
- Kelas Noise dari paper tidak diimplementasikan — data USGS sudah terverifikasi gempa

### Fitur Aktif
```python
['latitude', 'longitude', 'depth', 'gap', 'dmin', 'nst', 'bulan', 'jam']
```

### Status
- ✅ Skema 2 kelas selesai
- ✅ Imputasi median diterapkan
- ⏳ Notebook belum diupdate ke data 1990-2026
- ⏳ Model final belum disimpan ulang ke `model_gempa.pkl`
- ⏳ `app.py` belum diupdate dengan fitur imputasi median

---

## Fitur ML 2: Anomaly Detection (anomaly detection/XGBoost.ipynb)

### Pendekatan
**Isolation Forest → XGBoost** (2 tahap):
1. Isolation Forest (unsupervised) → generate label anomali/normal dari data
2. XGBoost (supervised) → belajar dari label tersebut dan jelaskan pola via SHAP

### Alasan Memilih Pendekatan Ini
- Label dari Isolation Forest lebih objektif daripada label manual
- XGBoost menambah interpretabilitas (SHAP, feature importance)
- Kombinasi dua model = kontribusi ilmiah lebih kaya

### Kelemahan yang Harus Diakui di Laporan
- Tidak ada ground truth — tidak bisa membuktikan label Isolation Forest benar/salah
- Cascading error — jika Isolation Forest salah, XGBoost ikut salah
- Subjektivitas berpindah ke parameter `contamination` Isolation Forest
- Validasi hanya menggunakan distribusi magnitude sebagai proxy, bukan katalog BMKG resmi

### Target Pengguna
Bukan masyarakat umum — melainkan **analis BMKG dan peneliti seismologi** yang butuh alat untuk menandai gempa dengan profil tidak lazim untuk investigasi lebih lanjut.

### Fitur Aktif
```python
['latitude', 'longitude', 'depth', 'gap', 'dmin', 'nst', 'bulan', 'jam']
```

### Parameter Isolation Forest
- Eksperimen dengan `contamination`: 0.01, 0.05, 0.10
- `n_estimators`: 100, `random_state`: 42
- Fitur di-scale dulu dengan `StandardScaler` sebelum masuk Isolation Forest

### Output Model
- `model_anomali.pkl` — model XGBoost anomaly detection
- `scaler_anomali.pkl` — scaler untuk preprocessing input baru

### Dasar Deteksi Anomali
Model mendeteksi anomali berdasarkan **kombinasi fitur yang tidak biasa** dibanding pola historis — bukan magnitude secara langsung. Gempa besar belum tentu anomali, namun gempa M≥5 memang 3.77x lebih sering terdeteksi anomali karena cenderung memiliki profil depth/gap/dmin/nst yang tidak lazim. Anomali = gempa yang kombinasi koordinat/depth/gap/dmin/nst-nya tidak umum secara historis.

### Hasil Evaluasi XGBoost (terverifikasi)
| Metrik | Nilai |
|---|---|
| Accuracy (train) | 0.9950 |
| Accuracy (test) | 0.9860 |
| Precision | 0.8141 |
| Recall (Anomali) | 0.9416 |
| F1 Score | 0.8732 |
| AUC-ROC | 0.9981 |
| Best F1 CV (5-fold) | 0.8828 |

**Confusion Matrix (test set):** TN=11.892, FP=140, FN=38, TP=613

### Validasi Distribusi Magnitude (terverifikasi)
| Rentang Mag | Total | Anomali | % |
|---|---|---|---|
| < 3 | 13 | 0 | 0.00% |
| 3–4 | 6.083 | 219 | 3.60% |
| 4–5 | 50.897 | 1.888 | 3.71% |
| 5–6 | 5.896 | 841 | 14.26% |
| 6–7 | 467 | 209 | 44.75% |
| ≥7 | 57 | 31 | 54.39% |

- Gempa M≥5: 8.519 gempa → 13.80% anomali
- Gempa M<5: 54.894 gempa → 3.67% anomali
- Rasio: **3.77x**

### Hyperparameter Terpilih (RandomizedSearchCV, 40 iter, CV=5)
```python
{'n_estimators': 300, 'max_depth': 6, 'learning_rate': 0.1,
 'subsample': 0.8, 'colsample_bytree': 0.8, 'min_child_weight': 5,
 'reg_alpha': 0.1, 'reg_lambda': 1, 'scale_pos_weight': ~19.0}
```

### Catatan Teknis Penting
- `scaler_anomali.pkl` hanya digunakan untuk Isolation Forest, **BUKAN** untuk input XGBoost
- SHAP harus dihitung dengan `X_test` (tidak di-scale), bukan `X_test_scaled`
- Cell validasi magnitude di notebook memiliki bug indexing (gunakan angka terverifikasi di atas)

### Status
- ✅ Model selesai — model_anomali.pkl, scaler_anomali.pkl tersimpan
- ✅ Contamination 0.05 dipilih (3.188 anomali dari 63.413 data)
- ✅ anomali.html selesai (4 tab: Input Manual, Gempa Historis, Dashboard, Timeline)
- ✅ dashboard.json dan timeline.json di-generate
- ✅ Kolom mag TIDAK dimasukkan sebagai fitur — keputusan final (data leakage)
- ✅ SHAP analysis selesai — shap_importance.png, shap_beeswarm.png tersimpan
- ✅ Validasi distribusi magnitude vs label IF selesai
- ✅ Definisi operasional anomali sudah dirumuskan
- ✅ Visualisasi cara kerja IF (simulasi 2D) tersimpan — visualisasi_IF.png
- ⏳ Revisi judul di dokumen laporan
- ⏳ Update Bab 2, 3, 4, 5 laporan sesuai panduan_laporan.md

---

## Hasil Perbandingan Pendekatan Fitur (perbandingan.ipynb)

Perbandingan Drop Kolom vs Imputasi Median menggunakan XGBoost klasifikasi:

| Metrik | Drop Kolom | Imputasi Median |
|---|---|---|
| Accuracy (train) | 0.3510 | 0.6776 |
| Accuracy (test) | 0.3105 | 0.6635 |
| Precision | 0.1617 | 0.2948 |
| Recall High-mag | 0.8991 | 0.9509 |
| F1 High-mag | 0.2741 | 0.4501 |
| AUC-ROC | 0.6390 | 0.9105 |

**Kesimpulan: Imputasi Median dipilih** — unggul di semua metrik, terutama AUC-ROC 0.91.

**Best params hasil tuning (berlaku untuk kedua pendekatan):**
```python
{'subsample': 1.0, 'n_estimators': 300, 'min_child_weight': 1,
 'max_depth': 8, 'learning_rate': 0.2, 'colsample_bytree': 0.8}
```

---

## Standar Kualitas ML

- **Hyperparameter Tuning** — wajib RandomizedSearchCV, bukan nilai default
- **Cross-Validation** — wajib k-fold
- **Early Stopping** — `early_stopping_rounds=20`, `eval_metric='aucpr'`
- **Cek Overfitting** — selalu bandingkan score train vs test
- **Metrik lengkap** — Accuracy, Precision, Recall, F1, AUC-ROC, Confusion Matrix
- **SHAP** — wajib untuk interpretabilitas, bukan hanya feature importance biasa
- **Data Leakage** — selalu periksa sebelum training

---

## Aturan Penting

- **Jangan confirmation bias** — jangan membenarkan pilihan model tanpa bukti perbandingan objektif
- **Urutan perubahan:** notebook → app.py → HTML (jika perlu). Jangan mulai dari HTML
- **Fitur waktu** (`bulan`, `jam`) wajib dibuat dari `df` asli sebelum `dropna()` untuk menghindari index mismatch
- **Kolom `mag` dilarang sebagai fitur** — data leakage
- **Setiap ganti skema label** di notebook wajib diikuti update `app.py`
- **JANGAN langsung edit notebook (.ipynb)** — user adalah mahasiswa TA yang harus bisa presentasikan perubahannya sendiri. Cukup jelaskan apa yang perlu diubah dan tunjukkan kode yang harus ditulis, biarkan user yang mengetik dan menjalankan sendiri
- **app.py boleh diedit langsung** — user mengizinkan perubahan langsung pada app.py

---

## Struktur File

```
TUGAS AKHIR/
├── data/
│   ├── gempa_1990-2026.csv      ← dataset utama
│   └── points.json              ← untuk heatmap
├── Anomaly Detection/
│   ├── XGBoost.ipynb            ← anomaly detection ✅ selesai
│   ├── XGBoost_solo.ipynb       ← versi latihan mandiri user
│   ├── shap_importance.png      ← SHAP bar chart ✅
│   ├── shap_beeswarm.png        ← SHAP beeswarm ✅
│   └── visualisasi_IF.png       ← simulasi cara kerja IF ✅
├── XGBoost.ipynb                ← klasifikasi tingkat bahaya
├── perbandingan.ipynb           ← perbandingan drop kolom vs imputasi
├── app.py                       ← Flask REST API (port 5000)
├── model_gempa.pkl              ← model klasifikasi
├── model_anomali.pkl            ← model anomaly detection ✅
├── scaler_anomali.pkl           ← scaler anomaly detection ✅
├── map.html
├── heatmap.html
└── prediksi.html
```

---

## Instalasi

```
pip install pandas numpy matplotlib seaborn xgboost scikit-learn flask joblib shap
```

Server prediksi: `python app.py` → buka `http://127.0.0.1:5000/prediksi.html`

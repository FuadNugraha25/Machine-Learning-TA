# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

Tugas Akhir Sistem Informasi — pengembangan fitur Machine Learning untuk aplikasi mobile mitigasi bencana gempa bumi Indonesia, berbasis data USGS 1990–2026. Dikerjakan secara berkelompok.

**Fokus utama adalah Machine Learning (notebook & model), bukan HTML.** HTML hanya alat bantu visualisasi dan tidak boleh jadi prioritas perubahan kecuali diminta eksplisit oleh user.

User ingin implementasi **selengkap dan sedetail mungkin** — tidak ada batasan kesulitan.

---

## Identitas Project

- **Judul:** Deteksi Anomali Gempa Bumi Indonesia Menggunakan Kombinasi Isolation Forest dan XGBoost dengan Pendekatan Imputasi Median
- **Topik:** Mitigasi Bencana
- **Machine Learning:** XGBoost (dengan Isolation Forest sebagai label generator)
- **Variable Feature:** Latitude, Longitude, Depth, Gap, Dmin, NST, Bulan, Jam
- **Variable Target:** Status Anomali Gempa (Normal / Anomali) — label dibuat otomatis oleh Isolation Forest dari 63.414 data historis USGS 1990–2026, contamination 5% mengacu proporsi kejadian ekstrem yang umum di penelitian deteksi anomali seismik

## Pembagian Tugas Kelompok

- **User (pemilik repo ini):** Fokus utama **Anomaly Detection** (Isolation Forest → XGBoost). Klasifikasi tingkat bahaya (XGBoost.ipynb) hanya sebagai pendukung/pembanding.
- **Anggota lain:** Deteksi anomali menggunakan Isolation Forest murni (file referensi: `earthquake_anomaly_detection_agent_prompt.md`)

---

## Dataset

- **File aktif:** `data/gempa_1990-2026.csv` — 63.414 baris, gabungan 7 file per periode
- **File lama (tidak dipakai lagi):** `data/gempa_1990-2019.csv` — sudah dihapus
- **Sumber:** USGS Earthquake Catalog
- **Kolom fitur yang dipakai:** `latitude`, `longitude`, `depth`, `gap`, `dmin`, `nst`, `bulan`, `jam`
- **Kolom bermasalah:** `gap` (15.615+ kosong), `dmin` (37.251+ kosong), `nst` (25.356+ kosong) — nilai kosong karena keterbatasan infrastruktur sensor era 1990-an, bukan data tidak valid
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
Model mendeteksi anomali berdasarkan **kombinasi fitur yang tidak biasa** dibanding pola historis — bukan magnitude. Gempa besar belum tentu anomali. Anomali = gempa yang koordinat/depth/gap/dmin/nst-nya tidak umum secara historis.

### Status
- ✅ Model selesai — model_anomali.pkl, scaler_anomali.pkl tersimpan
- ✅ Contamination 0.05 dipilih (3.171 anomali dari 63.414 data)
- ✅ anomali.html selesai (4 tab: Input Manual, Gempa Historis, Dashboard, Timeline)
- ✅ dashboard.json dan timeline.json di-generate
- ⏳ Keputusan: masukkan kolom mag sebagai fitur atau tidak?
- ⏳ SHAP analysis

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
│   └── XGBoost.ipynb            ← anomaly detection (sedang dikerjakan)
├── XGBoost.ipynb                ← klasifikasi tingkat bahaya
├── perbandingan.ipynb           ← perbandingan drop kolom vs imputasi
├── app.py                       ← Flask REST API (port 5000)
├── model_gempa.pkl              ← model klasifikasi
├── model_anomali.pkl            ← model anomaly detection (belum ada)
├── scaler_anomali.pkl           ← scaler anomaly detection (belum ada)
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

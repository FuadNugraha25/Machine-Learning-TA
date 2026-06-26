# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

Tugas Akhir Sistem Informasi — pengembangan deteksi anomali seismisitas menggunakan algoritma Machine Learning (Isolation Forest) berbasis data historis BMKG 2008-2026.

---

## Identitas Project

- **Fokus Utama:** Deteksi Anomali Gempa Bumi Indonesia Menggunakan Isolation Forest Murni (Unsupervised).
- **Machine Learning:** Isolation Forest (XGBoost dan pendekatan klasifikasi/SHAP dibatalkan/tidak dipakai untuk eksperimen ini).
- **Variable Feature:** `mag`, `depth`, `latitude`, `longitude`.
- **Variable Target:** Status Anomali Gempa (`0` = Normal, `1` = Anomali) — label dibuat otomatis oleh Isolation Forest dengan nilai *contamination* 0.005 (0.5%).

---

## Dataset

- **File Aktif:** `data/bmkg/gabungan_2008_2026.csv`
- **Data Preparation:** 
  - Filter koordinat *bounding box* Indonesia (Latitude: -11.0 s/d 6.0, Longitude: 95.0 s/d 141.0).
  - Menghapus semua baris yang memiliki nilai kosong (`dropna()`).
  - Total data akhir setelah filter dan pembersihan: 131.117 baris.
- **Standarisasi:** Menggunakan `StandardScaler` sebelum dimasukkan ke model Isolation Forest.

---

## Anomaly Detection (Fokus Saat Ini: Anomaly Detection BMKG/isolation_forest.ipynb)

### Pendekatan
- Menggunakan **Isolation Forest murni** (unsupervised) untuk mendeteksi anomali dari data historis BMKG.
- Parameter Isolation Forest: `contamination=0.005`, `random_state=42`.
- Fitur yang dipakai untuk training: `['mag', 'depth', 'latitude', 'longitude']`. (Fitur `mag` mutlak dimasukkan dalam analisis anomali ini).
- Label bawaan Isolation Forest (`1` dan `-1`) dikonversi ke format klasifikasi biner standar:
  - `0` = Normal (awalnya 1)
  - `1` = Anomali (awalnya -1)

### Output Eksperimen
- Menghasilkan file dataset baru beserta penambahan kolom `anomaly_score` dan `anomaly_label` yang disimpan di: `Anomaly Detection BMKG/dataset_dengan_anomali.csv`.
- Ekstraksi wawasan melalui analisis korelasi (khusus pada data anomali) dan visualisasi komparatif (boxplot) antara data Normal dan Anomali.
- Menyimpan model final Isolation Forest dengan nama: `isolation_forest_bmkg.pkl`. *(Catatan: cell yang mencoba menyimpan model XGBoost di notebook tersebut hanyalah sisa boilerplate/error handling, karena XGBoost mutlak tidak dilatih/dipakai).*

---

## Aturan Penting

- **Gaya Komunikasi Kritis & Edukatif:** Selalu jawab pertanyaan konseptual secara komprehensif, logis, dan didukung analogi yang mudah dipahami. Jangan sekadar membenarkan argumen user atau mengikuti perintah secara buta. Jika ada miskonsepsi (misal dari dosen/teori), berikan bantahan/argumen akademis yang solid dan terstruktur.
- **Jangan confirmation bias:** Jangan membenarkan pilihan model tanpa bukti perbandingan objektif.
- **Aturan mengedit notebook (.ipynb):** Secara *default*, JANGAN langsung edit file notebook. Cukup jelaskan apa yang perlu diubah dan berikan kode agar user yang memasukkannya sendiri. **PENGECUALIAN:** Anda HANYA diizinkan mengedit file notebook secara langsung jika user yang meminta secara eksplisit.
- **Kesesuaian Kode:** Semua pengerjaan ML mengenai gempa harus **berpedoman mutlak** pada file `Anomaly Detection BMKG/isolation_forest.ipynb`. Segala aturan atau pendekatan lama (seperti XGBoost, analisis SHAP, larangan pemakaian fitur `mag`, imputasi median, dll) sudah usang dan dibatalkan.
- **Kesesuaian Template Laporan:** Selalu patuhi standar penulisan (template) laporan atau proposal Tugas Akhir. Gambar/Visualisasi harus diletakkan relevan di tengah teks, dan panjang pembahasan bab (seperti Latar Belakang) harus proporsional untuk standar akademis (tidak boleh terlalu singkat).
- **Aturan Membaca Laporan:** Jika user meminta Anda melihat/membaca bagian tertentu (contoh: sub-bab 2.2), Anda WAJIB membaca bagian tersebut beserta bagian-bagian SEBELUMNYA (seperti 2.1 atau bahkan Bab 1 sepenuhnya) untuk memastikan pemahaman konteks secara utuh. Anda DILARANG KERAS melihat atau merujuk ke bagian setelahnya (seperti 2.3, Bab 3, dan seterusnya) kecuali diminta secara eksplisit.

---

## Struktur File Utama

```text
TUGAS AKHIR/
├── data/
│   └── bmkg/
│       └── gabungan_2008_2026.csv        ← dataset historis BMKG
├── Anomaly Detection BMKG/               ← FOKUS SAAT INI
│   ├── isolation_forest.ipynb            ← notebook utama eksperimen IF
│   ├── isolation_forest_bmkg.pkl         ← model final hasil training IF
│   └── dataset_dengan_anomali.csv        ← output hasil anomali dari IF
└── CLAUDE.md
```

---

## Dokumen Laporan (Word)

Lokasi file laporan utama yang dapat diedit secara otomatis:
- `C:\Users\Fuad Nugraha\Documents\Laporan Tugas Akhir\Tugas Akhir Semester 8 AI.docx`

**ATURAN WAJIB MENGEDIT WORD:**
1. JANGAN PERNAH mengedit file Word tersebut secara lokal di disk (misal: menggunakan `python-docx` atau memanipulasi file zip) karena file ini sering dibiarkan terbuka oleh user, sehingga akan menghasilkan error `Permission Denied`.
2. SELALU gunakan **COM Automation secara live** (misal: dengan skrip Python via library `win32com.client`). 
3. Anda harus menulis skrip Python dengan `win32com.client.Dispatch("Word.Application")` dan mencari dokumen yang sedang terbuka di `word.Documents`.
4. Dengan cara ini, user dapat melihat perubahannya secara langsung secara "live" tanpa perlu menutup aplikasinya.
5. Setelah skrip Python yang dibuat (misalnya di folder `scratch/`) selesai dieksekusi untuk membaca atau mengedit Word, skrip tersebut WAJIB langsung dihapus agar file tidak menumpuk.

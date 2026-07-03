import win32com.client
import sys

def insert_heading(selection, text, level):
    selection.Style = f"Heading {level}"
    selection.TypeText(text)
    selection.TypeParagraph()

def insert_normal(selection, text):
    selection.Style = "Normal"
    selection.TypeText(text)
    selection.TypeParagraph()

def main():
    try:
        word = win32com.client.Dispatch("Word.Application")
        target_doc = None
        for doc in word.Documents:
            if "Tugas Akhir Semester 8 AI" in doc.Name:
                target_doc = doc
                break
                
        if not target_doc:
            print("Dokumen tidak ditemukan.")
            return
            
        paragraphs = target_doc.Paragraphs
        start_idx = -1
        end_idx = -1
        
        # Find start of Isolation Forest and end (State of Art)
        for i in range(1, paragraphs.Count + 1):
            try:
                text = paragraphs(i).Range.Text.strip().upper()
                if "ISOLATION FOREST" in text and paragraphs(i).Style.NameLocal.startswith("Heading 2"):
                    start_idx = i
                elif "STATE OF ART" in text and paragraphs(i).Style.NameLocal.startswith("Heading 2") and start_idx != -1:
                    end_idx = i
                    break
            except:
                pass
                
        if start_idx != -1 and end_idx != -1:
            print(f"Mengganti BAB 2.5 dan 2.6 dari paragraf {start_idx} sampai {end_idx - 1}")
            start_pos = paragraphs(start_idx).Range.Start
            end_pos = paragraphs(end_idx - 1).Range.End
            
            selection = target_doc.ActiveWindow.Selection
            selection.SetRange(start_pos, end_pos)
            selection.Delete()
            
            # Now insert the new content
            # Bab 2.5
            insert_heading(selection, "Isolation Forest", 2)
            insert_heading(selection, "Konsep Dasar Isolation Forest", 3)
            insert_normal(selection, "Isolation Forest adalah algoritma unsupervised learning yang dikembangkan khusus untuk mendeteksi anomali. Berbeda dengan mayoritas algoritma klasifikasi yang mencoba membangun model dari data normal lalu mencari penyimpangannya, Isolation Forest bekerja dengan cara langsung mengisolasi anomali. Algoritma ini berlandaskan pada dua karakteristik utama anomali: jumlahnya yang sangat sedikit (minoritas) dan nilai atributnya yang berbeda secara signifikan dari observasi populasi normal.")
            
            insert_heading(selection, "Algoritma Partisi dan Perhitungan Anomaly Score", 3)
            insert_normal(selection, "Isolation Forest menggunakan struktur data berbasis pohon (Isolation Trees atau iTrees). Proses pembentukan pohon dilakukan dengan memilih fitur secara acak, lalu memilih nilai pemisah (split value) secara acak di antara nilai minimum dan maksimum dari fitur tersebut. Karena anomali memiliki nilai yang ekstrem atau berbeda dari data mayoritas, data anomali akan terisolasi lebih cepat (berada lebih dekat dengan akar pohon) dibandingkan data normal yang memerlukan banyak partisi berulang untuk dipisahkan. Tingkat anomali (anomaly score) pada akhirnya dihitung berdasarkan rata-rata panjang lintasan (path length) dari akar hingga daun pada seluruh kumpulan pohon (forest).")
            
            insert_heading(selection, "Isolation Forest dalam Analisis Data Seismik", 3)
            insert_normal(selection, "Dalam konteks pemrosesan data seismik historis BMKG, Isolation Forest sangat relevan karena data rekaman gempa bumi pada umumnya tidak memiliki label ground truth (tidak berlabel) yang secara eksplisit membedakan antara gempa normal dan anomali. Algoritma ini dirancang secara otomatis untuk menyeleksi dan memetakan kejadian seismik yang memiliki kombinasi anomali secara multivariat, baik dari segi magnitudo, kedalaman, maupun kluster spasial (koordinat latitude dan longitude) yang tidak lazim.")
            
            insert_heading(selection, "Kelebihan dan Kekurangan Isolation Forest", 3)
            insert_normal(selection, "Kelebihan utama dari algoritma Isolation Forest adalah efisiensi komputasi yang sangat tinggi dengan penggunaan memori yang rendah, skalabilitas yang mumpuni pada dataset masif berdimensi tinggi, serta kemampuannya beroperasi tanpa memerlukan fase pelabelan data (unsupervised). Meskipun demikian, kelemahan utamanya adalah algoritma ini sangat bergantung pada asumsi rasio kontaminasi (contamination rate) yang seringkali harus ditentukan secara empiris oleh pengguna, serta berpotensi kurang akurat jika dataset dipenuhi oleh variasi kepadatan kluster (local anomalies) yang tidak seragam.")

            # Bab 2.6
            insert_heading(selection, "Evaluasi Model Deteksi Anomali", 2)
            insert_heading(selection, "Analisis Distribusi Anomaly Score", 3)
            insert_normal(selection, "Karena pendekatan unsupervised learning tidak menyediakan label data aktual (ground truth), mekanisme evaluasi performa model konvensional seperti akurasi (accuracy), recall, atau confusion matrix tidak dapat diterapkan. Evaluasi model dalam konteks ini difokuskan pada analisis distribusi probabilitas atau persebaran anomaly score yang dihasilkan oleh model. Evaluasi ini bertujuan untuk memvalidasi pemisahan antara populasi data normal dengan anomali, serta untuk menentukan batas ambang (threshold) klasifikasi yang optimal secara matematis.")
            
            insert_heading(selection, "Visualisasi Komparatif", 3)
            insert_normal(selection, "Teknik visualisasi memainkan peran krusial dalam memvalidasi hasil deteksi anomali pada data tanpa label. Penggunaan grafik spasial (seperti pemetaan latitude dan longitude) serta plot distribusi komparatif (misalnya boxplot atau histogram) digunakan untuk membandingkan persebaran fitur antara kelompok normal dan anomali. Melalui analisis komparatif ini, analis dapat memperoleh konfirmasi visual bahwa model berhasil mengisolasi dan mendeteksi karakteristik kejadian gempa yang tidak wajar sesuai dengan kaidah seismologi.")
            
            insert_heading(selection, "Interpretasi Hasil Deteksi untuk Informasi Mitigasi", 3)
            insert_normal(selection, "Pada tahap akhir, seluruh hasil komputasi dan pemetaan dari Isolation Forest diterjemahkan menjadi wawasan analitik praktis. Anomali seismik yang terdeteksi tidak hanya dipandang sebagai outlier data, melainkan diinterpretasikan sebagai indikator geofisika. Informasi anomali ini selanjutnya diintegrasikan secara langsung ke dalam backend Aplikasi AMANIN untuk menyajikan notifikasi serta peringatan tingkat lanjut kepada masyarakat di kawasan rawan, sehingga mendukung sistem peringatan dini (early warning) dan mitigasi bencana yang proaktif berbasis kecerdasan buatan.")
            
            print("Berhasil memasukkan teks Bab 2.5 dan 2.6 baru.")
        else:
            print(f"Gagal menemukan batas: start_idx={start_idx}, end_idx={end_idx}")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

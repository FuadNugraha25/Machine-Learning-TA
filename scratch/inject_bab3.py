import win32com.client
import sys

def replace_in_doc(target_doc, find_text, replace_text):
    search_range = target_doc.Content
    search_range.Find.ClearFormatting()
    search_range.Find.Replacement.ClearFormatting()
    search_range.Find.Text = find_text
    search_range.Find.Replacement.Text = replace_text
    search_range.Find.MatchCase = False
    
    # 2 = wdReplaceAll
    search_range.Find.Execute(Replace=2)

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
            
        print("Melakukan Find & Replace di BAB 3...")
        
        # Replacements for Bab 3
        # 1. Paragraf 780
        replace_in_doc(target_doc, 
            "Pengolahan data dilakukan dengan memanfaatkan metode machine learning menggunakan model Logistic Regression.",
            "Pengolahan data dilakukan dengan memanfaatkan algoritma unsupervised learning menggunakan model Isolation Forest."
        )
        replace_in_doc(target_doc, 
            "Model ini digunakan untuk menghasilkan estimasi probabilitas dampak guncangan gempa berdasarkan parameter gempa yang tersedia.",
            "Model ini digunakan untuk mendeteksi kejadian gempa anomali berdasarkan kombinasi parameter gempa (seperti magnitudo, kedalaman, dan koordinat spasial)."
        )
        replace_in_doc(target_doc, 
            "Pemilihan Logistic Regression didasarkan pada kemampuannya dalam menghasilkan keluaran berupa probabilitas yang relatif mudah diinterpretasikan dan sesuai dengan tujuan sistem mitigasi yang berorientasi pada pemahaman pengguna.",
            "Pemilihan Isolation Forest didasarkan pada efisiensinya dalam menangani data tidak berlabel (unlabeled) serta kemampuannya mengisolasi karakteristik seismik yang berbeda dari pola mayoritas."
        )
        
        # 2. Paragraf 784
        replace_in_doc(target_doc,
            "Evaluasi model prediksi dilakukan secara terbatas menggunakan confusion matrix untuk memperoleh gambaran umum mengenai kemampuan model dalam menghasilkan klasifikasi probabilitas dampak guncangan gempa.",
            "Evaluasi model deteksi anomali difokuskan pada analisis distribusi anomaly score dan sebaran komparatif menggunakan visualisasi boxplot dan pemetaan spasial."
        )
        
        # 3. Paragraf 794
        replace_in_doc(target_doc,
            "Data sekunder ini digunakan sebagai masukan dalam pengembangan modul prediksi probabilitas dampak guncangan gempa.",
            "Data sekunder ini digunakan sebagai masukan utama dalam pengembangan modul deteksi anomali kegempaan."
        )
        replace_in_doc(target_doc,
            "Data sekunder tidak digunakan untuk memprediksi kejadian gempa, melainkan untuk mendukung penyajian estimasi probabilitas dampak sebagai bagian dari sistem mitigasi.",
            "Data sekunder tidak digunakan untuk memprediksi probabilitas dampak, melainkan untuk melatih model Isolation Forest dalam mengidentifikasi kejadian gempa bumi yang tidak biasa (anomali) sebagai bentuk mitigasi non-struktural."
        )
        
        # 4. Paragraf 799
        replace_in_doc(target_doc,
            "Model Logistic Regression dipilih sebagai metode analitik pendukung dalam sistem karena kemampuannya menghasilkan keluaran berupa probabilitas yang relatif mudah diinterpretasikan.",
            "Model Isolation Forest dipilih sebagai algoritma analitik pendukung dalam sistem karena efektivitasnya mendeteksi anomali pada data berdimensi tinggi tanpa memerlukan pelabelan manual (ground truth)."
        )
        replace_in_doc(target_doc,
            "Struktur model Logistic Regression yang sederhana dan transparan juga memungkinkan hasil prediksi dijelaskan secara konseptual",
            "Sifat Isolation Forest yang berbasis partisi acak juga memungkinkan hasil deteksi dijelaskan secara logis"
        )
        
        # 5. Paragraf 800
        replace_in_doc(target_doc,
            "pemilihan Logistic Regression didasarkan pada kesesuaian metode dengan tujuan sistem",
            "pemilihan Isolation Forest didasarkan pada kesesuaian algoritma dengan sifat data seismik yang masif dan tidak berlabel, serta kebutuhan analisis anomali"
        )
        
        print("Selesai melakukan perubahan di BAB 3.")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

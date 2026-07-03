import win32com.client
import sys

def replace_section(doc, start_heading, end_heading, new_text):
    start_para = None
    end_para = None
    
    in_toc = True
    paragraphs = doc.Paragraphs
    count = paragraphs.Count
    
    for i in range(1, count + 1):
        text = paragraphs(i).Range.Text.strip()
        if in_toc and "TINJAUAN PUSTAKA" in text and i > 50:
            in_toc = False
            
        if not in_toc:
            if start_heading in text and "\t" not in text:
                start_para = i
            elif start_para is not None and (end_heading in text or (end_heading == "II.4" and text.startswith("II.4"))) and "\t" not in text:
                end_para = i
                break
                
    if start_para and end_para:
        print(f"Found '{start_heading}' at para {start_para} and '{end_heading}' at para {end_para}")
        
        # Delete old paragraphs (backwards)
        deleted_count = 0
        for i in range(end_para - 1, start_para, -1):
            # Also check if we are not deleting other headings accidentally (just in case)
            p_text = paragraphs(i).Range.Text.strip()
            # print(f"Deleting: {p_text[:30]}...")
            paragraphs(i).Range.Delete()
            deleted_count += 1
            
        print(f"Deleted {deleted_count} old paragraphs.")
            
        # Insert new text
        rng = paragraphs(start_para).Range
        rng.Collapse(0) # Collapse to end of the heading paragraph
        rng.Text = "\r" + new_text
        print(f"Successfully updated section under '{start_heading}'")
    else:
        print(f"Could not find section '{start_heading}' to '{end_heading}'")
        print(f"start_para: {start_para}, end_para: {end_para}")

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
            
        # Texts
        text_231 = (
            "Gempa bumi merupakan fenomena alam yang memiliki spektrum variabilitas yang sangat luas, baik dari segi mekanisme pelepasan energi, sebaran spasial, maupun pola temporalnya. Dalam konteks seismologi observasional dan mitigasi kebencanaan, perhatian sering kali hanya tertuju pada gempa bumi dengan magnitudo besar yang berpotensi merusak. Namun, dari perspektif analisis data dan pemodelan statistik, kejadian seismik tidak hanya dievaluasi berdasarkan dampak kerusakannya, melainkan juga dari karakteristik kemunculannya. Di sinilah konsep \"anomali\" menjadi krusial. Anomali dalam konteks seismologi tidak secara kaku diartikan sebagai gempa bumi besar, melainkan sebagai kejadian seismik yang memiliki profil atau karakteristik yang menyimpang secara signifikan dari pola historis mayoritas kejadian di suatu wilayah tektonik tertentu (Mousavi & Beroza, 2025).\n"
            "Penyimpangan ini dapat bermanifestasi dalam berbagai bentuk multidimensi. Sebagai contoh, suatu gempa dengan magnitudo menengah dapat diklasifikasikan sebagai anomali apabila terjadi pada tingkat kedalaman hiposenter yang sangat ekstrem di zona yang secara historis hanya didominasi oleh gempa dangkal. Demikian pula, gempa bumi yang berpusat di titik koordinat (garis lintang dan bujur) yang secara geologis dikenal sebagai zona tenang atau seismic gap akan dianggap sebagai kejadian tidak lazim. Identifikasi kejadian anomali ini memiliki urgensi akademis dan praktis yang tinggi. Kejadian seismik dengan profil yang terisolasi dari pola umum sering kali mengindikasikan adanya pelepasan tegangan tektonik yang tidak biasa, pergeseran struktur sesar yang belum terpetakan, atau fenomena geofisika lain yang membutuhkan investigasi lebih lanjut oleh para analis seismologi. Oleh karena itu, mendeteksi anomali gempa bumi adalah langkah esensial untuk memahami dinamika blind-spots dalam sistem pemantauan seismik."
        )
        
        text_232 = (
            "Pertumbuhan eksponensial volume data historis gempa bumi yang dicatat oleh jaringan sensor seismik modern (seperti yang dihimpun oleh BMKG maupun USGS) membuat proses identifikasi pola-pola tidak lazim secara manual menjadi mustahil. Untuk mengatasi tantangan komputasional ini, algoritma Machine Learning, khususnya cabang anomaly detection (deteksi anomali), diterapkan sebagai pendekatan analitik tingkat lanjut. Deteksi anomali bertujuan untuk menemukan observasi atau data points yang menyimpang secara ekstrem dari mayoritas kumpulan data normal, sedemikian rupa sehingga observasi tersebut dicurigai dihasilkan oleh mekanisme yang berbeda.\n"
            "Dalam analisis data seismik, deteksi anomali digunakan untuk memisahkan gempa bumi dengan profil karakteristik wajar—yaitu gempa yang mematuhi hukum empiris seismologi seperti distribusi Gutenberg-Richter dan berpusat di jalur subduksi mayor—dengan gempa yang memiliki profil menyimpang. Berbeda dengan pendekatan Supervised Learning yang membutuhkan label kelas (seperti \"berbahaya\" atau \"aman\") yang mutlak dan pasti, deteksi kejadian anomali gempa di dunia nyata dihadapkan pada masalah ketiadaan ground-truth atau batasan yang jelas mengenai apa yang mutlak disebut anomali. Oleh karena itu, pendekatan Unsupervised Learning menjadi pilihan yang jauh lebih rasional dan objektif. Melalui metode tanpa pengawasan ini, sistem tidak \"diajari\" dari label buatan manusia, melainkan secara algoritmis mengukur jarak, kerapatan, atau seberapa \"terisolasi\" sebuah kejadian gempa dari ribuan kejadian historis lainnya di ruang fitur berdimensi tinggi. Hal ini menjadikan deteksi anomali sebagai instrumen eksploratif yang objektif untuk menemukan karakteristik kejadian gempa yang secara statistik benar-benar outlier."
        )
        
        text_233 = (
            "Keberhasilan dan validitas model Unsupervised Anomaly Detection sangat bergantung pada pemilihan variabel dasar (fitur) yang digunakan untuk merepresentasikan setiap kejadian gempa bumi. Agar model dapat mendeteksi kejanggalan profil secara komprehensif tanpa terjebak pada bias subjektif, diperlukan parameter fundamental yang secara universal merepresentasikan dimensi energi dan dimensi spasiotemporal kejadian seismik. Dalam analisis ini, penentuan status anomali difokuskan pada kombinasi dari empat variabel kuantitatif utama: Magnitudo (mag), Kedalaman (depth), Garis Lintang (latitude), dan Garis Bujur (longitude).\n"
            "Keempat variabel ini dipilih karena sifatnya yang saling mengikat dalam mendeskripsikan anatomi sebuah gempa. Magnitudo merepresentasikan estimasi ukuran absolut energi seismik yang dilepaskan pada saat rekahan terjadi. Sementara itu, kedalaman merepresentasikan posisi vertikal hiposenter di dalam struktur litosfer, yang secara langsung berkaitan dengan jenis interaksi lempeng tektonik (misalnya zona subduksi dangkal, menengah, atau dalam). Lebih lanjut, garis lintang dan bujur menetapkan titik absolut episenter di permukaan bumi, yang menempatkan kejadian gempa pada konteks geografi seismik wilayah Indonesia.\n"
            "Algoritma deteksi anomali yang andal, seperti Isolation Forest, tidak mengevaluasi keempat variabel ini secara linier maupun parsial, melainkan mengevaluasi interaksi non-linier dari kombinasi keempatnya secara simultan. Sebagai contoh empiris, sebuah gempa dengan magnitudo 4.5 mungkin merupakan kejadian rutin dan diklasifikasikan sebagai \"normal\" apabila terjadi di kedalaman 10 km pada koordinat jalur subduksi selatan Jawa. Namun, magnitudo yang persis sama dapat dideteksi dengan skor anomali (anomaly score) yang sangat tinggi apabila terjadi di kedalaman 600 km pada koordinat yang secara historis tidak pernah dilanda gempa dalam. Dengan demikian, status anomali sebuah gempa adalah hasil dari evaluasi profil multi-dimensi, yang menjadikan kombinasi magnitudo, kedalaman, dan koordinat sebagai variabel penentu utama yang tidak dapat dipisahkan."
        )
        
        print("--- Memperbarui II.3.1 ---")
        replace_section(doc=target_doc, 
                        start_heading="II.3.1 Konsep Anomali dalam Konteks Seismologi", 
                        end_heading="II.3.2 Deteksi Anomali sebagai Pendekatan Analisis", 
                        new_text=text_231)
                        
        print("--- Memperbarui II.3.2 ---")
        replace_section(doc=target_doc, 
                        start_heading="II.3.2 Deteksi Anomali sebagai Pendekatan Analisis", 
                        end_heading="II.3.3 Variabel Penentu Status Anomali", 
                        new_text=text_232)
                        
        print("--- Memperbarui II.3.3 ---")
        replace_section(doc=target_doc, 
                        start_heading="II.3.3 Variabel Penentu Status Anomali", 
                        end_heading="II.4", 
                        new_text=text_233)
            
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

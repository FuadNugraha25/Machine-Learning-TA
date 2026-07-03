import win32com.client
import sys

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
            
        print("Mencari heading II.3.3...")
        
        content = target_doc.Content
        find = content.Find
        find.ClearFormatting()
        
        # Search for the start heading
        find.Text = "II.3.3"
        find.Forward = True
        find.Wrap = 0 # wdFindStop
        
        start_pos = -1
        # Skip the first occurrence if it's in the TOC. We do this by searching from the start,
        # but to be sure we skip TOC, we can search for the text "TINJAUAN PUSTAKA" first, 
        # then set the start range to after it.
        
        find_toc_end = target_doc.Content.Find
        find_toc_end.Execute("TINJAUAN PUSTAKA")
        if find_toc_end.Found:
            search_range = target_doc.Range(find_toc_end.Parent.End, target_doc.Content.End)
        else:
            search_range = target_doc.Content
            
        # Now search for the heading in the search_range
        search_range.Find.Execute("Variabel Penentu Status Anomali (Magnitudo, Kedalaman, dan Koordinat)")
        if not search_range.Find.Found:
            print("Gagal menemukan heading II.3.3")
            return
            
        rng = search_range.Paragraphs(1).Range
        rng.Collapse(0) # 0 = wdCollapseEnd
        
        new_text = (
            "Keberhasilan dan validitas model Unsupervised Anomaly Detection sangat bergantung pada pemilihan variabel dasar (fitur) yang digunakan untuk merepresentasikan setiap kejadian gempa bumi. Agar model dapat mendeteksi kejanggalan profil secara komprehensif tanpa terjebak pada bias subjektif, diperlukan parameter fundamental yang secara universal merepresentasikan dimensi energi dan dimensi spasiotemporal kejadian seismik. Dalam analisis ini, penentuan status anomali difokuskan pada kombinasi dari empat variabel kuantitatif utama: Magnitudo (mag), Kedalaman (depth), Garis Lintang (latitude), dan Garis Bujur (longitude).\n\n"
            "Keempat variabel ini dipilih karena sifatnya yang saling mengikat dalam mendeskripsikan anatomi sebuah gempa. Magnitudo merepresentasikan estimasi ukuran absolut energi seismik yang dilepaskan pada saat rekahan terjadi. Sementara itu, kedalaman merepresentasikan posisi vertikal hiposenter di dalam struktur litosfer, yang secara langsung berkaitan dengan jenis interaksi lempeng tektonik (misalnya zona subduksi dangkal, menengah, atau dalam). Lebih lanjut, garis lintang dan bujur menetapkan titik absolut episenter di permukaan bumi, yang menempatkan kejadian gempa pada konteks geografi seismik wilayah Indonesia.\n\n"
            "Algoritma deteksi anomali yang andal, seperti Isolation Forest, tidak mengevaluasi keempat variabel ini secara linier maupun parsial, melainkan mengevaluasi interaksi non-linier dari kombinasi keempatnya secara simultan. Sebagai contoh empiris, sebuah gempa dengan magnitudo 4.5 mungkin merupakan kejadian rutin dan diklasifikasikan sebagai \"normal\" apabila terjadi di kedalaman 10 km pada koordinat jalur subduksi selatan Jawa. Namun, magnitudo yang persis sama dapat dideteksi dengan skor anomali (anomaly score) yang sangat tinggi apabila terjadi di kedalaman 600 km pada koordinat yang secara historis tidak pernah dilanda gempa dalam. Dengan demikian, status anomali sebuah gempa adalah hasil dari evaluasi profil multi-dimensi, yang menjadikan kombinasi magnitudo, kedalaman, dan koordinat sebagai variabel penentu utama yang tidak dapat dipisahkan.\n"
        )
        
        rng.Text = "\r" + new_text
        print("Berhasil memasukkan isi paragraf di bawah II.3.3.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

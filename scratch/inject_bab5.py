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
        
        # Find DAFTAR PUSTAKA
        for i in range(1, paragraphs.Count + 1):
            try:
                text = paragraphs(i).Range.Text.strip().upper()
                if "DAFTAR PUSTAKA" in text and ("Heading 1" in paragraphs(i).Style.NameLocal or "Judul" in paragraphs(i).Style.NameLocal):
                    start_idx = i
                    break
            except:
                pass
                
        if start_idx != -1:
            print(f"Menambahkan BAB V sebelum paragraf {start_idx}")
            start_pos = paragraphs(start_idx).Range.Start
            
            selection = target_doc.ActiveWindow.Selection
            selection.SetRange(start_pos, start_pos)
            
            # Bab 5
            insert_heading(selection, "KESIMPULAN DAN SARAN", 1)
            insert_heading(selection, "Kesimpulan", 2)
            insert_normal(selection, "Berdasarkan hasil pengolahan data historis gempa bumi BMKG periode 2008-2026 menggunakan algoritma unsupervised learning Isolation Forest, dapat ditarik kesimpulan bahwa model mampu mengisolasi dan mendeteksi kejadian gempa anomali berdasarkan kombinasi parameter geofisika secara otomatis tanpa membutuhkan label ground truth. Integrasi hasil deteksi ini ke dalam Aplikasi AMANIN juga telah berhasil dikembangkan, sehingga masyarakat dapat memperoleh peringatan dini secara informatif mengenai gempa dengan karakteristik tidak wajar.")
            
            insert_heading(selection, "Saran", 2)
            insert_normal(selection, "Untuk pengembangan sistem di masa mendatang, disarankan untuk melakukan eksplorasi penambahan parameter fitur geofisika sekunder (seperti jenis patahan atau data percepatan tanah) guna memperkaya dimensi deteksi anomali. Selain itu, tuning rasio kontaminasi secara dinamis berbasis kluster wilayah dapat diteliti lebih lanjut untuk meningkatkan ketepatan deteksi anomali spasial.")
            
            print("Berhasil memasukkan teks Bab 5.")
        else:
            print(f"Gagal menemukan batas: start_idx={start_idx}")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

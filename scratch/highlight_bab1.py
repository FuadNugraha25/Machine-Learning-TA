import win32com.client
import sys

def highlight_text(target_doc, text_to_find, color_index):
    search_range = target_doc.Content
    search_range.Find.ClearFormatting()
    search_range.Find.Text = text_to_find
    search_range.Find.MatchCase = False
    
    count = 0
    # Execute loop
    while search_range.Find.Execute(text_to_find):
        search_range.HighlightColorIndex = color_index
        count += 1
        # Collapse to end so we don't find the same text again
        search_range.Collapse(0) # wdCollapseEnd = 0
        
    print(f"Highlighted '{text_to_find[:30]}...' : {count} kali.")

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
            
        print("Mulai menghighlight dokumen...")
        
        # wdYellow = 7 (Masalah Nyata)
        highlight_text(target_doc, "Di dalam ribuan rekaman gempa biasa, sering kali tersembunyi kejadian-kejadian gempa bumi dengan karakteristik yang tidak lazim atau anomali", 7)
        highlight_text(target_doc, "Mengidentifikasi anomali secara manual pada data yang memiliki banyak variabel tidaklah efisien", 7)
        highlight_text(target_doc, "Pendekatan analitik konvensional seringkali mengalami hambatan dalam memetakan anomali secara akurat", 7)
        
        # wdBrightGreen = 4 (Data Pendukung)
        highlight_text(target_doc, "BMKG telah berhasil mengumpulkan data historis kejadian gempa bumi dalam jumlah besar", 4)
        highlight_text(target_doc, "Ketersediaan data berskala besar ini membuka peluang besar untuk melakukan pemetaan risiko", 4)
        
        # wdTurquoise = 3 (Solusi)
        highlight_text(target_doc, "penerapan metodologi komputasi modern yang berfokus pada pengenalan pola mandiri (unsupervised learning) merupakan jalan keluar yang paling rasional", 3)
        highlight_text(target_doc, "algoritma Isolation Forest telah muncul sebagai salah satu pendekatan unsupervised learning yang paling andal", 3)
        highlight_text(target_doc, "mengintegrasikannya ke dalam sebuah purwarupa aplikasi mobile berbasis Android yang dinamakan Aplikasi AMANIN", 3)

        print("Selesai.")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

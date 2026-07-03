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
            
        print(f"Total Sections: {target_doc.Sections.Count}")
        
        # Orientasi Portrait dalam wdOrientation
        wdOrientPortrait = 0
        
        # Kita cek semua section
        for i in range(1, target_doc.Sections.Count + 1):
            section = target_doc.Sections(i)
            # Cek teks di dalam section ini untuk mencari Bab 2 ke bawah
            # Tapi cara termudah adalah mengubah section yang orientasinya Landscape menjadi Portrait, 
            # asalkan bukan section yang memang sengaja di-landscape (kalau ada). 
            # Karena user bilang "BAB 2 kebawah layoutnya jadi landscape semua", kita asumsikan semua section 
            # dari awal sampai akhir harusnya Portrait, atau minimal section setelah Bab 1.
            
            if section.PageSetup.Orientation == 1: # 1 = wdOrientLandscape
                print(f"Mengubah Section {i} dari Landscape menjadi Portrait.")
                section.PageSetup.Orientation = wdOrientPortrait
                
        print("Selesai mengubah layout menjadi Portrait.")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

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
            
        wdOrientLandscape = 1
        
        # Cari tabel yang mengandung kata 'state of the art' atau sesuatu yang relevan
        target_table = None
        for table in target_doc.Tables:
            text = table.Range.Text.lower()
            if "state of the art" in text or "state-of-the-art" in text or "penulis" in text:
                # Kadang tabel state of the art punya kolom "Penulis" "Tahun" "Metode" dsb
                # Kita cek lebih jauh
                if "metode" in text or "algoritma" in text or "art" in text:
                    target_table = table
                    break
        
        if target_table:
            print("Tabel State of the Art ditemukan! Mengubah orientasi...")
            # Kita select tabel tersebut
            target_table.Select()
            selection = word.Selection
            
            # Ubah orientasi khusus untuk teks yang di-select.
            # Word akan otomatis membuat Section Break Continuous/Next Page di sekitarnya.
            selection.PageSetup.Orientation = wdOrientLandscape
            print("Berhasil mengubah orientasi tabel menjadi Landscape.")
        else:
            print("Tabel State of the Art tidak ditemukan secara otomatis.")
            # Coba berdasarkan paragraf
            for i in range(540, 600):
                if target_doc.Paragraphs(i).Range.Tables.Count > 0:
                    print(f"Menemukan tabel di paragraf {i}, mencoba mengubah orientasinya.")
                    target_table = target_doc.Paragraphs(i).Range.Tables(1)
                    target_table.Select()
                    word.Selection.PageSetup.Orientation = wdOrientLandscape
                    break
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

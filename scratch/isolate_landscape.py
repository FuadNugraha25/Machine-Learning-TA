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
        wdSectionBreakNextPage = 2
        
        target_table = None
        for table in target_doc.Tables:
            text = table.Range.Text.lower()
            if "state of the art" in text or "state-of-the-art" in text:
                if "metode" in text or "algoritma" in text or "art" in text:
                    target_table = table
                    break
        
        if target_table:
            print("Tabel State of the Art ditemukan! Membuat Section Break...")
            
            # Insert section break before table
            start_range = target_doc.Range(target_table.Range.Start, target_table.Range.Start)
            start_range.InsertBreak(Type=wdSectionBreakNextPage)
            
            # Insert section break after table
            end_range = target_doc.Range(target_table.Range.End, target_table.Range.End)
            end_range.InsertBreak(Type=wdSectionBreakNextPage)
            
            # Now the table is in its own section. 
            # Find the section that contains the table.
            for i in range(1, target_doc.Sections.Count + 1):
                sec = target_doc.Sections(i)
                # If table's start is within this section's range
                if sec.Range.Start <= target_table.Range.Start and sec.Range.End >= target_table.Range.End:
                    sec.PageSetup.Orientation = wdOrientLandscape
                    print("Berhasil mengisolasi tabel dan mengubah orientasi menjadi Landscape.")
                    break
        else:
            print("Tabel tidak ditemukan.")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

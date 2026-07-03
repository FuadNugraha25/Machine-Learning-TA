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
            
        # Skip TOC
        find_toc = target_doc.Content.Find
        find_toc.Execute("BAB III")
        if find_toc.Found:
            search_range = target_doc.Range(find_toc.Parent.End, target_doc.Content.End)
        else:
            search_range = target_doc.Content
            
        # Find start of BAB IV
        search_range.Find.ClearFormatting()
        search_range.Find.Execute("BAB IV")
        
        if not search_range.Find.Found:
            print("Could not find start: BAB IV")
            return
            
        # start_rng is the paragraph of BAB IV
        start_rng = search_range.Paragraphs(1).Range
        
        # We have the paragraph index of BAB IV? No, we just have Range.
        start_pos = start_rng.End
        
        # Let's find "BAB V" or "DAFTAR PUSTAKA"
        search_end_rng = target_doc.Range(start_pos, target_doc.Content.End)
        search_end_rng.Find.ClearFormatting()
        search_end_rng.Find.Execute("BAB V")
        
        if not search_end_rng.Find.Found:
            search_end_rng = target_doc.Range(start_pos, target_doc.Content.End)
            search_end_rng.Find.Execute("DAFTAR PUSTAKA")
            
        if not search_end_rng.Find.Found:
            print("Could not find end: BAB V or DAFTAR PUSTAKA")
            return
            
        end_pos = search_end_rng.Paragraphs(1).Range.Start
        
        # The user said "untuk judul bab 4 biarkan saja"
        # Often BAB IV is followed by a newline and then "HASIL DAN PEMBAHASAN".
        # Let's find out if the text right after start_pos is "HASIL DAN PEMBAHASAN"
        peek_rng = target_doc.Range(start_pos, start_pos + 100)
        peek_text = peek_rng.Text.strip()
        if "HASIL DAN PEMBAHASAN" in peek_text.upper():
            # Find the paragraph for HASIL DAN PEMBAHASAN
            temp_rng = target_doc.Range(start_pos, target_doc.Content.End)
            temp_rng.Find.Execute("HASIL")
            if temp_rng.Find.Found:
                start_pos = temp_rng.Paragraphs(1).Range.End
                
        print(f"Deleting from {start_pos} to {end_pos}")
        delete_rng = target_doc.Range(start_pos, end_pos)
        
        paras = delete_rng.Paragraphs
        num_paras = paras.Count
        print(f"Terdapat {num_paras} paragraf yang akan dihapus.")
        
        deleted_count = 0
        for i in range(num_paras, 0, -1):
            try:
                paras(i).Range.Delete()
                deleted_count += 1
            except Exception as pe:
                pass
                
        print(f"Berhasil menghapus {deleted_count} dari {num_paras} isi BAB IV.")
        
        print("Berhasil menghapus isi BAB IV.")
            
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

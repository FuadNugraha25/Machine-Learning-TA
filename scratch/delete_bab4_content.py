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
            
        paragraphs = target_doc.Paragraphs
        start_idx = -1
        end_idx = -1
        
        # Find HASIL DAN PEMBAHASAN (BAB IV)
        for i, para in enumerate(paragraphs):
            try:
                style_name = para.Style.NameLocal
                text = para.Range.Text.strip().upper()
                if ("Heading 1" in style_name or "Judul" in style_name) and "HASIL DAN PEMBAHASAN" in text:
                    start_idx = i
                elif ("Heading 1" in style_name or "Judul" in style_name) and ("BAB V" in text or "DAFTAR PUSTAKA" in text or "KESIMPULAN" in text) and start_idx != -1:
                    end_idx = i
                    break
            except:
                pass
                
        if start_idx != -1 and end_idx != -1:
            print(f"Deleting paragraphs from {start_idx + 2} to {end_idx}")
            deleted = 0
            # 1-based indexing for Paragraphs
            for i in range(end_idx, start_idx + 1, -1):
                try:
                    paragraphs(i).Range.Delete()
                    deleted += 1
                except Exception as ex:
                    print(f"Failed to delete {i}: {ex}")
            print(f"Berhasil menghapus {deleted} paragraf isi BAB 4.")
        else:
            print(f"Gagal menemukan batas: start_idx={start_idx}, end_idx={end_idx}")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

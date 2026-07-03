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
            print(f"Mengganti teks dari paragraf {start_idx + 2} sampai {end_idx - 1}")
            start_pos = paragraphs(start_idx + 2).Range.Start
            end_pos = paragraphs(end_idx - 1).Range.End
            
            rng = target_doc.Range(start_pos, end_pos)
            rng.Text = "\r"
            print("Berhasil menghapus isi BAB 4.")
        else:
            print(f"Gagal menemukan batas: start_idx={start_idx}, end_idx={end_idx}")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

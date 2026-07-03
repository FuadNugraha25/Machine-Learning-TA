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
        count = paragraphs.Count
        
        start_para = -1
        end_para = -1
        
        # Find BAB IV (the actual one should be the last occurrence)
        for i in range(count, 0, -1):
            text = paragraphs(i).Range.Text.strip().upper()
            if text.startswith("BAB IV"):
                start_para = i
                break
                
        if start_para == -1:
            print("Gagal menemukan BAB IV")
            return
            
        # Find BAB V (the actual one should be the last occurrence, or the first occurrence after BAB IV)
        for i in range(start_para + 1, count + 1):
            text = paragraphs(i).Range.Text.strip().upper()
            if text.startswith("BAB V"):
                end_para = i
                break
                
        if end_para == -1:
            # If no BAB V, maybe DAFTAR PUSTAKA
            for i in range(start_para + 1, count + 1):
                text = paragraphs(i).Range.Text.strip().upper()
                if text.startswith("DAFTAR PUSTAKA"):
                    end_para = i
                    break
                    
        if end_para == -1:
            print("Gagal menemukan batas akhir BAB IV")
            return
            
        print(f"Menghapus isi dari paragraf {start_para + 1} sampai {end_para - 1}")
        
        # Delete backwards to preserve indices
        deleted = 0
        for i in range(end_para - 1, start_para, -1):
            # Do not delete the title itself which might be at start_para or start_para+1 if title is split
            # Let's check if start_para + 1 is the title part 2 (e.g. "HASIL DAN PEMBAHASAN")
            # If it's short and uppercase, it might be the title. Let's ask user to keep it or just keep start_para.
            # "untuk judul bab 4 biarkan saja". Usually BAB IV is one paragraph, or two.
            text = paragraphs(i).Range.Text.strip()
            # If the next paragraph is "HASIL DAN PEMBAHASAN" or similar, keep it.
            if i == start_para + 1 and text.isupper() and len(text) < 50:
                print(f"Mempertahankan sub-judul BAB IV: {text}")
                continue
                
            paragraphs(i).Range.Delete()
            deleted += 1
            
        print(f"Berhasil menghapus {deleted} paragraf di dalam BAB IV.")
        
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

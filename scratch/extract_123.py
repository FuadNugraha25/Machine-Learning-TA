import win32com.client
import sys
import io

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
        
        # Find start of 1.2 and end boundary
        for i in range(1, paragraphs.Count + 1):
            try:
                text = paragraphs(i).Range.Text.strip().upper()
                style_name = paragraphs(i).Style.NameLocal
                
                if "RUMUSAN MASALAH" in text and style_name.startswith("Heading 2"):
                    start_idx = i
                elif ("BATASAN MASALAH" in text or "MANFAAT PENELITIAN" in text) and style_name.startswith("Heading 2") and start_idx != -1:
                    end_idx = i
                    break
            except:
                pass
                
        if start_idx != -1 and end_idx != -1:
            with io.open("c:\\Users\\Fuad Nugraha\\Documents\\GitHub\\Machine-Learning-TA\\scratch\\read_1_2.txt", "w", encoding="utf-8") as f:
                for i in range(start_idx, end_idx):
                    text = paragraphs(i).Range.Text.strip()
                    style = paragraphs(i).Style.NameLocal
                    if len(text) > 2:
                        f.write(f"[{i}] ({style}): {text}\n")
            print("Berhasil mengekstrak 1.2 dan 1.3")
        else:
            print(f"Gagal menemukan batas: start_idx={start_idx}, end_idx={end_idx}")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

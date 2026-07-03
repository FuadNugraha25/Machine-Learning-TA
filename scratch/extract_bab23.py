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
        
        # Find start of BAB II
        for i in range(1, paragraphs.Count + 1):
            try:
                style_name = paragraphs(i).Style.NameLocal
                text = paragraphs(i).Range.Text.strip().upper()
                if ("Heading 1" in style_name or "Judul" in style_name) and "TINJAUAN PUSTAKA" in text:
                    start_idx = i
                elif ("Heading 1" in style_name or "Judul" in style_name) and "HASIL DAN PEMBAHASAN" in text and start_idx != -1:
                    end_idx = i
                    break
            except:
                pass
                
        if start_idx != -1 and end_idx != -1:
            with io.open("c:\\Users\\Fuad Nugraha\\Documents\\GitHub\\Machine-Learning-TA\\scratch\\bab2_bab3_content.txt", "w", encoding="utf-8") as f:
                for i in range(start_idx, end_idx):
                    try:
                        text = paragraphs(i).Range.Text.strip()
                        style = paragraphs(i).Style.NameLocal
                        if len(text) > 2:
                            f.write(f"[{i}] ({style}): {text}\n")
                    except:
                        pass
            print("Berhasil mengekstrak BAB II dan BAB III.")
        else:
            print(f"Gagal menemukan batas: start_idx={start_idx}, end_idx={end_idx}")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

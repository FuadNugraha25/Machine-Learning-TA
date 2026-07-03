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
        
        # Find PENDAHULUAN (BAB I)
        for i, para in enumerate(paragraphs):
            try:
                style_name = para.Style.NameLocal
                text = para.Range.Text.strip().upper()
                if ("Heading 1" in style_name or "Judul" in style_name) and "PENDAHULUAN" in text:
                    start_idx = i
                elif ("Heading 1" in style_name or "Judul" in style_name) and "TINJAUAN PUSTAKA" in text and start_idx != -1:
                    end_idx = i
                    break
            except:
                pass
                
        if start_idx != -1 and end_idx != -1:
            # Print the text of Chapter 1
            print("=== BAB I TEXT ===")
            for i in range(start_idx, end_idx):
                try:
                    text = paragraphs(i).Range.Text.strip()
                    if len(text) > 5:
                        print(f"[{i}]: {text}")
                except Exception as ex:
                    pass
        else:
            print(f"Gagal menemukan batas BAB I: start_idx={start_idx}, end_idx={end_idx}")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

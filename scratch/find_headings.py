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
            
        print("Mencari Heading 1...")
        
        for i, para in enumerate(target_doc.Paragraphs):
            try:
                style_name = para.Style.NameLocal
                if "Heading 1" in style_name or "Judul" in style_name:
                    text = para.Range.Text.strip()
                    print(f"[{i}] {style_name}: {text}")
            except:
                pass
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

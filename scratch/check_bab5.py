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
        for i in range(1050, 1080):
            try:
                style_name = paragraphs(i).Style.NameLocal
                if "Heading" in style_name or "Judul" in style_name or "BAB" in paragraphs(i).Range.Text.strip() or "KESIMPULAN" in paragraphs(i).Range.Text.strip():
                    print(f"[{i}] {style_name}: {paragraphs(i).Range.Text.strip()}")
            except:
                pass
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

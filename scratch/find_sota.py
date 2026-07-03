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
        for i in range(1, paragraphs.Count + 1):
            try:
                text = paragraphs(i).Range.Text.strip().lower()
                if "state of the art" in text or "state-of-the-art" in text:
                    page_num = paragraphs(i).Range.Information(3) # wdActiveEndPageNumber
                    print(f"Ditemukan di Paragraf [{i}], Teks: {text[:50]}, Halaman: {page_num}")
            except:
                pass
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

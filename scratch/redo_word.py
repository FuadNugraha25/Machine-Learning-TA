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
            
        print("Mencoba Redo...")
        for i in range(30):
            result = target_doc.Redo()
            if result:
                # Cek isi sekitar paragraf 216
                text_216 = target_doc.Paragraphs(216).Range.Text.strip() if target_doc.Paragraphs.Count >= 216 else ""
                text_217 = target_doc.Paragraphs(217).Range.Text.strip() if target_doc.Paragraphs.Count >= 217 else ""
                text_218 = target_doc.Paragraphs(218).Range.Text.strip() if target_doc.Paragraphs.Count >= 218 else ""
                print(f"Redo {i+1}: [216] {text_216[:30]} | [217] {text_217[:30]} | [218] {text_218[:30]}")
            else:
                print("Tidak bisa Redo lagi.")
                break
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

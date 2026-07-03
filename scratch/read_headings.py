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
            
        print("Mencari struktur BAB...")
        
        for i, para in enumerate(target_doc.Paragraphs):
            text = para.Range.Text.strip()
            text_upper = text.upper()
            if text_upper.startswith("BAB ") or text_upper.startswith("DAFTAR "):
                # Print to understand structure
                print(f"[{i}]: {text}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

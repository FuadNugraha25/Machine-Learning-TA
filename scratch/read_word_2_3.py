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
            
        print("Membaca isi di bawah II.3...")
        # Get all paragraphs
        found_start = False
        in_toc = True
        content = []
        for i, para in enumerate(target_doc.Paragraphs):
            text = para.Range.Text.strip()
            # Skip until we pass the TOC (e.g. we see BAB II or similar, but let's just use a heuristic: TOC lines usually have tabs or end with numbers)
            if in_toc and "TINJAUAN PUSTAKA" in text and i > 50:
                in_toc = False
                
            if not in_toc:
                if "Deteksi Anomali pada Data Historis Gempa Bumi" in text and not "\t" in text:
                    found_start = True
                    content.append(f"--- [START II.3] ---")
                elif found_start and text.startswith("II.4 "):
                    content.append(f"--- [END II.3] ---")
                    break
                elif found_start:
                    if text:
                        content.append(f"[{i}]: {text}")
                
        for line in content:
            print(line)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

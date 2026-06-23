import docx
import sys

def read_docx(filepath):
    doc = docx.Document(filepath)
    paragraphs = []
    start = False
    idx = 0
    for p in doc.paragraphs:
        text = p.text.strip()
        if "Latar Belakang" in text and ("I.1" in text or "1.1" in text):
            start = True
        elif start and text.startswith("I.2") or text.startswith("1.2"):
            break
        
        if start:
            paragraphs.append(f"{idx}: {text}")
        idx += 1
            
    return "\n".join(paragraphs)

if __name__ == "__main__":
    filepath = r"C:\Users\Fuad Nugraha\Documents\Laporan Tugas Akhir\Tugas Akhir Semester 8 AI.docx"
    print("--- Latar Belakang Content ---")
    content = read_docx(filepath)
    print(content)

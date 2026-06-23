import win32com.client
import sys

def main():
    word = win32com.client.Dispatch("Word.Application")
    doc = None
    for d in word.Documents:
        if "Tugas Akhir Semester 8 AI.docx" in d.Name:
            doc = d
            break
            
    if not doc:
        print("Could not find the open document")
        sys.exit(1)
        
    start_capture = False
    captured_text = []
    
    for i, p in enumerate(doc.Paragraphs):
        text = p.Range.Text.strip()
        if "I.2\tRumusan Masalah" in text or "Rumusan Masalah" == text:
            start_capture = True
            
        if "Bab II\tTINJAUAN PUSTAKA" in text or "TINJAUAN PUSTAKA" == text:
            break
            
        if start_capture and text:
            captured_text.append(f"{i}: {text}")
            
    with open('bab1_rest.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(captured_text))
        
    print("Extracted rest of Bab 1.")

if __name__ == '__main__':
    main()

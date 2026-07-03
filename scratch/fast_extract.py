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
            
        start_idx = -1
        end_idx = -1
        
        # Iterate efficiently
        with io.open("c:\\Users\\Fuad Nugraha\\Documents\\GitHub\\Machine-Learning-TA\\scratch\\bab2_bab3_content.txt", "w", encoding="utf-8") as f:
            for i, para in enumerate(target_doc.Paragraphs):
                try:
                    style_name = para.Style.NameLocal
                    text = para.Range.Text.strip()
                    text_upper = text.upper()
                    
                    if ("Heading 1" in style_name or "Judul" in style_name) and "TINJAUAN PUSTAKA" in text_upper:
                        start_idx = i
                        
                    if start_idx != -1:
                        if ("Heading 1" in style_name or "Judul" in style_name) and "HASIL DAN PEMBAHASAN" in text_upper:
                            end_idx = i
                            break
                        
                        if len(text) > 2:
                            f.write(f"[{i}] ({style_name}): {text}\n")
                except:
                    pass
                    
        print(f"Berhasil mengekstrak BAB II dan BAB III (from {start_idx} to {end_idx}).")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

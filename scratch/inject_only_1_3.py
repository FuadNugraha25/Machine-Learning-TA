import win32com.client
import sys

def insert_heading(selection, text, level):
    selection.Style = f"Heading {level}"
    selection.TypeText(text)
    selection.TypeParagraph()

def insert_normal(selection, text):
    selection.Style = "Normal"
    selection.TypeText(text)
    selection.TypeParagraph()

def insert_list(selection, text):
    # Instead of fighting with list styles, we just use "Normal" or "List Paragraph"
    selection.Style = "List Paragraph"
    selection.TypeText(text)
    selection.TypeParagraph()

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
        
        # Find start of 1.3 Tujuan Penelitian and end boundary (Batasan Penelitian)
        for i in range(1, paragraphs.Count + 1):
            try:
                text = paragraphs(i).Range.Text.strip().upper()
                style_name = paragraphs(i).Style.NameLocal
                
                if "TUJUAN PENELITIAN" in text and style_name.startswith("Heading 2"):
                    start_idx = i
                elif ("BATASAN PENELITIAN" in text or "BATASAN MASALAH" in text) and style_name.startswith("Heading 2") and start_idx != -1:
                    end_idx = i
                    break
            except:
                pass
                
        if start_idx != -1 and end_idx != -1:
            print(f"Mengganti HANYA BAB 1.3 dari paragraf {start_idx} sampai {end_idx - 1}")
            start_pos = paragraphs(start_idx).Range.Start
            end_pos = paragraphs(end_idx - 1).Range.End
            
            selection = target_doc.ActiveWindow.Selection
            selection.SetRange(start_pos, end_pos)
            selection.Delete()
            
            selection.SetRange(start_pos, start_pos)
            
            # 1.3 TUJUAN PENELITIAN
            insert_heading(selection, "Tujuan Penelitian", 2)
            insert_normal(selection, "Berdasarkan rumusan masalah sebelumnya, tujuan penelitian dapat diuraikan sebagai berikut:")
            insert_list(selection, "Merancang dan mengintegrasikan model deteksi anomali ke dalam Aplikasi AMANIN agar mampu menyajikan wawasan mitigasi (insight) yang cerdas dan proaktif kepada masyarakat.")
            insert_list(selection, "Mengimplementasikan algoritma Isolation Forest untuk mendeteksi kejadian anomali seismik secara otomatis pada data historis kegempaan BMKG yang berdimensi multivariat, tidak berlabel, dan tidak memiliki ground truth.")
            insert_list(selection, "Mengevaluasi persebaran anomaly score dan batas ambang (threshold) yang dihasilkan oleh model untuk memastikan bahwa kejadian yang diisolasi benar-benar memiliki karakteristik gempa yang tidak wajar.")
            
            selection.TypeParagraph()

            print("Berhasil memasukkan teks Bab 1.3 baru tanpa mengganggu yang lain.")
        else:
            print(f"Gagal menemukan batas: start_idx={start_idx}, end_idx={end_idx}")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

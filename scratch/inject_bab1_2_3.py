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
    # Using normal text but starting with numbers for simplicity, or we can use List Paragraph
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
        
        # Find start of 1.2 Rumusan Masalah and end boundary (1.4 Batasan Masalah or Manfaat)
        for i in range(1, paragraphs.Count + 1):
            try:
                text = paragraphs(i).Range.Text.strip().upper()
                style_name = paragraphs(i).Style.NameLocal
                
                # Check for 1.2 Rumusan Masalah
                if "RUMUSAN MASALAH" in text and style_name.startswith("Heading 2"):
                    start_idx = i
                # Check for the next heading after Tujuan (usually Batasan Masalah or Manfaat Penelitian)
                elif ("BATASAN MASALAH" in text or "MANFAAT PENELITIAN" in text) and style_name.startswith("Heading 2") and start_idx != -1:
                    end_idx = i
                    break
            except:
                pass
                
        if start_idx != -1 and end_idx != -1:
            print(f"Mengganti BAB 1.2 dan 1.3 dari paragraf {start_idx} sampai {end_idx - 1}")
            start_pos = paragraphs(start_idx).Range.Start
            end_pos = paragraphs(end_idx - 1).Range.End
            
            selection = target_doc.ActiveWindow.Selection
            selection.SetRange(start_pos, end_pos)
            selection.Delete()
            
            # Posisikan ke titik yang sudah dihapus
            selection.SetRange(start_pos, start_pos)
            
            # 1.2 RUMUSAN MASALAH
            insert_heading(selection, "Rumusan Masalah", 2)
            insert_normal(selection, "Berdasarkan latar belakang yang telah diuraikan, rumusan masalah dalam penelitian ini difokuskan pada tiga poin utama:")
            insert_list(selection, "Bagaimana mengimplementasikan algoritma Isolation Forest untuk mendeteksi kejadian anomali seismik secara otomatis pada data historis kegempaan BMKG yang berdimensi multivariat dan tidak berlabel (unlabeled)?")
            insert_list(selection, "Bagaimana merancang dan mengintegrasikan model deteksi anomali tersebut ke dalam Aplikasi AMANIN agar mampu menyajikan wawasan mitigasi (insight) yang cerdas dan proaktif kepada masyarakat?")
            insert_list(selection, "Bagaimana mengevaluasi persebaran anomaly score dan batas ambang (threshold) yang dihasilkan oleh model untuk memastikan bahwa kejadian yang diisolasi benar-benar memiliki karakteristik gempa yang tidak wajar?")
            
            selection.TypeParagraph() # Extra space
            
            # 1.3 TUJUAN PENELITIAN
            insert_heading(selection, "Tujuan Penelitian", 2)
            insert_normal(selection, "Sejalan dengan rumusan masalah yang telah ditetapkan, penelitian ini memiliki tujuan yang ingin dicapai, yaitu:")
            insert_list(selection, "Mengimplementasikan algoritma Isolation Forest untuk mendeteksi kejadian anomali seismik secara otomatis pada data historis kegempaan BMKG yang berdimensi multivariat dan tidak berlabel.")
            insert_list(selection, "Merancang dan mengintegrasikan model deteksi anomali tersebut ke dalam sistem Aplikasi AMANIN sehingga mampu memberikan wawasan peringatan dini yang proaktif bagi masyarakat.")
            insert_list(selection, "Mengevaluasi hasil pemisahan kejadian gempa anomali dan normal berdasarkan persebaran anomaly score yang dihasilkan oleh model.")
            
            selection.TypeParagraph() # Extra space

            print("Berhasil memasukkan teks Bab 1.2 dan 1.3 baru.")
        else:
            print(f"Gagal menemukan batas: start_idx={start_idx}, end_idx={end_idx}")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

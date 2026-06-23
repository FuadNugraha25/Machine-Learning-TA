import win32com.client
import sys

def main():
    word = win32com.client.Dispatch("Word.Application")
    doc = next((d for d in word.Documents if 'Tugas Akhir Semester 8 AI.docx' in d.Name), None)
    if not doc:
        print("Document not found.")
        sys.exit(1)
        
    target_text = "Berdasarkan hasil analisis terhadap aplikasi yang telah tersedia, Aplikasi AMANIN dirancang"
    found = False
    
    for p in doc.Paragraphs:
        if target_text in p.Range.Text:
            rng = p.Range
            # Find the specific sentence to insert after
            success = rng.Find.Execute("menggunakan algoritma Isolation Forest.")
            if success:
                # rng is now exactly the matched text
                insert_rng = doc.Range(rng.End, rng.End)
                added_text = " Lebih lanjut, fitur analitik ini diwujudkan dalam bentuk mekanisme live notification (notifikasi langsung), di mana aplikasi akan mengirimkan peringatan khusus kepada pengguna apabila gempa bumi terbaru (latest earthquake) yang masuk ke dalam sistem terdeteksi sebagai suatu kejadian anomali."
                insert_rng.Text = added_text
                
                # Format only the added text with underline
                # wdUnderlineSingle = 1
                format_rng = doc.Range(rng.End + 1, rng.End + len(added_text))
                format_rng.Font.Underline = 1
                
                word.ActiveWindow.ScrollIntoView(format_rng)
                found = True
                print("Text inserted and underlined successfully.")
                break
                
    if not found:
        print("Target paragraph or text not found.")

if __name__ == '__main__':
    main()

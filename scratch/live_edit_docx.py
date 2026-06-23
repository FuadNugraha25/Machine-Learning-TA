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
        print("Could not find the open document 'Tugas Akhir Semester 8 AI.docx'")
        sys.exit(1)
        
    target_p = None
    for p in doc.Paragraphs:
        if "Berdasarkan paparan permasalahan di atas, penelitian ini bertujuan untuk mengimplementasikan" in p.Range.Text:
            target_p = p
            break
            
    if not target_p:
        print("Target paragraph not found")
        sys.exit(1)
        
    print("Found target paragraph. Replacing text...")
    
    # 1. Replace target paragraph text
    # It's better to preserve formatting, but overwriting Range.Text replaces the whole paragraph text.
    target_p.Range.Text = "Meskipun algoritma komputasional seperti Isolation Forest sangat andal dalam mendeteksi anomali seismik dari data masif, luaran (output) yang dihasilkan pada dasarnya masih berupa metrik analitik yang bersifat teknis. Agar wawasan deteksi anomali ini dapat dimanfaatkan secara praktis dan menjadi instrumen mitigasi bencana yang proaktif, hasil analisis model Machine Learning tersebut harus diintegrasikan ke dalam sebuah platform yang mudah diakses dan dipahami oleh berbagai lapisan masyarakat.\n"
    
    # 2. Insert new paragraph 1
    new_p1 = doc.Range(target_p.Range.End, target_p.Range.End)
    new_p1.Text = "Hingga saat ini, telah terdapat beberapa aplikasi mobile yang berfokus pada penyampaian informasi kebencanaan dan gempa bumi di Indonesia maupun global. Namun, mayoritas aplikasi existing tersebut cenderung hanya menyajikan informasi parametrik dasar—seperti magnitudo, episentrum, dan kedalaman—tanpa dilengkapi fitur analitik cerdas yang mengidentifikasi letak anomali kejadian secara historis. Ketiadaan fitur analitik cerdas ini membuat masyarakat awam seringkali kesulitan untuk menilai tingkat signifikansi dari suatu kejadian gempa yang secara magnitudo mungkin terlihat wajar, namun secara karakteristik profil seismik merupakan sebuah anomali yang sangat jarang terjadi.\n"
    
    # 3. Insert new paragraph 2
    new_p2 = doc.Range(new_p1.End, new_p1.End)
    new_p2.Text = "Berangkat dari permasalahan tersebut, penelitian ini bertujuan tidak hanya untuk mengimplementasikan algoritma Isolation Forest pada dataset historis BMKG, melainkan juga mengintegrasikan sistem pendeteksi anomali tersebut ke dalam sebuah purwarupa aplikasi mobile berbasis Android yang dinamakan Aplikasi AMANIN. Aplikasi AMANIN dirancang untuk menjembatani kesenjangan antara kompleksitas model pendeteksi anomali dan kebutuhan pengguna akan sistem informasi mitigasi gempa yang komprehensif, cerdas, dan mudah dipahami. Sebagai landasan dalam pengembangan fitur inovatif pada Aplikasi AMANIN, berikut disajikan tabel perbandingan antara Aplikasi AMANIN dengan aplikasi informasi gempa bumi yang telah beredar di masyarakat:\n"
    
    # 4. Insert Table
    new_table_range = doc.Range(new_p2.End, new_p2.End)
    table = doc.Tables.Add(new_table_range, 2, 4)
    table.Style = "Table Grid"
    
    table.Cell(1, 1).Range.Text = "Nama Aplikasi / Platform"
    table.Cell(1, 2).Range.Text = "Fitur Utama"
    table.Cell(1, 3).Range.Text = "Penyajian Anomali Seismik"
    table.Cell(1, 4).Range.Text = "Keterbatasan"
    
    # 5. Insert new paragraph 3
    new_p3 = doc.Range(table.Range.End, table.Range.End)
    new_p3.Text = "\nBerdasarkan perbandingan pada tabel di atas, Aplikasi AMANIN dirancang untuk mengisi kekosongan (gap) solusi pada aplikasi mitigasi existing. Melalui pendekatan end-to-end yang mengawinkan kehandalan algoritma unsupervised learning dengan antarmuka mobile yang intuitif, penelitian ini diharapkan mampu memberikan kontribusi nyata dalam memperkuat kesiapsiagaan masyarakat serta mendukung pengambilan keputusan strategis dalam sistem mitigasi bencana gempa bumi di Indonesia.\n"
    
    # Scroll to the edited part so the user can see it
    word.ActiveWindow.ScrollIntoView(target_p.Range)
    
    print("Success editing the open document.")

if __name__ == '__main__':
    main()

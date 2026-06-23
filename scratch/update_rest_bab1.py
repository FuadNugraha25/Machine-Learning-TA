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
        
    print("Document found. Updating...")
    
    # Track which ones we found
    found_rm = False
    found_tp = False
    found_bp = False
    found_mp = False
    
    for i, p in enumerate(doc.Paragraphs):
        text = p.Range.Text.strip()
        
        # 1. Update Rumusan Masalah
        # The last point in Rumusan Masalah is: "Upaya pengawasan seismisitas memerlukan sistem yang mampu mengisolasi kejadian langka..."
        if "Upaya pengawasan seismisitas memerlukan sistem yang mampu mengisolasi kejadian langka yang berbeda secara signifikan dari populasi data latar belakang" in text:
            # We append a new paragraph after this
            new_p = doc.Range(p.Range.End, p.Range.End)
            new_p.Text = "Bagaimana merancang arsitektur integrasi untuk menanamkan (embed) luaran model pendeteksi anomali seismik ini ke dalam layanan backend yang dapat diakses melalui antarmuka Aplikasi AMANIN?\n"
            new_p.ParagraphFormat.Style = p.Range.ParagraphFormat.Style
            # We must apply the same list formatting
            if p.Range.ListFormat.ListType != 0:
                new_p.ListFormat.ApplyListTemplateWithLevel(
                    p.Range.ListFormat.ListTemplate,
                    ContinuePreviousList=True,
                    DefaultListBehavior=1
                )
            found_rm = True
            
        # 2. Update Tujuan Penelitian
        # The last point is: "Menerapkan dan mengevaluasi keandalan algoritma Isolation Forest murni untuk mendeteksi, mengisolasi, dan memetakan skor kejadian gempa anomali berdas"
        elif "Menerapkan dan mengevaluasi keandalan algoritma Isolation Forest murni untuk mendeteksi, mengisolasi, dan memetakan skor kejadian gempa anomali" in text:
            new_p = doc.Range(p.Range.End, p.Range.End)
            new_p.Text = "Mengintegrasikan model komputasional deteksi anomali seismik tersebut ke dalam backend layanan guna mendukung operasional fitur cerdas pada purwarupa Aplikasi AMANIN.\n"
            new_p.ParagraphFormat.Style = p.Range.ParagraphFormat.Style
            if p.Range.ListFormat.ListType != 0:
                new_p.ListFormat.ApplyListTemplateWithLevel(
                    p.Range.ListFormat.ListTemplate,
                    ContinuePreviousList=True,
                    DefaultListBehavior=1
                )
            found_tp = True
            
        # 3. Update Batasan Penelitian
        # The last point is: "Hasil klasifikasi anomali yang dihasilkan model dibatasi fungsinya sebagai wawasan awal (early insight) teknis komputasional..."
        elif "Hasil klasifikasi anomali yang dihasilkan model dibatasi fungsinya sebagai wawasan awal" in text:
            new_p = doc.Range(p.Range.End, p.Range.End)
            new_p.Text = "Fokus utama dari batasan kajian ini adalah pemodelan arsitektur Machine Learning dan backend API; adapun pengembangan tampilan antarmuka (UI/UX) dan sistem frontend mobile dari Aplikasi AMANIN diposisikan sebagai wadah integrasi akhir di luar pemodelan analitik data utama.\n"
            new_p.ParagraphFormat.Style = p.Range.ParagraphFormat.Style
            if p.Range.ListFormat.ListType != 0:
                new_p.ListFormat.ApplyListTemplateWithLevel(
                    p.Range.ListFormat.ListTemplate,
                    ContinuePreviousList=True,
                    DefaultListBehavior=1
                )
            found_bp = True
            
        # 4. Update Manfaat Penelitian
        # "Hasil penelitian ini diharapkan dapat memberikan manfaat bagi masyarakat, khususnya masyarakat di berbagai kawasan rawan gempa di Indonesia, melalui penyediaan landasan analitik yang berpotensi memperkuat akurasi sistem mitigasi bencana nasional. Dengan terdeteksinya anomali gempa secara presisi oleh sistem komputasional, institusi berwenang dapat merumuskan strategi penanggulangan yang lebih tajam, sehingga masyarakat pada akhirnya menerima informasi kesiapsiagaan yang lebih terukur terhadap risiko kejadian gempa yang tidak biasa."
        elif "Hasil penelitian ini diharapkan dapat memberikan manfaat bagi masyarakat, khususnya masyarakat di berbagai kawasan rawan gempa di Indonesia" in text:
            # We replace this paragraph to include AMANIN
            new_text = "Hasil penelitian ini diharapkan dapat memberikan manfaat bagi masyarakat di berbagai kawasan rawan gempa di Indonesia melalui penyediaan landasan analitik cerdas yang berpotensi memperkuat sistem mitigasi bencana nasional. Dengan terdeteksinya anomali gempa secara presisi oleh sistem komputasional, institusi berwenang dapat merumuskan strategi penanggulangan yang lebih tajam, sehingga masyarakat pada akhirnya menerima peringatan dan informasi kesiapsiagaan yang lebih terukur secara langsung melalui platform interaktif seperti Aplikasi AMANIN.\n"
            # It replaces the whole paragraph, wait, range.text replaces the text inside. But we must be careful with the trailing \r.
            p.Range.Text = new_text
            found_mp = True
            
    if found_rm and found_tp and found_bp and found_mp:
        print("Successfully updated all sub-chapters (Rumusan Masalah, Tujuan, Batasan, Manfaat)!")
    else:
        print(f"Update partial. RM: {found_rm}, TP: {found_tp}, BP: {found_bp}, MP: {found_mp}")
        
if __name__ == '__main__':
    main()

import win32com.client
import sys

def insert_normal(selection, text):
    selection.Style = "Normal"
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
        
        # Find start of Latar Belakang and end (Rumusan Masalah)
        for i in range(1, paragraphs.Count + 1):
            try:
                text = paragraphs(i).Range.Text.strip().upper()
                style_name = paragraphs(i).Style.NameLocal
                
                # Check for 1.1 Latar Belakang
                if "LATAR BELAKANG" in text and style_name.startswith("Heading 2"):
                    start_idx = i
                elif "RUMUSAN MASALAH" in text and style_name.startswith("Heading 2") and start_idx != -1:
                    end_idx = i
                    break
            except:
                pass
                
        if start_idx != -1 and end_idx != -1:
            print(f"Mengganti BAB 1.1 dari paragraf {start_idx} sampai {end_idx - 1}")
            start_pos = paragraphs(start_idx).Range.End # Kita pertahankan judul "Latar Belakang"
            end_pos = paragraphs(end_idx - 1).Range.End
            
            selection = target_doc.ActiveWindow.Selection
            selection.SetRange(start_pos, end_pos)
            selection.Delete()
            
            # Posisikan ke awal lagi (setelah judul)
            selection.SetRange(start_pos, start_pos)
            
            # Draf baru
            p1 = "Gempa bumi merupakan salah satu fenomena alam global yang memiliki daya destruktif sangat tinggi sekaligus paling sulit diprediksi secara presisi. Secara geologis, aktivitas seismik ini dipicu oleh pelepasan energi secara tiba-tiba akibat pergerakan dinamis lempeng-lempeng tektonik yang menyusun kerak bumi. Dalam skala nasional, Indonesia memiliki tingkat kerentanan seismik yang ekstrem karena posisinya yang strategis sekaligus rawan, yakni berada persis di sepanjang Cincin Api Pasifik (Pacific Ring of Fire) serta menjadi titik temu tiga lempeng tektonik utama dunia: Indo-Australia, Eurasia, dan Pasifik. Tingginya intensitas gempa yang melanda kawasan Nusantara ini menjadikan urgensi mitigasi bencana sebagai sebuah prioritas absolut demi meminimalisasi kerugian jiwa maupun infrastruktur (Nugraha dkk., 2018)."
            p2 = "Seiring dengan kemajuan teknologi pemantauan, stasiun sensor kegempaan yang dioperasikan oleh Badan Meteorologi, Klimatologi, dan Geofisika (BMKG) telah merekam setiap kejadian gempa selama belasan tahun. Aktivitas pemantauan ini menghasilkan objek data historis berskala masif (mencapai lebih dari 63.000 rekaman periode 2008-2026) yang memuat berbagai parameter penting seperti magnitudo, kedalaman, garis lintang, dan garis bujur. Tumpukan big data historis ini sesungguhnya menyimpan manfaat yang sangat besar; kumpulan data tersebut merekam jejak pola pergerakan tektonik masa lalu yang apabila digali lebih dalam, dapat dimanfaatkan sebagai basis analitik intelijen untuk memperkuat strategi mitigasi bencana non-struktural yang kuat."
            p3 = "Namun, di balik potensi pemanfaatan data tersebut, terdapat sebuah masalah krusial di bidang geofisika. Di dalam ribuan rekaman gempa biasa, sering kali tersembunyi kejadian-kejadian gempa bumi dengan karakteristik yang tidak lazim atau anomali. Pendeteksian anomali seismik ini sebenarnya sangat penting, karena anomali seringkali menjadi indikator peringatan dini mengenai adanya potensi rekahan sesar baru, anomali struktur bawah permukaan, maupun akumulasi pelepasan stres (tegangan) lempeng yang sebelumnya belum pernah terpetakan (Pratama dkk., 2020)."
            p4 = "Sayangnya, pemetaan dan identifikasi anomali ini menjadi masalah yang sulit diselesaikan karena terkendala oleh beberapa penyebab utama. Pertama, besarnya volume data yang dihasilkan setiap hari membuat proses inspeksi anomali secara manual oleh pakar menjadi sesuatu yang mustahil dan sangat rentan terhadap subjektivitas interpretasi. Kedua, data historis gempa bumi ini berdimensi multivariat dan tidak memiliki pelabelan (ground truth) yang secara eksplisit membedakan antara status gempa normal dengan gempa anomali, sehingga metode komputasional konvensional kesulitan untuk mendeteksi pola yang tersembunyi di dalamnya."
            p5 = "Kondisi tersebut memunculkan celah penelitian (research gap) yang nyata, baik dari sisi akademis maupun praktis. Secara akademis, pendekatan komputasi konvensional tidak mampu beradaptasi dengan kumpulan data berdimensi tinggi yang tidak dilengkapi label. Sementara itu secara praktis, meskipun saat ini telah banyak tersedia aplikasi informasi gempa (seperti platform info BMKG dan InaRisk), aplikasi-aplikasi tersebut umumnya hanya menyajikan parameter dasar kejadian gempa secara mentah. Belum ada mekanisme yang menyajikan wawasan cerdas (insight) kepada masyarakat mengenai apakah kejadian gempa terbaru yang sedang menimpa mereka merupakan sebuah gempa dengan karakteristik anomali atau sekadar rutinitas pergerakan tektonik biasa."
            p6 = "Untuk menjawab gap dan permasalahan tersebut, penelitian ini menawarkan sebuah solusi komprehensif berupa pengembangan sistem cerdas berbasis aplikasi seluler (Aplikasi AMANIN). Sistem ini tidak hanya beroperasi sebagai penampil data pasif, tetapi dirancang proaktif untuk memberikan notifikasi otomatis serta penanda khusus apabila gempa yang baru saja terjadi memiliki penyimpangan karakteristik secara historis."
            p7 = "Dalam proses di balik layarnya, untuk menghadirkan kecerdasan deteksi anomali tersebut tanpa terkendala oleh ketiadaan label data, penelitian ini mengimplementasikan metode Machine Learning berjenis Unsupervised Learning, yaitu algoritma Isolation Forest. Pemilihan metode Isolation Forest didasarkan pada keunggulan fundamentalnya yang sangat efisien dalam memproses big data dan langsung bekerja dengan cara mengisolasi titik data anomali (yang berjumlah sedikit dan memiliki atribut berbeda ekstrem) menggunakan partisi pohon acak (Hariri dkk., 2019). Dengan pendekatan ini, diharapkan sistem yang dibangun dapat menghadirkan era baru informasi mitigasi bencana yang tidak hanya sekadar real-time, tetapi juga informatif secara analitik."

            # Insert paragraphs
            selection.TypeParagraph() # Beri spasi sebelum mulai paragraf pertama
            insert_normal(selection, p1)
            insert_normal(selection, p2)
            insert_normal(selection, p3)
            insert_normal(selection, p4)
            insert_normal(selection, p5)
            insert_normal(selection, p6)
            insert_normal(selection, p7)
            
            print("Berhasil memasukkan teks Bab 1.1 baru.")
        else:
            print(f"Gagal menemukan batas: start_idx={start_idx}, end_idx={end_idx}")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

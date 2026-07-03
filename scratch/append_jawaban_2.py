import codecs

with codecs.open(r"c:\Users\Fuad Nugraha\Documents\GitHub\Machine-Learning-TA\Anomaly Detection BMKG\jawaban_laporan.txt", "a", "utf-8") as f:
    f.write("\n\nF. Evaluasi\n")
    f.write("1. Bagaimana model dievaluasi?\n")
    f.write("   (KURANG YAKIN)\n")
    f.write("   Secara teori, model unsupervised seperti Isolation Forest dievaluasi dengan menganalisis distribusi Anomaly Score, melihat seberapa logis batas pemisahan (threshold) yang terbentuk, dan memvalidasi secara visual (deskriptif spasial) apakah titik gempa yang dicap 'anomali' benar-benar memiliki karakteristik ekstrem dibandingkan mayoritas data normal.\n\n")
    
    f.write("2. Metrik apa yang digunakan?\n")
    f.write("   (KURANG YAKIN)\n")
    f.write("   Metrik utamanya adalah Anomaly Score (berdasarkan rata-rata kedalaman/path length pada pohon acak). Jika penelitian ini dikembangkan lebih lanjut, bisa saja menggunakan pseudo-metric seperti Silhouette Score atau analisis kontur spasial.\n\n")
    
    f.write("3. Mengapa memilih metrik tersebut?\n")
    f.write("   (KURANG YAKIN)\n")
    f.write("   Karena dataset geofisika aktual ini tidak berlabel (unlabeled), kita sama sekali tidak bisa menggunakan metrik konvensional yang butuh kunci jawaban (seperti Akurasi, Presisi, atau Recall). Anomaly Score adalah pengukuran matematis yang paling murni untuk melihat tingkat 'keterasingan' suatu titik gempa.\n\n")
    
    f.write("4. Bagaimana menentukan bahwa model sudah baik?\n")
    f.write("   (KURANG YAKIN)\n")
    f.write("   Model dianggap baik apabila Anomaly Score berhasil menarik batas ambang (threshold) yang secara tegas memisahkan sebagian kecil data (misal 1-5% gempa dengan kedalaman/kekuatan sangat tidak wajar) dari kerumunan besar rutinitas gempa dangkal/skala kecil.\n\n")
    
    f.write("\n\nH. Workflow Penelitian\n")
    f.write("Tuliskan seluruh penelitian dalam bentuk urutan langkah:\n\n")
    f.write("1. Pengumpulan Data: Mengunduh kumpulan data historis kegempaan (2008-2026) dari repositori BMKG.\n")
    f.write("2. Data Preprocessing: Membersihkan data mentah dari missing value/duplikasi, membuang kolom teks yang tak relevan, dan menormalisasi 4 atribut (Latitude, Longitude, Kedalaman, Magnitudo).\n")
    f.write("3. Pemodelan (Modeling): Melatih (training) algoritma Isolation Forest menggunakan dataset yang telah bersih untuk mengenali pola wajar kegempaan.\n")
    f.write("4. Evaluasi Model: Menganalisis sebaran Anomaly Score dan menetapkan batas ambang (threshold) untuk mengklasifikasi anomali vs normal.\n")
    f.write("5. Pengembangan Backend/API (KURANG YAKIN): Membangun jalur integrasi untuk melayani (serve) hasil deteksi model secara sistemik.\n")
    f.write("6. Pengembangan Aplikasi Frontend: Merancang dan membangun antarmuka Aplikasi AMANIN berbasis Android.\n")
    f.write("7. Integrasi & Pengujian Sistem: Mensimulasikan data gempa untuk memastikan aplikasi merespons output anomali dengan notifikasi proaktif dan penanda khusus (marker) di peta aplikasi.\n\n")
    
    f.write("\n\nJ. Kontribusi Penelitian\n")
    f.write("1. Apa kontribusi utama penelitian ini?\n")
    f.write("   Kontribusi utama penelitian ini adalah memecahkan masalah stagnasi informasi gempa (yang selama ini pasif), dengan menyajikan wawasan mitigasi proaktif yang diotaki oleh pendeteksian anomali Machine Learning (Isolation Forest).\n\n")
    
    f.write("2. Apakah fokus penelitian berada pada: algoritma, sistem, aplikasi, integrasi, atau lainnya?\n")
    f.write("   Fokus penelitian ini berada pada ranah **INTEGRASI**.\n\n")
    
    f.write("3. Mengapa?\n")
    f.write("   Karena kebaruan (novelty) tertinggi dalam penelitian ini bukanlah menciptakan algoritma deteksi yang benar-benar baru, dan bukan pula sekadar membuat aplikasi biasa. Fokus utamanya adalah pada **pengintegrasian** model kecerdasan buatan analitik berdimensi tinggi ke dalam lingkungan aplikasi mobile interaktif (Aplikasi AMANIN), sehingga wawasan data science yang rumit bisa langsung bermanfaat untuk peringatan dini masyarakat luas.\n")

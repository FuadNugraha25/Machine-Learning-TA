import codecs

with codecs.open(r"c:\Users\Fuad Nugraha\Documents\GitHub\Machine-Learning-TA\Anomaly Detection BMKG\jawaban_laporan.txt", "a", "utf-8") as f:
    f.write("\n\nE. Setelah Model Menghasilkan Output\n")
    f.write("Urutan proses setelah algoritma Isolation Forest menghasilkan output (berupa label prediksi dan anomaly score):\n\n")
    
    f.write("1. Penyimpanan Hasil ke Database (KURANG YAKIN)\n")
    f.write("   Output prediksi dari model kemungkinan besar disimpan terlebih dahulu ke dalam database di sisi backend. Hal ini diperlukan untuk merekam riwayat (history) kejadian gempa beserta status anomalinya agar dapat diakses kembali.\n\n")
    
    f.write("2. Pengiriman Data ke Backend / Aplikasi (KURANG YAKIN)\n")
    f.write("   Setelah diproses dan disimpan, hasil deteksi (berupa JSON/response API) dikirimkan dari server/backend menuju ke frontend antarmuka pengguna, yaitu Aplikasi AMANIN (Android).\n\n")
    
    f.write("3. Pemrosesan Logika Peringatan Dini (Trigger Notification) (KURANG YAKIN)\n")
    f.write("   Aplikasi menerima hasil tersebut. Jika data berlabel 'Anomali', aplikasi memproses logika lanjutan, seperti memicu (trigger) push notification, alarm, atau pop-up peringatan bahaya ke layar *smartphone* pengguna.\n\n")
    
    f.write("4. Visualisasi pada Peta Aplikasi\n")
    f.write("   Kejadian gempa divisualisasikan pada fitur peta (map) di dalam aplikasi. Untuk membedakannya secara visual, gempa berstatus anomali akan diberi penanda khusus (misalnya marker berwarna merah menyala), sedangkan gempa normal diberi penanda biasa.\n\n")
    
    f.write("5. Ditampilkan Sepenuhnya kepada Pengguna (Selesai)\n")
    f.write("   Siklus selesai ketika informasi mitigasi telah tersaji secara komprehensif. Pengguna kini tidak hanya melihat data mentah, melainkan menerima wawasan cerdas (insight) mengenai tingkat kewajaran gempa tersebut.\n")

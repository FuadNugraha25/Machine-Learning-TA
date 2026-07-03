import win32com.client
import sys

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
            
        print("Mencoba melakukan Undo...")
        # Lakukan Undo berulang kali sampai teks "Berdasarkan latar belakang yang telah diuraikan, rumusan masalah dalam penelitian ini difokuskan pada tiga poin utama:" menghilang dari dokumen.
        # Kita batasi maksimal 50 kali Undo agar aman.
        
        undo_count = 0
        success = False
        for i in range(100):
            # Cek apakah teks hasil inject kita masih ada di dokumen
            content = target_doc.Content.Text
            if "Berdasarkan latar belakang yang telah diuraikan, rumusan masalah dalam penelitian ini difokuskan pada tiga poin utama:" not in content:
                print(f"Berhasil mengembalikan dokumen setelah {undo_count} kali Undo.")
                success = True
                break
            
            # Lakukan 1 kali undo
            result = target_doc.Undo()
            if not result:
                print("Tidak bisa Undo lagi.")
                break
            undo_count += 1
            
        if not success:
            print(f"Selesai melakukan {undo_count} kali Undo, tapi teks masih ada atau limit tercapai.")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

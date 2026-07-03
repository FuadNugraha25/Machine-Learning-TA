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
            
        print("Mencoba Undo 1 kali untuk mengembalikan orientasi halaman...")
        result = target_doc.Undo()
        if result:
            print("Undo berhasil!")
        else:
            print("Gagal melakukan Undo.")
                
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

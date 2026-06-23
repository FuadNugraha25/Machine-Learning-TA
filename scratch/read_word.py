import win32com.client

word = win32com.client.Dispatch("Word.Application")
word.Visible = False
doc = word.Documents.Open(r'C:\Users\Fuad Nugraha\Documents\Laporan Tugas Akhir\Tugas Akhir Semester 8 AI.docx')
text = []
for i in range(1, min(100, doc.Paragraphs.Count + 1)):
    text.append(f"{i}: {doc.Paragraphs(i).Range.Text.strip()}")

doc.Close()
word.Quit()

with open('latar_belakang.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(text))

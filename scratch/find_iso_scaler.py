import json
import codecs
import re

def check_scaler():
    file_path = r'c:\Users\Fuad Nugraha\Documents\GitHub\Machine-Learning-TA\Anomaly Detection BMKG\isolation_forest.ipynb'
    with open(file_path, 'r', encoding='utf-8') as f:
        d = json.load(f)
        
    with codecs.open('scratch/output_iso.txt', 'w', 'utf-8') as out_f:
        for i, cell in enumerate(d.get('cells', [])):
            source = "".join(cell.get('source', []))
            if re.search(r'(scaler|scale|minmax|standard|robust)', source, re.IGNORECASE):
                out_f.write(f"--- Cell {i} ---\n")
                out_f.write(source + "\n")
                out_f.write("-----------------\n")

if __name__ == "__main__":
    check_scaler()

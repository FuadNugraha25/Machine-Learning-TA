"""
Ilustrasi Konseptual Distribusi Anomaly Score
Untuk Bab II.1.5 Isolation Forest

PENTING:
Data di script ini SINTETIS, dibuat cuma buat kebutuhan ilustrasi konsep.
Bukan data hasil training model Isolation Forest yang sebenarnya.
Bentuk distribusinya mengacu pada penjelasan teoritis anomaly score
di Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008), Isolation Forest,
2008 Eighth IEEE International Conference on Data Mining, 413-422.

Sesuai rumus s(x,n) di paper tersebut, skor mendekati 0.5 menandakan
data normal, sedangkan skor mendekati 1 menandakan anomali. Makanya
di sini data normal disimulasikan mengumpul di sekitar 0.5, dan
data anomali disimulasikan mengumpul lebih tinggi, mendekati 0.75.
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# Simulasi skor untuk data normal, mengumpul rapat di sekitar 0.5
normal_scores = np.random.normal(loc=0.50, scale=0.05, size=950)
normal_scores = np.clip(normal_scores, 0, 1)

# Simulasi skor untuk data anomali, jumlahnya sedikit dan terpisah jauh
anomaly_scores = np.random.normal(loc=0.75, scale=0.04, size=50)
anomaly_scores = np.clip(anomaly_scores, 0, 1)

all_scores = np.concatenate([normal_scores, anomaly_scores])

plt.figure(figsize=(8, 5))
plt.hist(all_scores, bins=40, color="#4C72B0", edgecolor="white")
plt.title("Ilustrasi Konseptual Distribusi Anomaly Score")
plt.xlabel("Anomaly Score")
plt.ylabel("Frekuensi")
plt.tight_layout()

output_path = "d:\\Github\\Machine-Learning-TA\\Anomaly Detection BMKG\\Ilustrasi Anomaly Score\\ilustrasi_anomaly_score.png"
plt.savefig(output_path, dpi=300)
print(f"Gambar tersimpan di {output_path}")
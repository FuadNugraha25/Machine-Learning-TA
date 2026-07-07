import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

file_path = '../data/bmkg/gabungan_2008_2025.csv'
df = pd.read_csv(file_path)
lat_min, lat_max = -11.0, 6.0
lon_min, lon_max = 95.0, 141.0
df = df[(df['latitude'] >= lat_min) & (df['latitude'] <= lat_max) &
        (df['longitude'] >= lon_min) & (df['longitude'] <= lon_max)]
df = df.dropna().reset_index(drop=True)

features = ['mag', 'depth', 'latitude', 'longitude']
X = df[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

contaminations = [0.001, 0.005, 0.01, 0.02, 0.05]
for cont in contaminations:
    iso = IsolationForest(contamination=cont, random_state=42)
    labels = iso.fit_predict(X_scaled)
    df_anomaly = df[labels == -1]
    
    print(f'=== Contamination: {cont} ===')
    print(f'Total Anomaly: {len(df_anomaly)}')
    print(f'Min/Max Mag: {df_anomaly["mag"].min()} / {df_anomaly["mag"].max()} (Mean: {df_anomaly["mag"].mean():.2f})')
    print(f'Min/Max Depth: {df_anomaly["depth"].min()} / {df_anomaly["depth"].max()} (Mean: {df_anomaly["depth"].mean():.2f})')
    print()


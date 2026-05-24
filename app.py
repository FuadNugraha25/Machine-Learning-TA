from flask import Flask, request, jsonify, send_from_directory
import joblib
import numpy as np
from datetime import datetime

app = Flask(__name__)
model        = joblib.load('model_gempa.pkl')
model_anomali = joblib.load('model_anomali.pkl')
scaler_anomali = joblib.load('scaler_anomali.pkl')

LABEL = {0: 'Low-magnitude', 1: 'High-magnitude'}
WARNA = {0: '#3388ff', 1: '#cc0000'}

LABEL_ANOMALI = {0: 'Normal', 1: 'Anomali'}
WARNA_ANOMALI = {0: '#3388ff', 1: '#cc0000'}

@app.route('/')
def index():
    return send_from_directory('.', 'prediksi.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/prediksi', methods=['POST'])
def prediksi():
    data = request.get_json()
    lat   = float(data['lat'])
    lon   = float(data['lon'])
    depth = float(data.get('depth', 10))
    now   = datetime.now()
    bulan = now.month
    jam   = now.hour

    fitur = np.array([[lat, lon, depth, bulan, jam]])
    kelas = int(model.predict(fitur)[0])
    proba = model.predict_proba(fitur)[0].tolist()

    return jsonify({
        'kelas': kelas,
        'label': LABEL[kelas],
        'warna': WARNA[kelas],
        'probabilitas': {LABEL[i]: round(p * 100, 1) for i, p in enumerate(proba)}
    })

@app.route('/prediksi-anomali', methods=['POST'])
def prediksi_anomali():
    data  = request.get_json()
    lat   = float(data['lat'])
    lon   = float(data['lon'])
    depth = float(data.get('depth', 10))
    gap   = float(data['gap'])   if data.get('gap')   else None
    dmin  = float(data['dmin'])  if data.get('dmin')  else None
    nst   = float(data['nst'])   if data.get('nst')   else None
    bulan = int(data.get('bulan', datetime.now().month))
    jam   = int(data.get('jam',   datetime.now().hour))

    # Median fallback jika kosong (nilai dari data training)
    gap_val  = gap  if gap  is not None else 149.0
    dmin_val = dmin if dmin is not None else 1.458
    nst_val  = nst  if nst  is not None else 20.0

    fitur = np.array([[lat, lon, depth, gap_val, dmin_val, nst_val, bulan, jam]])

    # XGBoost ditraining tanpa scaling — jangan di-scale
    kelas = int(model_anomali.predict(fitur)[0])
    proba = model_anomali.predict_proba(fitur)[0].tolist()

    return jsonify({
        'kelas': kelas,
        'label': LABEL_ANOMALI[kelas],
        'warna': WARNA_ANOMALI[kelas],
        'probabilitas': {LABEL_ANOMALI[i]: round(p * 100, 1) for i, p in enumerate(proba)}
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

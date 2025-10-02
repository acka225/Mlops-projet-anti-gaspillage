# api_flask_correct.py - CORRIGE LE CHEMIN
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app)

print("🔧 Recherche du modèle...")

# Essaye différents chemins possibles
model_paths = [
    'models/model.joblib',           # Structure standard
    '../models/model.joblib',        # Si API dans src/
    '../../models/model.joblib',     # Si profond
    'model.joblib',                  # Dans le dossier courant
    r'C:\Users\DELL\anti-gaspillage\models\model.joblib'  # Chemin absolu
]

model = None
for path in model_paths:
    try:
        model = joblib.load(path)
        print(f"✅ Modèle chargé depuis: {path}")
        break
    except:
        continue

if model is None:
    print("⚠️  Mode simulation - Modèle non trouvé")

@app.route('/')
def home():
    return jsonify({"message": "API Anti-Gaspillage 🚀", "status": "active", "model_loaded": model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        stock = data.get('stock_quantity', 50)
        expiration = data.get('expiration_days', 3)
        price = data.get('price', 5.0)
        sold = data.get('quantity_sold', 30)
        
        if model:
            features = [[stock, expiration, price, sold]]
            risk_score = model.predict(features)[0]
        else:
            # Mode simulation
            risk_score = (stock - sold) / expiration
        
        # Logique métier
        if risk_score > 15:
            level = "🚨 CRITIQUE"
            action = "Promotion 50% urgente"
        elif risk_score > 8:
            level = "⚠️ ÉLEVÉ"
            action = "Promotion 30% recommandée"
        elif risk_score > 3:
            level = "🔶 MODÉRÉ"
            action = "Surveillance renforcée"
        else:
            level = "✅ FAIBLE"
            action = "Niveau normal"
        
        return jsonify({
            "risk_score": round(risk_score, 2),
            "risk_level": level,
            "recommendation": action,
            "model_used": "real" if model else "simulation"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Remplacez la dernière ligne :
if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 8001))  # Utilise le port de l'env
    print(f"🚀 API Flask sur le port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)  # debug=False en production
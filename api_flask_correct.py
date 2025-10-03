# api_flask_correct.py - VERSION SANS scikit-learn
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import os

app = Flask(__name__)
CORS(app)

print("🚀 API Anti-Gaspillage démarrée - Mode Simulation Intelligent")

# Plus besoin de scikit-learn - mode simulation intelligent
model = None
print("🔧 Mode simulation intelligent activé")

@app.route('/')
def home():
    return jsonify({"message": "API Anti-Gaspillage 🚀", "status": "active", "mode": "simulation_intelligent"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        stock = data.get('stock_quantity', 50)
        expiration = data.get('expiration_days', 3)
        price = data.get('price', 5.0)
        sold = data.get('quantity_sold', 30)
        
        # Mode simulation intelligent avec logique métier
        base_risk = (stock - sold) / expiration
        
        # Ajouter des facteurs de risque supplémentaires
        price_factor = max(0.5, min(2.0, price / 10.0))  # Prix influence le risque
        demand_factor = sold / max(1, stock)  # Ratio demande/stock
        
        risk_score = base_risk * price_factor * (1 + (1 - demand_factor))
        
        # Logique métier améliorée
        if risk_score > 15:
            level = "🚨 CRITIQUE"
            action = "Promotion 50% urgente + Dons"
        elif risk_score > 8:
            level = "⚠️ ÉLEVÉ" 
            action = "Promotion 30% recommandée"
        elif risk_score > 3:
            level = "🔶 MODÉRÉ"
            action = "Promotion 15% ciblée"
        else:
            level = "✅ FAIBLE"
            action = "Niveau normal - Surveillance standard"
        
        return jsonify({
            "risk_score": round(risk_score, 2),
            "risk_level": level,
            "recommendation": action,
            "model_used": "simulation_intelligent",
            "details": {
                "stock": stock,
                "expiration_days": expiration,
                "quantity_sold": sold,
                "base_risk": round(base_risk, 2),
                "price_factor": round(price_factor, 2),
                "demand_factor": round(demand_factor, 2)
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PORT OPTIMISÉ pour Streamlit Cloud
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8502))
    print(f"🚀 API Flask sur http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
from flask import Flask, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)

# Données simulées
np.random.seed(42)
n_samples = 1000
dates = [datetime.now() - timedelta(days=x) for x in range(n_samples)]
categories = ['fruits', 'legumes', 'viande', 'poisson', 'produits_laitiers']
data = {
    'date': dates,
    'category': np.random.choice(categories, n_samples),
    'quantity_kg': np.random.exponential(2, n_samples),
    'price_euros': np.random.uniform(1, 50, n_samples),
    'reason': np.random.choice(['surstock', 'date_expiration', 'dommage', 'saison'], n_samples)
}
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Endpoint pour les statistiques
@app.route('/stats/', methods=['GET'])
def get_stats():
    return jsonify({
        'total_waste_kg': round(df['quantity_kg'].sum(), 2),
        'total_cost_cfa': round(df['price_euros'].sum() * 655.96, 2),
        'total_cost_euros': round(df['price_euros'].sum(), 2),
        'number_of_records': len(df)
    })

# Endpoint pour les catégories avec date
@app.route('/categories/', methods=['GET'])
def get_categories():
    category_stats = df.groupby('category').agg({'quantity_kg': 'sum', 'date': 'first'}).reset_index()
    return jsonify({'categories': category_stats.to_dict('records')})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
    import requests

def get_api_stats():
    """Récupère les statistiques depuis l'API Flask"""
    try:
        response = requests.get('http://localhost:8001/stats/')
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def get_api_categories():
    """Récupère les catégories depuis l'API Flask"""
    try:
        response = requests.get('http://localhost:8001/categories/')
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None
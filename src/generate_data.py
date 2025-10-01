import pandas as pd
import numpy as np
import os

def generate_urgent_data(n=500):
    """Génère des données supermarché réalistes"""
    os.makedirs('../data', exist_ok=True)
    
    dates = pd.date_range('2024-09-15', periods=n)
    categories = ['laitage', 'viande', 'legumes', 'fruits', 'boulangerie']
    
    data = {
        'date': dates,
        'product_id': np.random.randint(1, 50, n),
        'category': np.random.choice(categories, n),
        'quantity_sold': np.random.randint(0, 30, n),
        'stock_quantity': np.random.randint(5, 150, n),
        'expiration_days': np.random.randint(1, 10, n),
        'price': np.round(np.random.uniform(0.5, 15.0, n), 2),
        'promotion': np.random.choice([0, 1], n, p=[0.8, 0.2]),
        'day_of_week': np.random.randint(0, 7, n)
    }
    
    df = pd.DataFrame(data)
    # Calcul du risque de gaspillage
    df['waste_risk'] = ((df['stock_quantity'] - df['quantity_sold']) / df['expiration_days']).round(2)
    
    df.to_csv('../data/synthetic_data.csv', index=False)
    print(f" {n} lignes générées dans data/synthetic_data.csv")
    print(" Aperçu des données:")
    print(df.head())
    return df

if __name__ == "__main__":
    generate_urgent_data()
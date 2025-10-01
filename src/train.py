# train.py - VERSION CORRIGÉE
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

print(" ÉTAPE 1: ENTRAÎNEMENT DU MODÈLE CORRIGÉ")

# 1. CHARGER LES DONNÉES
print(" Chargement des données...")
df = pd.read_csv('../data/synthetic_data.csv')
print("Colonnes disponibles:", list(df.columns))

# 2. UTILISER LES BONNES COLONNES (adaptées à tes données)
# Si tes colonnes sont différentes, utilise celles-ci :
X = df[['stock_quantity', 'expiration_days', 'price', 'quantity_sold']]  # À ADAPTER
y = df['waste_risk']

print(f" {len(df)} produits chargés")
print(f"Features utilisées: {list(X.columns)}")

# 3. ENTRAÎNER LE MODÈLE
print(" Création et entraînement du modèle...")
model = RandomForestRegressor(n_estimators=50, random_state=42)
model.fit(X, y)

# 4. ÉVALUER LE MODÈLE
y_pred = model.predict(X)
mae = mean_absolute_error(y, y_pred)
r2 = r2_score(y, y_pred)

print(f" MAE: {mae:.3f}")
print(f" R² Score: {r2:.3f}")

# 5. SAUVEGARDER LE MODÈLE
print(" Sauvegarde...")
os.makedirs('../models', exist_ok=True)
joblib.dump(model, '../models/model.joblib')

# 6. TEST DE PRÉDICTION
test_pred = model.predict([[50, 3, 5.0, 40]])[0]  # stock, expiration, price, sold
print(f" Test: Stock 50, Expiration 3j → Risque: {test_pred:.2f}")

print(" ÉTAPE 1 TERMINÉE - MODÈLE CRÉÉ!")
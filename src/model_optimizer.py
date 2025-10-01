# model_optimizer.py
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
import numpy as np

print("🎯 ÉTAPE 2: OPTIMISATION DU MODÈLE")

# 1. CHARGER LES DONNÉES
df = pd.read_csv('../data/synthetic_data.csv')
X = df[['stock_quantity', 'expiration_days', 'price', 'quantity_sold']]
y = df['waste_risk']

print(f"📊 Données: {X.shape[0]} produits, {X.shape[1]} features")

# 2. TESTER DIFFÉRENTS MODÈLES
models = {
    'RandomForest_Basic': RandomForestRegressor(n_estimators=50, random_state=42),
    'RandomForest_Optimized': RandomForestRegressor(
        n_estimators=100, 
        max_depth=15,
        min_samples_split=3,
        random_state=42
    ),
    'GradientBoost': GradientBoostingRegressor(n_estimators=100, random_state=42)
}

# 3. ÉVALUATION PAR CROSS-VALIDATION
best_score = -np.inf
best_model_name = None

print("🔍 Évaluation des modèles...")
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, scoring='r2')
    mean_score = scores.mean()
    print(f"   {name}: R² = {mean_score:.3f} (+/- {scores.std() * 2:.3f})")
    
    if mean_score > best_score:
        best_score = mean_score
        best_model_name = name
        best_model = model

# 4. ENTRAÎNER LE MEILLEUR MODÈLE
print(f"🏆 Meilleur modèle: {best_model_name}")
best_model.fit(X, y)

# 5. SAUVEGARDER LE MODÈLE OPTIMISÉ
joblib.dump(best_model, '../models/optimized_model.joblib')
print(f"💾 Modèle optimisé sauvegardé: {best_model_name}")

# 6. COMPARAISON AVEC ANCIEN MODÈLE
old_model = joblib.load('../models/model.joblib')
old_score = cross_val_score(old_model, X, y, cv=5, scoring='r2').mean()

print(f"📈 Comparaison:")
print(f"   Ancien modèle: R² = {old_score:.3f}")
print(f"   Nouveau modèle: R² = {best_score:.3f}")
print(f"   Amélioration: {best_score - old_score:.3f}")

print("🎉 ÉTAPE 2 TERMINÉE - MODÈLE OPTIMISÉ!")
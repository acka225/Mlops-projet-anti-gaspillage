# analytics.py
import pandas as pd
import joblib
from prediction_service import WastePredictionService
import matplotlib.pyplot as plt
import os

print(" ÉTAPE 4: ANALYTICS ET RAPPORTS")

# 1. CHARGER LES DONNÉES ET MODÈLE
df = pd.read_csv('../data/synthetic_data.csv')
service = WastePredictionService()

print(f" Analyse de {len(df)} produits...")

# 2. ANALYSE COMPLÈTE DU DATASET
predictions = service.analyze_dataset(df)

# 3. STATISTIQUES GLOBALES
high_risk = [p for p in predictions if p['risk_level'] in [' CRITIQUE', ' ÉLEVÉ']]
moderate_risk = [p for p in predictions if p['risk_level'] == ' MODÉRÉ']
low_risk = [p for p in predictions if p['risk_level'] == ' FAIBLE']

print("\n STATISTIQUES DE RISQUE:")
print(f"    CRITIQUE/ ÉLEVÉ: {len(high_risk)} produits ({len(high_risk)/len(df)*100:.1f}%)")
print(f"    MODÉRÉ: {len(moderate_risk)} produits ({len(moderate_risk)/len(df)*100:.1f}%)")
print(f"    FAIBLE: {len(low_risk)} produits ({len(low_risk)/len(df)*100:.1f}%)")

# 4. ANALYSE PAR CATÉGORIE
if 'category' in df.columns:
    print("\n RISQUE PAR CATÉGORIE:")
    categories = df['category'].unique()
    for category in categories:
        cat_products = df[df['category'] == category]
        cat_predictions = service.analyze_dataset(cat_products)
        high_risk_cat = len([p for p in cat_predictions if p['risk_level'] in [' CRITIQUE', '⚠️ ÉLEVÉ']])
        print(f"   {category}: {high_risk_cat}/{len(cat_products)} à risque ({high_risk_cat/len(cat_products)*100:.1f}%)")

# 5. CALCUL ÉCONOMIES POTENTIELLES
total_potential_loss = 0
potential_savings = 0

for _, product in df.iterrows():
    risk_score = (product['stock_quantity'] - product['quantity_sold']) / product['expiration_days']
    potential_loss = risk_score * product['price']
    total_potential_loss += potential_loss
    
    # Économies avec promotions ciblées
    if risk_score > 8:
        potential_savings += potential_loss * 0.7  # 70% d'économies sur produits risqués

print(f"\n IMPACT FINANCIER:")
print(f"   Pertes potentielles totales: {total_potential_loss:.2f}€")
print(f"   Économies avec système IA: {potential_savings:.2f}€")
print(f"   Taux de réduction du gaspillage: {potential_savings/total_potential_loss*100:.1f}%")

# 6. PRODUITS PRIORITAires
print("\n TOP 5 PRODUITS PRIORITAIRES:")
high_risk_sorted = sorted(high_risk, key=lambda x: x['risk_score'], reverse=True)[:5]

for i, product in enumerate(high_risk_sorted, 1):
    print(f"   {i}. Risque: {product['risk_score']} - {product['risk_level']}")
    print(f"      → {product['recommendation']}")

# 7. SAUVEGARDER RAPPORT
os.makedirs('../reports', exist_ok=True)
report_path = '../reports/analytics_report.txt'

with open(report_path, 'w', encoding='utf-8') as f:
    f.write(" RAPPORT ANTI-GASPILLAGE - ANALYTICS\n")
    f.write("=" * 50 + "\n")
    f.write(f"Produits analysés: {len(df)}\n")
    f.write(f"Produits à risque élevé: {len(high_risk)} ({len(high_risk)/len(df)*100:.1f}%)\n")
    f.write(f"Pertes potentielles: {total_potential_loss:.2f}€\n")
    f.write(f"Économies potentielles: {potential_savings:.2f}€\n")
    f.write(f"Réduction gaspillage: {potential_savings/total_potential_loss*100:.1f}%\n\n")
    
    f.write(" PRODUITS PRIORITAIRES:\n")
    for i, product in enumerate(high_risk_sorted, 1):
        f.write(f"{i}. Risque: {product['risk_score']} - {product['recommendation']}\n")

print(f"\n Rapport sauvegardé: {report_path}")
print(" ÉTAPE 4 TERMINÉE - ANALYTICS COMPLÈTES!")
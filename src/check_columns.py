# check_columns.py - CRÉER CE FICHIER
import pandas as pd

print("🔍 VÉRIFICATION DES COLONNES DISPONIBLES")

df = pd.read_csv('../data/synthetic_data.csv')
print("Colonnes disponibles:", list(df.columns))
print("\nAperçu des données:")
print(df.head())
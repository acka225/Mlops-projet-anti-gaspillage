# prepare_for_b.py - CRÉER CE FICHIER MAINTENANT
import os
import shutil

print(" PRÉPARATION DES FICHIERS POUR B")
print("=" * 50)

# Liste des fichiers à envoyer à B
files_to_send = [
    '../data/synthetic_data.csv',
    '../models/model.joblib',
    'prediction_service.py',
    '../reports/analytics_report.txt'
]

# Vérifier chaque fichier
print(" FICHIERS À ENVOYER À B:")
all_files_exist = True

for file_path in files_to_send:
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path) / 1024  # Taille en KB
        print(f"    {file_path} ({file_size:.1f} KB)")
    else:
        print(f"    {file_path} (MANQUANT)")
        all_files_exist = False

print("\n INSTRUCTIONS D'ENVOI:")
print("1.  METHODES D'ENVOI:")
print("   • Email avec pièces jointes")
print("   • Google Drive/OneDrive")
print("   • WhatsApp/Telegram (fichiers individuels)")
print("   • GitHub si configuré")

print("\n2.  STRUCTURE POUR B:")
print("   B doit créer cette structure:")
print("   anti-gaspillage/")
print("   ├── data/")
print("   │   └── synthetic_data.csv")
print("   ├── models/")
print("   │   └── model.joblib")
print("   ├── src/")
print("   │   └── prediction_service.py")
print("   └── reports/")
print("       └── analytics_report.txt")

print("\n3.  MESSAGE À ENVOYER À B:")
print("""
 PARTIE ML TERMINÉE - PRÊTE POUR INTÉGRATION !

 RÉSULTATS OBTENUS :
• Modèle entraîné : R² = 0.998 (excellent)
• 66.9% de réduction du gaspillage possible
• 52 012€ d'économies potentielles identifiées
• Catégorie critique : Boulangerie (40.4% à risque)

 FICHIERS INCLUS :
- synthetic_data.csv (500 produits)
- model.joblib (modèle optimisé)
- prediction_service.py (service de prédiction)
- analytics_report.txt (analyse complète)

 POUR B :
1. Placer les fichiers dans ta structure
2. Utiliser prediction_service.py dans ton API
3. Tester avec les données fournies

 On se retrouve à 14h pour l'intégration !
""")

if all_files_exist:
    print(" TOUS LES FICHIERS SONT PRÊTS À ÊTRE ENVOYÉS !")
else:
    print("  CERTAINS FICHIERS MANQUENT - VÉRIFIE LA STRUCTURE")
# prediction_service.py
import joblib
import pandas as pd

class WastePredictionService:
    def __init__(self, model_path='../models/optimized_model.joblib'):
        try:
            self.model = joblib.load(model_path)
            print(" Service de prédiction initialisé avec modèle optimisé")
        except:
            # Fallback sur le modèle de base
            self.model = joblib.load('../models/model.joblib')
            print(" Service de prédiction initialisé avec modèle de base")
    
    def predict_single(self, stock_quantity, expiration_days, price, quantity_sold):
        """Prédire le risque pour un seul produit"""
        features = [[stock_quantity, expiration_days, price, quantity_sold]]
        risk_score = self.model.predict(features)[0]
        
        # Logique métier basée sur tes données
        if risk_score > 15:
            level = " CRITIQUE"
            action = "PROMOTION URGENTE 50% - Risque très élevé"
            discount = "50%"
        elif risk_score > 8:
            level = " ÉLEVÉ" 
            action = "Promotion 30% recommandée"
            discount = "30%"
        elif risk_score > 3:
            level = " MODÉRÉ"
            action = "Surveillance renforcée - Promotion 15% envisageable"
            discount = "15%"
        else:
            level = " FAIBLE"
            action = "Niveau normal - Aucune action nécessaire"
            discount = "0%"
        
        return {
            'risk_score': round(risk_score, 2),
            'risk_level': level,
            'recommendation': action,
            'suggested_discount': discount,
            'features_used': {
                'stock_quantity': stock_quantity,
                'expiration_days': expiration_days,
                'price': price,
                'quantity_sold': quantity_sold
            }
        }
    
    def predict_batch(self, products_list):
        """Prédire pour plusieurs produits"""
        return [self.predict_single(**product) for product in products_list]
    
    def analyze_dataset(self, df):
        """Analyser un dataset complet"""
        predictions = []
        for _, row in df.iterrows():
            pred = self.predict_single(
                row['stock_quantity'],
                row['expiration_days'], 
                row['price'],
                row['quantity_sold']
            )
            pred['product'] = row['product_id'] if 'product_id' in df.columns else 'Unknown'
            pred['category'] = row['category'] if 'category' in df.columns else 'Unknown'
            predictions.append(pred)
        return predictions

# TEST DU SERVICE
if __name__ == "__main__":
    print(" ÉTAPE 3: TEST DU SERVICE DE PRÉDICTION")
    
    service = WastePredictionService()
    
    # Test single
    print("\n Test single prediction:")
    result = service.predict_single(100, 2, 4.5, 60)
    for key, value in result.items():
        print(f"   {key}: {value}")
    
    # Test batch
    print("\n Test batch prediction:")
    products = [
        {'stock_quantity': 50, 'expiration_days': 3, 'price': 5.0, 'quantity_sold': 40},
        {'stock_quantity': 80, 'expiration_days': 1, 'price': 2.0, 'quantity_sold': 50},
        {'stock_quantity': 30, 'expiration_days': 5, 'price': 8.0, 'quantity_sold': 25}
    ]
    
    batch_results = service.predict_batch(products)
    for i, result in enumerate(batch_results):
        print(f"   Produit {i+1}: {result['risk_level']} (Score: {result['risk_score']})")
        print(f"      → {result['recommendation']}")
    
    print(" ÉTAPE 3 TERMINÉE - SERVICE FONCTIONNEL!")
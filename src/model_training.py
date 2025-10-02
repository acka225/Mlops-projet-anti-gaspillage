import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

class DemandPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.features = []
        
    def prepare_features(self, df):
        df = df.copy()
        
        # Vérifier et corriger les noms de colonnes
        if 'date' not in df.columns and 'Date' in df.columns:
            df = df.rename(columns={'Date': 'date'})
        if 'category' not in df.columns and 'Produit' in df.columns:
            df = df.rename(columns={'Produit': 'category'})
        if 'quantity_sold' not in df.columns and 'Ventes' in df.columns:
            df = df.rename(columns={'Ventes': 'quantity_sold'})
        if 'price' not in df.columns and 'Prix' in df.columns:
            df = df.rename(columns={'Prix': 'price'})
        
        # Créer les colonnes manquantes avec des valeurs par défaut
        if 'promotion' not in df.columns:
            df['promotion'] = 0
        if 'weather_effect' not in df.columns:
            df['weather_effect'] = 1.0
        
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        
        feature_columns = [
            'day_of_week', 'month', 'is_weekend', 
            'price', 'promotion', 'weather_effect'
        ]
        
        category_dummies = pd.get_dummies(df['category'], prefix='cat')
        
        self.features = feature_columns + list(category_dummies.columns)
        X = pd.concat([df[feature_columns], category_dummies], axis=1)
        y = df['quantity_sold']
        
        return X, y
    
    def train(self, df):
        print('Entraînement du modèle de prédiction de demande...')
        
        X, y = self.prepare_features(df)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print(f'MAE: {mae:.2f}, RMSE: {rmse:.2f}')
        
        # Créer le dossier models s'il n'existe pas
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, 'models/demand_predictor.pkl')
        print('Modèle sauvegardé')
        
        return mae, rmse
    
    def predict_demand(self, product_data):
        try:
            model = joblib.load('models/demand_predictor.pkl')
            
            df = pd.DataFrame([product_data])
            df['date'] = pd.to_datetime(df['date'])
            df['day_of_week'] = df['date'].dt.dayofweek
            df['month'] = df['date'].dt.month
            df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
            
            feature_columns = ['day_of_week', 'month', 'is_weekend', 'price', 'promotion', 'weather_effect']
            category_dummies = pd.get_dummies(df['category'], prefix='cat')
            
            X_pred = pd.concat([df[feature_columns], category_dummies], axis=1)
            
            # Obtenir les caractéristiques attendues du modèle entraîné
            expected_features = self.features
            
            for col in expected_features:
                if col not in X_pred.columns:
                    X_pred[col] = 0
            
            X_pred = X_pred[expected_features]
            
            prediction = model.predict(X_pred)[0]
            return max(0, int(prediction))
            
        except Exception as e:
            print(f'Erreur de prédiction: {e}')
            return None

def create_sample_data():
    """Crée un fichier de données d'exemple pour l'anti-gaspillage"""
    np.random.seed(42)
    
    dates = pd.date_range('2023-01-01', '2023-04-10')
    categories = ['Lait', 'Pain', 'Yaourt', 'Fromage', 'Fruits', 'Légumes']
    
    data = []
    for date in dates:
        for category in categories:
            data.append({
                'date': date,
                'category': category,
                'quantity_sold': np.random.randint(10, 100),
                'price': np.random.uniform(0.5, 5.0),
                'promotion': np.random.choice([0, 1], p=[0.7, 0.3]),
                'weather_effect': np.random.uniform(0.8, 1.2)
            })
    
    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    # Créer le dossier data s'il n'existe pas
    os.makedirs('data', exist_ok=True)
    
    # Essayer de lire le fichier, le créer s'il n'existe pas
    try:
        df = pd.read_csv('data/supermarket_sales.csv')
        print("Fichier de données chargé avec succès !")
    except FileNotFoundError:
        print("Création du fichier de données d'exemple...")
        df = create_sample_data()
        df.to_csv('data/supermarket_sales.csv', index=False)
        print("Fichier data/supermarket_sales.csv créé avec succès !")
    
    # Afficher les premières lignes pour vérification
    print("\Aperçu des données:")
    print(df.head())
    print(f"\nTaille du dataset : {df.shape}")
    print(f"Colonnes : {df.columns.tolist()}")
    
    # Entraîner le modèle
    predictor = DemandPredictor()
    mae, rmse = predictor.train(df)
    
    # Tester une prédiction
    test_data = {
        'date': '2023-04-11',
        'category': 'Lait',
        'price': 1.5,
        'promotion': 0,
        'weather_effect': 1.0
    }
    
    prediction = predictor.predict_demand(test_data)
    print(f"\nTest de prédiction pour Lait: {prediction} unités")
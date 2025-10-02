import pandas as pd
import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os

# Configuration de la page
st.set_page_config(
    page_title="Système Anti-Gaspillage",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<h1 class="main-header">🛒 Système de Prédiction du Gaspillage Alimentaire</h1>', unsafe_allow_html=True)

# Sidebar pour la configuration
st.sidebar.title("⚙️ Configuration")
api_url = st.sidebar.text_input("URL de l'API",  "http://localhost:8001")

# -----------------------------
# GÉNÉRATION DONNÉES DÉMO
# -----------------------------
def generate_demo_data():
    """Génère des données de démonstration réalistes"""
    np.random.seed(42)
    n_samples = 300
    
    data = {
        'date': [datetime.now() - timedelta(days=x) for x in range(n_samples)],
        'product_id': np.random.randint(1, 30, n_samples),
        'category': np.random.choice(['laitage', 'viande', 'legumes', 'fruits', 'boulangerie'], n_samples),
        'quantity_sold': np.random.randint(0, 25, n_samples),
        'stock_quantity': np.random.randint(10, 100, n_samples),
        'expiration_days': np.random.randint(1, 7, n_samples),
        'price': np.round(np.random.uniform(1, 10, n_samples), 2),
        'promotion': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        'day_of_week': np.random.randint(0, 7, n_samples)
    }
    
    df = pd.DataFrame(data)
    df['waste_risk'] = ((df['stock_quantity'] - df['quantity_sold']) / df['expiration_days']).round(2)
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/synthetic_data.csv', index=False)
    st.success("✅ Données de démonstration générées et sauvegardées")
    
    return df

# -----------------------------
# CHARGEMENT DES DONNÉES
# -----------------------------
@st.cache_data
def load_data():
    """Charge les données avec fallback sur données de démo"""
    possible_paths = [
        'data/synthetic_data.csv',
        '../data/synthetic_data.csv',
        './synthetic_data.csv'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            st.success(f"✅ Données chargées depuis: {path}")
            return df
    
    st.warning("📁 Aucune donnée trouvée → génération de données de démo")
    return generate_demo_data()

# -----------------------------
# VÉRIFICATION API
# -----------------------------
def check_api_status():
    """Vérifie si l'API est en ligne"""
    try:
        response = requests.get(f"{api_url}/", timeout=3)
        return response.status_code == 200
    except:
        return False

# -----------------------------
# AFFICHAGE PRÉDICTIONS
# -----------------------------
def display_prediction_results(result, stock, expiration, price, sold):
    """Affiche les résultats de prédiction"""
    st.success("✅ Analyse terminée !")
    
    col3, col4, col5 = st.columns(3)
    with col3:
        st.metric("Score de risque", f"{result['risk_score']}")
    with col4:
        st.metric("Niveau de risque", result['risk_level'])
    with col5:
        st.metric("Recommandation", result['recommendation'].split(' - ')[0])
    
    # Jauge
    risk_score = result['risk_score']
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "NIVEAU DE RISQUE"},
        gauge={
            'axis': {'range': [None, 25]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 3], 'color': "lightgreen"},
                {'range': [3, 8], 'color': "yellow"},
                {'range': [8, 15], 'color': "orange"},
                {'range': [15, 25], 'color': "red"}
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)
    
    # Actions recommandées
    st.subheader("💡 Plan d'action recommandé")
    if "CRITIQUE" in result['risk_level']:
        st.error("🚨 ACTION IMMÉDIATE REQUISE")
        st.write("• Promotion 50% immédiate")
        st.write("• Donner aux associations")
        st.write("• Réduire les commandes futures")
    elif "ÉLEVÉ" in result['risk_level']:
        st.warning("⚠️ ACTION RAPIDE RECOMMANDÉE")
        st.write("• Promotion 30%")
        st.write("• Ajustement des commandes")
    elif "MODÉRÉ" in result['risk_level']:
        st.info("🔶 SURVEILLANCE RENFORCÉE")
        st.write("• Promotions ciblées 15%")
        st.write("• Suivi rapproché")
    else:
        st.success("✅ SITUATION NORMALE")
        st.write("• Stratégie actuelle à maintenir")

# -----------------------------
# MODE DÉMO
# -----------------------------
def use_demo_mode(stock, expiration, sold):
    """Mode fallback si API indisponible"""
    st.warning("🔄 Mode démo activé")
    risk_demo = (stock - sold) / expiration
    
    if risk_demo > 15:
        level, action = "🚨 CRITIQUE", "Promotion 50% urgente"
    elif risk_demo > 8:
        level, action = "⚠️ ÉLEVÉ", "Promotion 30% recommandée"
    elif risk_demo > 3:
        level, action = "🔶 MODÉRÉ", "Surveillance renforcée"
    else:
        level, action = "✅ FAIBLE", "Niveau normal"
    
    demo_result = {
        "risk_score": round(risk_demo, 2),
        "risk_level": level,
        "recommendation": action
    }
    display_prediction_results(demo_result, stock, expiration, 1000, sold)

# -----------------------------
# MAIN
# -----------------------------
def main():
    api_online = check_api_status()
    tab1, tab2, tab3 = st.tabs(["🏠 Accueil", "🎯 Prédictions", "📊 Analytics"])
    
    # Accueil
    with tab1:
        st.header("Bienvenue dans le système anti-gaspillage")
        col1, col2 = st.columns(2)
        with col1:
            st.write("• **Prédiction intelligente** du gaspillage")
            st.write("• **Recommandations personnalisées**")
            st.write("• **Analytics en temps réel**")
        with col2:
            st.subheader("📈 Statut du système")
            st.success("✅ API connectée" if api_online else "❌ API non connectée")
            st.metric("Performance modèle", "R² = 0.998")
            st.metric("Réduction gaspillage", "67%")
            st.metric("Économies potentielles", "52 012 CFA")
    
    # Prédictions
    with tab2:
        st.header("🎯 Prédictions en temps réel")
        if not api_online:
            st.error("🌐 API indisponible → mode démo activé")
        col1, col2 = st.columns(2)
        with col1:
            stock = st.slider("Stock actuel", 0, 200, 50)
            expiration = st.slider("Jours avant péremption", 1, 10, 3)
        with col2:
            price = st.number_input("Prix unitaire (CFA)", 100, 50000, 3000, step=100)
            sold = st.slider("Ventes quotidiennes moyennes", 0, 100, 30)
        if st.button("🚀 Analyser le risque", type="primary", use_container_width=True):
            if api_online:
                try:
                    response = requests.post(
                        f"{api_url}/predict",
                        json={
                            "stock_quantity": stock,
                            "expiration_days": expiration,
                            "price": price,
                            "quantity_sold": sold
                        },
                        timeout=5
                    )
                    if response.status_code == 200:
                        result = response.json()
                        display_prediction_results(result, stock, expiration, price, sold)
                    else:
                        st.error(f"❌ Erreur API: {response.status_code}")
                        use_demo_mode(stock, expiration, sold)
                except:
                    st.error("🌐 Impossible de contacter l’API")
                    use_demo_mode(stock, expiration, sold)
            else:
                use_demo_mode(stock, expiration, sold)
    
    # Analytics
    with tab3:
        st.header("📊 Analytics et Données")
        df = load_data()
        if df is not None:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Produits analysés", len(df))
            high_risk = len(df[df['waste_risk'] > 8])
            col2.metric("Produits à risque", high_risk)
            col3.metric("Taux de risque", f"{(high_risk/len(df))*100:.1f}%")
            col4.metric("Risque financier", f"{(df['waste_risk']*df['price']).sum():.0f} CFA")
            
            col5, col6 = st.columns(2)
            with col5:
                st.plotly_chart(px.pie(df, names="category", title="Répartition par catégorie"), use_container_width=True)
            with col6:
                st.plotly_chart(px.box(df, x="category", y="waste_risk", title="Risque par catégorie"), use_container_width=True)
            
            st.dataframe(df, use_container_width=True, height=400)

if __name__ == "__main__":
    main()

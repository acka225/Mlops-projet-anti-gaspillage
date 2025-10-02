import subprocess
import threading
import time
import os
import signal
import sys

# Démarrer Flask en arrière-plan
def start_flask():
    try:
        # Sur Streamlit Cloud, on utilise le port 8502 pour éviter les conflits
        os.environ['FLASK_PORT'] = '8502'
        subprocess.Popen([
            sys.executable, "api_flask_correct.py"
        ])
        print("🚀 Flask API démarrée")
    except Exception as e:
        print(f"❌ Erreur démarrage Flask: {e}")

# Démarrer Flask au lancement
if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Attendre que Flask soit prêt
    time.sleep(5)
    
    # Importer et exécuter l'app Streamlit
    try:
        from streamlit_app import main
        print("✅ Streamlit app importée")
        main()
    except Exception as e:
        print(f"❌ Erreur Streamlit: {e}")
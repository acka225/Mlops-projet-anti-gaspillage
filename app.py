import subprocess
import time
import sys

def start_flask():
    try:
        print("🚀 Démarrage de l'API Flask...")
        process = subprocess.Popen([sys.executable, "api_flask_correct.py"])
        return process
    except Exception as e:
        print(f"❌ Erreur Flask: {e}")
        return None

def main():
    flask_process = start_flask()
    time.sleep(3)
    
    try:
        print("✅ Lancement de Streamlit...")
        from streamlit_app import main as streamlit_main
        streamlit_main()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        if flask_process:
            flask_process.terminate()

if __name__ == "__main__":
    main()
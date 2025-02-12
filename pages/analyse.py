import streamlit as st
import requests
import time

# URLs pour envoyer la requête et récupérer les résultats
N8N_REQUEST_URL = "https://matin.app.n8n.cloud/webhook-test/ea2dfa42-51b4-410c-a9c5-7192a9a0dbd9"


def get_results():
    """Récupère les résultats envoyés par n8n"""
    try:
        response = requests.get(N8N_REQUEST_URL)
        if response.status_code == 200:
            return response.json().get("data", "Aucune donnée disponible.")
        return None
    except Exception as e:
        return f"Erreur lors de la récupération des résultats : {e}"

def analyse_agent():
    """Page dédiée à l'agent d'analyse."""
    st.title("📊 Agent d'Analyse")
    st.write("Posez une question pour analyser les données des restaurants.")

    user_query = st.text_input("💬 Posez votre question :", placeholder="Exemple : Analyse les avis du restaurant XYZ.")

    if st.button("Envoyer"):
        if user_query.strip():
            try:
                # Envoi de la requête à n8n
                response = requests.post(N8N_REQUEST_URL, json={"query": user_query})
                
                if response.status_code == 200:
                    st.success("Requête envoyée avec succès ! 📡")
                    st.write("🔄 Attente des résultats...")

                    # Attente en boucle pour récupérer les résultats (Polling)
                    with st.spinner("Analyse en cours..."):
                        for i in range(10):  # Attente max de 10 itérations (ajuster si besoin)
                            time.sleep(2)  # Pause pour éviter de surcharger le serveur
                            result = get_results()
                            if result and result != "Aucune donnée disponible.":
                                st.success("✅ Résultats reçus :")
                                st.write(result)
                                break
                        else:
                            st.warning("⚠️ Temps d'attente dépassé, réessayez plus tard.")
                else:
                    st.error(f"Erreur ({response.status_code}) : {response.text}")

            except Exception as e:
                st.error(f"Erreur : {e}")
        else:
            st.error("Veuillez entrer une requête valide.")

if __name__ == "__main__":
    analyse_agent()

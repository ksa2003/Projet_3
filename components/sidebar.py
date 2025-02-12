import streamlit as st
import requests  # Pour appeler les webhooks dans n8n

# Fonction pour déclencher les workflows dans n8n
def trigger_n8n_webhook(webhook_url):
    try:
        response = requests.post(webhook_url)
        if response.status_code == 200:
            st.sidebar.success(f"Workflow déclenché avec succès !")
        else:
            st.sidebar.error(f"Erreur lors du déclenchement : Statut {response.status_code}")
    except Exception as e:
        st.sidebar.error(f"Erreur : {e}")

# Fonction pour gérer la sidebar et stocker l'agent sélectionné dans les query params
def render_sidebar():
    st.sidebar.title("Actions disponibles")

    # Boutons pour accéder aux pages dédiées
    if st.sidebar.button("Recherche avancée"):
        st.switch_page("pages/recherche.py")

    if st.sidebar.button("Analyse des avis"):
        st.switch_page("pages/analyse.py")

    if st.sidebar.button("Recommandations"):
        st.switch_page("pages/recommendation.py")

    if st.sidebar.button("Recherche par image"):
        st.switch_page("pages/image_search.py")


if __name__ == "__main__":
    render_sidebar()

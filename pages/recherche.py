import streamlit as st
import requests

def recherche_agent():
    """
    Page dédiée à l'agent de recherche.
    """
    st.title("🔍 Agent de Recherche")
    st.write("Posez une question pour rechercher des restaurants.")

    user_query = st.text_input("💬 Posez votre question :", placeholder="Exemple : Quels restaurants sont ouverts maintenant ?")

    if st.button("Envoyer"):
        if user_query.strip():
            try:
                response = requests.post(
                    "https://matin.app.n8n.cloud/webhook-test/66033b5c-4237-4f51-b4b6-3a9892dc1b50",
                    json={"query": user_query}
                )
                if response.status_code == 200:
                    st.success("Réponse :")
                    st.write(response.json().get("response", "Aucune réponse reçue."))
                else:
                    st.error(f"Erreur ({response.status_code}) : {response.text}")
            except Exception as e:
                st.error(f"Erreur : {e}")
        else:
            st.error("Veuillez entrer une requête valide.")

if __name__ == "__main__":
    recherche_agent()

import streamlit as st
import requests

def recommendation_agent():
    """
    Page dédiée à l'agent de recommandations.
    """
    st.title("✨ Agent de Recommandations")
    st.write("Posez une question pour obtenir des recommandations.")

    user_query = st.text_input("💬 Posez votre question :", placeholder="Exemple : Recommande-moi un restaurant romantique.")

    if st.button("Envoyer"):
        if user_query.strip():
            try:
                response = requests.post(
                    "https://matin.app.n8n.cloud/webhook-test/f280c154-93cf-4320-8ece-7f4cfccf66ed",
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
    recommendation_agent()

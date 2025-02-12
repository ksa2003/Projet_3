import streamlit as st
import requests
from PIL import Image
from io import BytesIO

def image_search_agent():
    """
    Page dédiée à l'agent de recherche par image.
    """
    st.title("🖼️ Agent de Recherche par Image")
    st.write("Téléversez une image pour rechercher des restaurants similaires.")

    # Téléversement de l'image
    uploaded_file = st.file_uploader("📤 Téléversez une image :", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        # Afficher un aperçu de l'image
        image = Image.open(uploaded_file)
        st.image(image, caption="📷 Aperçu de l'image téléversée", use_container_width=True)

        # Activer le bouton uniquement si une image est chargée
        send_button = st.button("📡 Envoyer")

        if send_button:
            try:
                # Convertir l'image en fichier binaire
                img_buffer = BytesIO()
                image.save(img_buffer, format=image.format)  # Utiliser le format original
                img_buffer.seek(0)  # Remettre le pointeur au début du fichier

                # Création du payload avec un fichier binaire
                files = {
                    "file": (uploaded_file.name, img_buffer, uploaded_file.type)  # (nom, contenu, type MIME)
                }

                # Envoi à n8n via Webhook (directement en binaire)
                response = requests.post(
                    "https://matin.app.n8n.cloud/webhook-test/97cd1bb3-6cee-4fdd-9638-afa4904edb1c",
                    files=files  # Envoi du fichier binaire au lieu de JSON
                )

                # Affichage de la réponse
                if response.status_code == 200:
                    st.success("✅ Réponse reçue :")
                    st.json(response.json())  # Affiche proprement le JSON de réponse
                else:
                    st.error(f"❌ Erreur ({response.status_code}) : {response.text}")
            except Exception as e:
                st.error(f"⚠️ Erreur : {e}")

if __name__ == "__main__":
    image_search_agent()

import streamlit as st
st.set_page_config(layout="wide",initial_sidebar_state="collapsed")  
import pandas as pd
from rapidfuzz import process  
from components.sidebar import render_sidebar





def load_css():
    with open("css/style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Charger les données des restaurants depuis le CSV avec cache
@st.cache_data
def load_restaurants():
    return pd.read_csv("data/restautants_avec_photos_v2.csv")

def show_home():
    # Charger le CSS
    load_css()
    render_sidebar()

    if "user" not in st.session_state:
        st.switch_page("main.py")  
        st.stop()

    user = st.session_state["user"]
    st.title("🏠 Home - Restaurant List")
    st.subheader(f"Welcome, {user['role']}!")

    # Bouton de déconnexion
    if st.button("Logout", key="logout_button"):
        st.session_state.clear()
        st.switch_page("main.py")

    # Charger les données des restaurants
    df = load_restaurants()

    # Ajout d'un champ de recherche
    search_query = st.text_input("🔍 Rechercher un restaurant :", "")

    if search_query:
        
        results = process.extract(
            search_query,  # Terme de recherche
            df["name"],  # Liste des noms de restaurants
            limit=20,  # Nombre maximal de résultats
            
        )

        # Filtrer les restaurants basés sur les résultats flous
        matching_names = [match[0] for match in results if match[1] > 60]  # Score de similarité > 60
        df = df[df["name"].isin(matching_names)]

    # Limiter à 20 restaurants après recherche
    df = df.head(20)

    # Affichage des restaurants sous forme de cartes
    for _, row in df.iterrows():
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 4, 1])  

        # Colonne 1 : Image du restaurant
        with col1:
            if pd.notna(row["image_url"]):  # Vérifier si l'image existe
                st.image(row["image_url"], use_container_width=True)

        # Colonne 2 : Informations principales
        with col2:
            st.subheader(row["name"])
            st.write(f"📍 **Adresse :** {row['Exact_Address']}")
            st.write(f"⭐ **Note :** {row['rating']}/5")

            # Vérification et formatage du type de cuisine
            if isinstance(row["categories_list"], str):
                # Si c'est une chaîne JSON ou similaire (par ex. "['French', 'Italian']")
                try:
                    import ast  # Utiliser ast pour convertir une chaîne ressemblant à une liste en liste
                    categories = ast.literal_eval(row["categories_list"])
                    cuisines = ", ".join(categories)
                except:
                    cuisines = row["categories_list"]  # Si ce n'est pas une liste valide, garder la chaîne brute
            elif isinstance(row["categories_list"], list):
                # Si c'est déjà une liste
                cuisines = ", ".join(row["categories_list"])
            else:
                cuisines = "Non spécifié"  # Si aucune donnée valide

            st.write(f"🍽 **Type de cuisine :** {cuisines}")

        # Colonne 3 : Bouton "Voir détails"
        with col3:
            if st.button(f"Voir détails", key=row["id"]):
                st.switch_page("pages/restaurant.py")  # Redirige vers la page de détails (à créer)

if __name__ == "__main__":
    show_home()

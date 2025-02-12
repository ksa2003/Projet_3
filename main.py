import streamlit as st
from backend_.auth import signup_user, login_user

def login():
    st.title("🔐 Authentication")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # Vérifier si l'utilisateur est déjà connecté
    if "user" in st.session_state:
        st.switch_page("pages/home.py")  # Redirige vers la page d'accueil directement

    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            result = login_user(email, password)
            if result["success"]:
                #  Stocker les infos de l'utilisateur dans `st.session_state`
                st.session_state["user"] = result["user"]
                st.session_state["authenticated"] = True

                # Redirection vers la page d'accueil
                st.switch_page("pages/home.py")
            else:
                st.error(result["error"])

    with tab2:
        st.subheader("Sign Up")
        new_email = st.text_input("New Email", key="signup_email")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        role = st.selectbox("Role", ["Client", "Restaurateur"])

        if st.button("Sign Up"):
            response = signup_user(new_email, new_password, role)
            
            if response["success"]:
                st.success("Account created successfully! You can now log in.")

                # Stocker les infos dans `st.session_state` après inscription
                st.session_state["user"] = {
                    "email": new_email,
                    "role": role
                }
                st.session_state["authenticated"] = True

                #  Redirection vers la page d'accueil
                st.switch_page("pages/home.py")
            else:
                st.error(response["error"])


if __name__ == "__main__":
    login()

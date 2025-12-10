import streamlit as st

def check_authentication():
    """Vérifie si l'utilisateur est connecté"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    return st.session_state.authenticated

def login_user(email, password):
    """Simule la connexion d'un utilisateur"""
    # Pour l'instant, simulation simple
    if email and password:
        st.session_state.authenticated = True
        st.session_state.user_email = email
        return True
    return False

def logout_user():
    """Déconnecte l'utilisateur"""
    st.session_state.authenticated = False
    st.session_state.user_email = None
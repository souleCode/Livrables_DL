import streamlit as st
import os
from utils.auth import check_authentication
from components.sidebar import render_sidebar
import base64

# Configuration de la page
st.set_page_config(
    page_title="ML Boost Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Charger le CSS personnalisé
def load_css():
    with open("assets/css/custom.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Background gradient moderne
def set_background():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    # Charger les styles
    load_css()
    set_background()
    
    # Vérifier l'authentification
    if not check_authentication():
        st.switch_page("pages/connexion.py")
    
    # Sidebar
    with st.sidebar:
        render_sidebar()
    
    # Page d'accueil principale
    st.markdown("""
        <div class="main-container">
            <div class="hero-section">
                <h1 class="hero-title">🚀 ML Boost Platform</h1>
                <p class="hero-subtitle">Plateforme de Machine Learning intuitive et puissante</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Section fonctionnalités
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h3>📊 Data Science</h3>
                <p>Importez et analysez vos données facilement</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h3>🤖 ML Automatique</h3>
                <p>Entraînez des modèles sans code</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <h3>📈 Visualisation</h3>
                <p>Analysez les résultats avec des graphiques interactifs</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Call-to-action
    st.markdown("""
        <div class="cta-section">
            <h2>Prêt à commencer ?</h2>
            <p>Créez votre premier projet de Machine Learning en quelques minutes</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🎯 Créer un Nouveau Projet", use_container_width=True):
            st.switch_page("pages/New_project.py")

if __name__ == "__main__":
    main()
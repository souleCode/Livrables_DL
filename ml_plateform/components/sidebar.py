import streamlit as st

def render_sidebar():
    st.markdown("""
        <style>
        .sidebar-logo {
            text-align: center;
            padding: 2rem 0;
            color: white;
        }
        .sidebar-logo h2 {
            margin: 0;
            font-size: 1.5rem;
        }
        </style>
        
        <div class="sidebar-logo">
            <h2>🧠 ML Boost</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Navigation principale
    st.page_link("app.py", label="🏠 Accueil", icon="🏠")
    st.page_link("pages/dashboard.py", label="📊 Tableau de bord", icon="📊")
    st.page_link("pages/New_project.py", label="🆕 Nouveau projet", icon="🆕")
    st.page_link("pages/Gestion_model.py", label="🗃️ Modèles", icon="🗃️")
    st.page_link("pages/Historique.py", label="📚 Historique", icon="📚")
    # st.page_link("config/settings.py", label="⚙️ Paramètres", icon="⚙️")
    st.divider()
    
    # Informations utilisateur
    if st.session_state.get('authenticated'):
        st.write(f"👤 {st.session_state.get('user_email', 'Utilisateur')}")
        if st.button("🚪 Déconnexion", use_container_width=True):
            from utils.auth import logout_user
            logout_user()
            st.rerun()
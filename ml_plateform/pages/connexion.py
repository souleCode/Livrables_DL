import streamlit as st
from utils.auth import login_user

st.set_page_config(page_title="Connexion - ML Boost", page_icon="🔐")

st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 5rem auto;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    </style>
    
    <div class="login-container">
        <h2 style="text-align: center; color: #667eea;">🔐 Connexion</h2>
    </div>
""", unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Se connecter")
        
        with st.form("login_form"):
            email = st.text_input("📧 Email")
            password = st.text_input("🔒 Mot de passe", type="password")
            
            if st.form_submit_button("🚀 Se connecter", use_container_width=True):
                if login_user(email, password):
                    st.success("Connexion réussie !")
                    st.switch_page("app.py")
                else:
                    st.error("Erreur de connexion")
        
        st.markdown("---")
        st.markdown("#### Ou connectez-vous avec")
        col1, col2 = st.columns(2)
        with col1:
            st.button("🔵 Google", use_container_width=True)
        with col2:
            st.button("⚫ GitHub", use_container_width=True)
        
        st.markdown("---")
        st.markdown("📝 [Mot de passe oublié?](#)")
        st.markdown("👤 [Créer un compte](#)")


## Session State Debugging Utility
def print_session_state():
    """Afficher dans la console"""
    print("\n" + "="*50)
    print("SESSION STATE:")
    print("="*50)
    for key, value in st.session_state.items():
        print(f"{key}: {type(value).__name__} = {value}")
    print("="*50 + "\n")

# Appeler quand nécessaire
# print_session_state()
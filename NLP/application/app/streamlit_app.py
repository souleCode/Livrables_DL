import streamlit as st
import requests
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Assistant RAG PDF",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design moderne
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1e293b 0%, #f59e42 100%);
    }
    .stApp {
        background: linear-gradient(to bottom right, #f59e42, #1e293b, #fbbf24);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background: linear-gradient(135deg, #1e293b 0%, #f59e42 100%);
        color: white;
        margin-left: 20%;
    }
       .assistant-message {
        background: #fff7ed;
        border: 1px solid #f59e42;
        box-shadow: 0 1px 3px rgba(245, 158, 66, 0.1);
        margin-right: 20%;
        color: #1e293b; /* <-- Ajouté : texte foncé */
    }
    .system-message {
        background: #fbbf24;
        border: 1px solid #f59e42;
        color: #1e293b;
    }
    .error-message {
        background: #fee2e2;
        border: 1px solid #fca5a5;
        color: #991b1b;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #1e293b 0%, #f59e42 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.75rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 25px rgba(245, 158, 66, 0.3);
    }
    .success-box {
        background: #d1fae5;
        border: 1px solid #6ee7b7;
        border-radius: 0.75rem;
        padding: 1rem;
        color: #065f46;
    }
    </style>
""", unsafe_allow_html=True)

# Initialisation des variables de session
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'pdf_loaded' not in st.session_state:
    st.session_state.pdf_loaded = False
if 'chunks_count' not in st.session_state:
    st.session_state.chunks_count = 0
if 'api_url' not in st.session_state:
    st.session_state.api_url = 'http://localhost:8001'

# Sidebar - Configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # URL de l'API
    api_url = st.text_input(
        "URL de l'API",
        value=st.session_state.api_url,
        placeholder="http://localhost:8001"
    )
    st.session_state.api_url = api_url
    
    st.divider()
    
    # Section Chargement PDF
    st.subheader("📄 Chargement du PDF")
    
    if st.session_state.pdf_loaded:
        st.success(f"✅ PDF chargé\n\n**{st.session_state.chunks_count}** segments créés")
        if st.button("🔄 Recharger le PDF"):
            st.session_state.pdf_loaded = False
            st.session_state.messages = []
            st.rerun()
    else:
        if st.button("📥 Charger le PDF"):
            with st.spinner("Chargement du PDF en cours..."):
                try:
                    response = requests.post(f"{st.session_state.api_url}/load_pdf/")
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.pdf_loaded = True
                        st.session_state.chunks_count = data['chunks']
                        st.session_state.messages.append({
                            'type': 'system',
                            'content': f"✓ PDF chargé avec succès : {data['chunks']} segments créés",
                            'timestamp': datetime.now().strftime("%H:%M")
                        })
                        st.success("PDF chargé avec succès !")
                        st.rerun()
                    else:
                        st.error(f"Erreur {response.status_code}")
                except Exception as e:
                    st.error(f"Erreur de connexion : {str(e)}")
    
    st.divider()
    
    # Informations
    st.subheader("ℹ️ Informations")
    st.info("""
    **Instructions :**
    1. Configurez l'URL de l'API
    2. Chargez le PDF
    3. Posez vos questions
    
    **Astuces :**
    - Soyez précis dans vos questions
    - Utilisez le contexte du document
    """)
    
    # Bouton pour effacer l'historique
    if st.button("🗑️ Effacer l'historique"):
        st.session_state.messages = []
        st.rerun()

# Interface principale
st.title("🤖 Assistant RAG PDF")
st.markdown("### Posez vos questions sur le document chargé")

# Affichage des messages
chat_container = st.container()
with chat_container:
    if len(st.session_state.messages) == 0:
        st.info("👋 Bienvenue ! Chargez un PDF dans la barre latérale pour commencer.")
    else:
        for message in st.session_state.messages:
            msg_type = message['type']
            content = message['content']
            timestamp = message.get('timestamp', '')
            
            if msg_type == 'user':
                st.markdown(f"""
                    <div class="chat-message user-message">
                        <div style="font-weight: 600; margin-bottom: 0.5rem;">👤 Vous <span style="opacity: 0.7; font-size: 0.85rem; font-weight: 400;">{timestamp}</span></div>
                        <div>{content}</div>
                    </div>
                """, unsafe_allow_html=True)
            elif msg_type == 'assistant':
                st.markdown(f"""
                    <div class="chat-message assistant-message">
                        <div style="font-weight: 600; margin-bottom: 0.5rem;">🤖 Assistant <span style="opacity: 0.7; font-size: 0.85rem; font-weight: 400;">{timestamp}</span></div>
                        <div>{content}</div>
                    </div>
                """, unsafe_allow_html=True)
            elif msg_type == 'system':
                st.markdown(f"""
                    <div class="chat-message system-message">
                        <div style="font-weight: 600; margin-bottom: 0.5rem;">ℹ️ Système</div>
                        <div>{content}</div>
                    </div>
                """, unsafe_allow_html=True)
            elif msg_type == 'error':
                st.markdown(f"""
                    <div class="chat-message error-message">
                        <div style="font-weight: 600; margin-bottom: 0.5rem;">❌ Erreur</div>
                        <div>{content}</div>
                    </div>
                """, unsafe_allow_html=True)

# Zone de saisie (en bas)
st.divider()

# Vérifier si le PDF est chargé
if not st.session_state.pdf_loaded:
    st.warning("⚠️ Veuillez d'abord charger le PDF dans la barre latérale.")
    query = st.text_input("Votre question", disabled=True, placeholder="Chargez d'abord le PDF...")
else:
    # Formulaire de question
    with st.form(key='question_form', clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        
        with col1:
            query = st.text_input(
                "Votre question",
                placeholder="Posez votre question sur le document...",
                label_visibility="collapsed"
            )
        
        with col2:
            submit_button = st.form_submit_button("📤 Envoyer")
        
        if submit_button and query.strip():
            # Ajouter le message utilisateur
            st.session_state.messages.append({
                'type': 'user',
                'content': query,
                'timestamp': datetime.now().strftime("%H:%M")
            })
            
            # Appel à l'API
            with st.spinner("🤔 Réflexion en cours..."):
                try:
                    response = requests.post(
                        f"{st.session_state.api_url}/ask/",
                        json={'query': query}  # <-- ici, on utilise json au lieu de params
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.messages.append({
                            'type': 'assistant',
                            'content': data['answer'],
                            'timestamp': datetime.now().strftime("%H:%M")
                        })
                    else:
                        st.session_state.messages.append({
                            'type': 'error',
                            'content': f"Erreur {response.status_code}: {response.text}",
                            'timestamp': datetime.now().strftime("%H:%M")
                        })
                except Exception as e:
                    st.session_state.messages.append({
                        'type': 'error',
                        'content': f"Erreur de connexion : {str(e)}",
                        'timestamp': datetime.now().strftime("%H:%M")
                    })
            
            st.rerun()

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.875rem; padding: 1rem;">
        💡 Propulsé par FastAPI + Streamlit | Assistant RAG PDF
    </div>
""", unsafe_allow_html=True)
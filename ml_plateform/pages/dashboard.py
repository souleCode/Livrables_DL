import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Configuration de la page
st.set_page_config(
    page_title="Tableau de Bord - FrameML",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    /* Styles généraux */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header du dashboard */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .dashboard-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    .dashboard-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Cartes de statistiques */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid;
        transition: transform 0.3s;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stat-trend {
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Carte de projet */
    .project-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        transition: all 0.3s;
    }
    
    .project-card:hover {
        box-shadow: 0 4px 16px rgba(102,126,234,0.2);
        border-color: #667eea;
    }
    
    .project-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .project-meta {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 0.8rem;
    }
    
    .project-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    
    /* Boutons d'action */
    .action-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(102,126,234,0.3);
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102,126,234,0.4);
    }
    
    /* Notifications */
    .notification-item {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        border-left: 3px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .notification-time {
        color: #999;
        font-size: 0.85rem;
    }
    
    /* Section title */
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 FrameML")
    st.markdown("---")
    
    # Menu de navigation
    st.markdown("#### 📍 Navigation")
    menu_items = {
        "🏠 Tableau de Bord": "dashboard",
        "➕ Nouveau Projet": "new_project",
        "📊 Mes Projets": "projects",
        "🤖 Mes Modèles": "models",
        "📈 Historique": "history",
        "⚙️ Paramètres": "settings",
    }
    
    selected = st.radio("", list(menu_items.keys()), label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("#### 👤 Utilisateur")
    st.markdown("**Jean Dupont**")
    st.markdown("jean.dupont@email.com")
    
    st.markdown("---")
    if st.button("🚪 Déconnexion", use_container_width=True):
        st.info("Déconnexion...")

# Header du dashboard
st.markdown("""
<div class="dashboard-header">
    <h1>📊 Tableau de Bord</h1>
    <p>Bienvenue ! Voici un aperçu de vos projets et activités récentes</p>
</div>
""", unsafe_allow_html=True)

# Statistiques rapides
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card" style="border-left-color: #667eea;">
        <div class="stat-label">📁 Total Projets</div>
        <div class="stat-number" style="color: #667eea;">12</div>
        <div class="stat-trend" style="color: #10b981;">↗ +3 ce mois</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card" style="border-left-color: #f59e0b;">
        <div class="stat-label">🤖 Modèles Entraînés</div>
        <div class="stat-number" style="color: #f59e0b;">34</div>
        <div class="stat-trend" style="color: #10b981;">↗ +8 ce mois</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card" style="border-left-color: #10b981;">
        <div class="stat-label">✅ Projets Actifs</div>
        <div class="stat-number" style="color: #10b981;">5</div>
        <div class="stat-trend" style="color: #10b981;">↗ En progression</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card" style="border-left-color: #ef4444;">
        <div class="stat-label">🎯 Précision Moyenne</div>
        <div class="stat-number" style="color: #ef4444;">92.4%</div>
        <div class="stat-trend" style="color: #10b981;">↗ +2.1%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Actions rapides
st.markdown('<div class="section-title">⚡ Actions Rapides</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("➕ Nouveau Projet", use_container_width=True, type="primary"):
        st.success("Redirection vers création de projet...")

with col2:
    if st.button("📤 Importer Données", use_container_width=True):
        st.info("Ouverture de l'importateur...")

with col3:
    if st.button("🔍 Explorer Modèles", use_container_width=True):
        st.info("Navigation vers les modèles...")

with col4:
    if st.button("📊 Voir Statistiques", use_container_width=True):
        st.info("Chargement des statistiques...")

st.markdown("<br>", unsafe_allow_html=True)

# Conteneur principal avec deux colonnes
col_main, col_side = st.columns([2, 1])

with col_main:
    # Projets récents
    st.markdown('<div class="section-title">📁 Projets Récents</div>', unsafe_allow_html=True)
    
    # Projet 1
    st.markdown("""
    <div class="project-card">
        <div class="project-title">🏡 Prédiction Prix Immobilier</div>
        <div class="project-meta">📅 Créé le 05 Oct 2024 • 🤖 Random Forest • 📊 Classification</div>
        <span class="project-badge" style="background: #d1fae5; color: #065f46;">✅ Entraîné</span>
        <span class="project-badge" style="background: #dbeafe; color: #1e40af;">📈 Accuracy: 94.2%</span>
    </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        st.button("👁️ Voir", key="view1", use_container_width=True)
    with col_btn2:
        st.button("📊 Résultats", key="results1", use_container_width=True)
    with col_btn3:
        st.button("⚙️ Configurer", key="config1", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Projet 2
    st.markdown("""
    <div class="project-card">
        <div class="project-title">🖼️ Classification d'Images</div>
        <div class="project-meta">📅 Créé le 03 Oct 2024 • 🤖 CNN • 📊 Deep Learning</div>
        <span class="project-badge" style="background: #fef3c7; color: #92400e;">⏳ En cours</span>
        <span class="project-badge" style="background: #dbeafe; color: #1e40af;">📈 Epoch: 45/100</span>
    </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        st.button("👁️ Voir", key="view2", use_container_width=True)
    with col_btn2:
        st.button("📊 Monitoring", key="monitor2", use_container_width=True)
    with col_btn3:
        st.button("⏸️ Pause", key="pause2", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Projet 3
    st.markdown("""
    <div class="project-card">
        <div class="project-title">📈 Analyse de Sentiment</div>
        <div class="project-meta">📅 Créé le 01 Oct 2024 • 🤖 BERT • 📊 NLP</div>
        <span class="project-badge" style="background: #d1fae5; color: #065f46;">✅ Entraîné</span>
        <span class="project-badge" style="background: #dbeafe; color: #1e40af;">📈 F1-Score: 0.89</span>
    </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        st.button("👁️ Voir", key="view3", use_container_width=True)
    with col_btn2:
        st.button("📊 Résultats", key="results3", use_container_width=True)
    with col_btn3:
        st.button("🚀 Déployer", key="deploy3", use_container_width=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Graphique d'activité
    st.markdown('<div class="section-title">📈 Activité des 30 Derniers Jours</div>', unsafe_allow_html=True)
    
    # Données de démonstration
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    activity_data = pd.DataFrame({
        'Date': dates,
        'Projets Créés': [random.randint(0, 3) for _ in range(30)],
        'Modèles Entraînés': [random.randint(1, 5) for _ in range(30)]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=activity_data['Date'], y=activity_data['Projets Créés'], 
                             name='Projets Créés', line=dict(color='#667eea', width=3)))
    fig.add_trace(go.Scatter(x=activity_data['Date'], y=activity_data['Modèles Entraînés'], 
                             name='Modèles Entraînés', line=dict(color='#764ba2', width=3)))
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_side:
    # Notifications
    st.markdown('<div class="section-title">🔔 Notifications</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="notification-item">
        <div style="font-weight: 600; color: #333;">✅ Entraînement terminé</div>
        <div style="font-size: 0.9rem; color: #666; margin-top: 0.3rem;">
            Votre modèle "Prix Immobilier" a terminé avec succès
        </div>
        <div class="notification-time">Il y a 2 heures</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="notification-item">
        <div style="font-weight: 600; color: #333;">📊 Nouveau dataset disponible</div>
        <div style="font-size: 0.9rem; color: #666; margin-top: 0.3rem;">
            Un nouveau jeu de données a été ajouté à votre projet
        </div>
        <div class="notification-time">Il y a 5 heures</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="notification-item">
        <div style="font-weight: 600; color: #333;">⚠️ Attention requise</div>
        <div style="font-size: 0.9rem; color: #666; margin-top: 0.3rem;">
            Le modèle CNN nécessite plus de données pour améliorer les performances
        </div>
        <div class="notification-time">Hier</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Performance des modèles
    st.markdown('<div class="section-title">🎯 Top Modèles</div>', unsafe_allow_html=True)
    
    model_perf = pd.DataFrame({
        'Modèle': ['Random Forest', 'XGBoost', 'CNN', 'BERT', 'SVM'],
        'Précision': [94.2, 92.8, 91.5, 89.3, 87.1]
    })
    
    fig2 = px.bar(model_perf, x='Précision', y='Modèle', orientation='h',
                  color='Précision', color_continuous_scale='Purples')
    fig2.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stockage
    st.markdown('<div class="section-title">💾 Stockage</div>', unsafe_allow_html=True)
    
    storage_used = 65
    st.progress(storage_used / 100)
    st.markdown(f"**{storage_used}%** utilisé (6.5 GB / 10 GB)")
    
    if st.button("📦 Gérer le stockage", use_container_width=True):
        st.info("Gestion du stockage...")



## Session debugging
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
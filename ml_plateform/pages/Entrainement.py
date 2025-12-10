import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import random
from utils.Client import api_client
from utils.Helpers import show_loading, show_success, show_error

# Configuration de la page
st.set_page_config(
    page_title="Entraînement - FrameML",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Vérifier qu'un entraînement est configuré
if 'training_config' not in st.session_state or 'experiment_id' not in st.session_state:
    st.error("❌ Aucun entraînement configuré. Veuillez d'abord configurer un modèle.")
    st.switch_page("pages/config_model.py")

# Initialisation de la session state
if 'is_training' not in st.session_state:
    st.session_state.is_training = False
if 'current_epoch' not in st.session_state:
    st.session_state.current_epoch = 0
if 'total_epochs' not in st.session_state:
    st.session_state.total_epochs = st.session_state.training_config.get('epochs', 50)
if 'training_history' not in st.session_state:
    st.session_state.training_history = {'epoch': [], 'train_loss': [], 'val_loss': [], 'train_acc': [], 'val_acc': []}
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'experiment_data' not in st.session_state:
    st.session_state.experiment_data = None
if 'training_results' not in st.session_state:
    st.session_state.training_results = None

# CSS personnalisé
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header */
    .page-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .page-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    /* Status card */
    .status-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-left: 5px solid;
    }
    
    .status-card.training {
        border-left-color: #f59e0b;
        background: linear-gradient(135deg, rgba(245,158,11,0.05) 0%, rgba(251,191,36,0.05) 100%);
    }
    
    .status-card.completed {
        border-left-color: #10b981;
        background: linear-gradient(135deg, rgba(16,185,129,0.05) 0%, rgba(52,211,153,0.05) 100%);
    }
    
    .status-card.error {
        border-left-color: #ef4444;
        background: linear-gradient(135deg, rgba(239,68,68,0.05) 0%, rgba(248,113,113,0.05) 100%);
    }
    
    .status-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .status-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .status-subtitle {
        color: #666;
        font-size: 1rem;
    }
    
    /* Metric card */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
        border-top: 4px solid;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-change {
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Chart card */
    .chart-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    .chart-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    
    /* Log container */
    .log-container {
        background: #1e293b;
        padding: 1.5rem;
        border-radius: 12px;
        height: 400px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
    }
    
    .log-entry {
        margin-bottom: 0.5rem;
        line-height: 1.6;
    }
    
    .log-time {
        color: #94a3b8;
    }
    
    .log-info {
        color: #60a5fa;
    }
    
    .log-success {
        color: #34d399;
    }
    
    .log-warning {
        color: #fbbf24;
    }
    
    .log-error {
        color: #f87171;
    }
    
    /* Progress container */
    .progress-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    .time-remaining {
        background: #f0f9ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
        margin-top: 1rem;
    }
    
    /* Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .pulsing {
        animation: pulse 2s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour ajouter un log
def add_log(message, log_type="info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({
        'time': timestamp,
        'message': message,
        'type': log_type
    })
    # Garder seulement les 100 derniers logs
    if len(st.session_state.logs) > 100:
        st.session_state.logs = st.session_state.logs[-100:]

# Fonction pour récupérer les résultats de l'entraînement
def get_training_results():
    """Récupérer les résultats de l'entraînement depuis l'API"""
    try:
        experiment = api_client.get_training_status(st.session_state.experiment_id)
        st.session_state.experiment_data = experiment
        return experiment
    except Exception as e:
        show_error(f"❌ Erreur lors de la récupération des résultats: {str(e)}")
        return None

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 FrameML")
    st.markdown("---")
    
    # Informations du projet depuis l'API
    try:
        project = api_client.get_project(st.session_state.project_id)
        st.markdown("#### 📊 Projet Actuel")
        st.markdown(f"**{project['name']}**")
        st.markdown(f"{project['task_type']} • {project['problem_type']}")


        # print(f"====project from API de ENTRAINNEMENT: {project}==========")



    except:
        st.error("❌ Impossible de charger les infos du projet")
    
    st.markdown("---")
    
    st.markdown("#### 🎯 Configuration")
    training_config = st.session_state.training_config
    st.info(f"**Modèle:** {training_config.get('model_type', 'N/A')}")
    st.info(f"**Epochs:** {training_config.get('epochs', 50)}")
    st.info(f"**Train/Test:** {int(training_config.get('train_test_split', 0.8)*100)}/{int((1-training_config.get('train_test_split', 0.8))*100)}")
    
    st.markdown("---")
    
    # Contrôles d'entraînement
    st.markdown("#### ⚙️ Contrôles")
    
    if not st.session_state.is_training:
        if st.button("▶️ Démarrer l'Entraînement", use_container_width=True, type="primary"):
            st.session_state.is_training = True
            st.session_state.current_epoch = 0
            st.session_state.training_history = {'epoch': [], 'train_loss': [], 'val_loss': [], 'train_acc': [], 'val_acc': []}
            st.session_state.logs = []
            add_log("🚀 Démarrage de l'entraînement...", "info")
            add_log("📊 Chargement des données...", "info")
            add_log("⚙️ Initialisation du modèle...", "info")
            st.rerun()
    else:
        if st.button("⏸️ Pause", use_container_width=True):
            st.session_state.is_training = False
            add_log("⏸️ Entraînement mis en pause", "warning")
            st.rerun()
        
        if st.button("⏹️ Arrêter", use_container_width=True):
            st.session_state.is_training = False
            st.session_state.current_epoch = 0
            add_log("⏹️ Entraînement arrêté", "error")
            st.rerun()
    
    if st.button("🔄 Réinitialiser", use_container_width=True):
        st.session_state.current_epoch = 0
        st.session_state.training_history = {'epoch': [], 'train_loss': [], 'val_loss': [], 'train_acc': [], 'val_acc': []}
        st.session_state.logs = []
        st.rerun()
    
    if st.button("📊 Voir Résultats API", use_container_width=True):
        with show_loading("Récupération des résultats..."):
            results = get_training_results()
            if results:
                show_success("✅ Résultats récupérés!")
                st.session_state.training_results = results

# Header
st.markdown("""
<div class="page-header">
    <h1>🚀 Entraînement et Monitoring</h1>
    <p>Suivez la progression de l'entraînement en temps réel</p>
</div>
""", unsafe_allow_html=True)

# Status Card
if st.session_state.is_training:
    status_class = "training"
    status_icon = "⏳"
    status_title = "Entraînement en cours..."
    status_subtitle = f"Epoch {st.session_state.current_epoch}/{st.session_state.total_epochs}"
elif st.session_state.current_epoch >= st.session_state.total_epochs and st.session_state.current_epoch > 0:
    status_class = "completed"
    status_icon = "✅"
    status_title = "Entraînement terminé!"
    status_subtitle = "Modèle prêt pour l'évaluation"
elif st.session_state.training_results:
    status_class = "completed"
    status_icon = "✅"
    status_title = "Entraînement terminé (API)"
    status_subtitle = "Résultats disponibles"
else:
    status_class = "training"
    status_icon = "⏸️"
    status_title = "En attente"
    status_subtitle = "Cliquez sur Démarrer pour lancer l'entraînement"

st.markdown(f"""
<div class="status-card {status_class}">
    <div class="status-icon {'pulsing' if st.session_state.is_training else ''}">{status_icon}</div>
    <div class="status-title">{status_title}</div>
    <div class="status-subtitle">{status_subtitle}</div>
</div>
""", unsafe_allow_html=True)

# Simulation de l'entraînement (pour la démo)
if st.session_state.is_training and st.session_state.current_epoch < st.session_state.total_epochs:
    # Simulation des métriques d'entraînement
    base_train_loss = 2.5 * np.exp(-0.05 * st.session_state.current_epoch) + random.uniform(-0.05, 0.05)
    base_val_loss = 2.7 * np.exp(-0.045 * st.session_state.current_epoch) + random.uniform(-0.05, 0.05)
    base_train_acc = 100 * (1 - np.exp(-0.08 * st.session_state.current_epoch)) + random.uniform(-1, 1)
    base_val_acc = 100 * (1 - np.exp(-0.075 * st.session_state.current_epoch)) + random.uniform(-1, 1)
    
    data = {
        'train_loss': max(0.1, base_train_loss),
        'val_loss': max(0.1, base_val_loss),
        'train_acc': min(99, max(0, base_train_acc)),
        'val_acc': min(99, max(0, base_val_acc))
    }
    
    st.session_state.training_history['epoch'].append(st.session_state.current_epoch + 1)
    st.session_state.training_history['train_loss'].append(data['train_loss'])
    st.session_state.training_history['val_loss'].append(data['val_loss'])
    st.session_state.training_history['train_acc'].append(data['train_acc'])
    st.session_state.training_history['val_acc'].append(data['val_acc'])
    
    # Ajouter des logs
    if st.session_state.current_epoch % 5 == 0:
        add_log(f"Epoch {st.session_state.current_epoch + 1}/{st.session_state.total_epochs} - Loss: {data['train_loss']:.4f} - Acc: {data['train_acc']:.2f}%", "success")
    
    st.session_state.current_epoch += 1
    
    if st.session_state.current_epoch >= st.session_state.total_epochs:
        st.session_state.is_training = False
        add_log("✅ Entraînement terminé avec succès!", "success")
        add_log("💾 Sauvegarde du modèle...", "info")
        st.balloons()
    
    time.sleep(0.3)  # Simulation du temps d'entraînement
    st.rerun()

# Affichage des résultats de l'API si disponibles
if st.session_state.training_results:
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Résultats de l'Entraînement (API)")
    
    metrics = st.session_state.training_results.get('metrics', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Accuracy Test", f"{metrics.get('test_accuracy', 0)*100:.2f}%")
    with col2:
        st.metric("Precision", f"{metrics.get('precision', 0)*100:.2f}%")
    with col3:
        st.metric("Recall", f"{metrics.get('recall', 0)*100:.2f}%")
    with col4:
        st.metric("F1-Score", f"{metrics.get('f1_score', 0)*100:.2f}%")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Progress bar et métriques (pour la simulation)
if st.session_state.current_epoch > 0 and not st.session_state.training_results:
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    
    # Barre de progression
    progress = st.session_state.current_epoch / st.session_state.total_epochs
    st.progress(progress)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**Progression:** Epoch {st.session_state.current_epoch}/{st.session_state.total_epochs} ({progress*100:.1f}%)")
    with col2:
        remaining_epochs = st.session_state.total_epochs - st.session_state.current_epoch
        estimated_time = remaining_epochs * 2  # Estimation: 2 secondes par epoch
        st.markdown(f"**Temps restant:** ~{estimated_time}s")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Métriques actuelles
    st.markdown("<br>", unsafe_allow_html=True)
    
    if len(st.session_state.training_history['epoch']) > 0:
        latest_idx = -1
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="border-top-color: #ef4444;">
                <div class="metric-label">Train Loss</div>
                <div class="metric-value" style="color: #ef4444;">
                    {st.session_state.training_history['train_loss'][latest_idx]:.4f}
                </div>
                <div class="metric-change" style="color: #10b981;">
                    ↓ Diminution
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="border-top-color: #f59e0b;">
                <div class="metric-label">Val Loss</div>
                <div class="metric-value" style="color: #f59e0b;">
                    {st.session_state.training_history['val_loss'][latest_idx]:.4f}
                </div>
                <div class="metric-change" style="color: #10b981;">
                    ↓ Diminution
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card" style="border-top-color: #3b82f6;">
                <div class="metric-label">Train Accuracy</div>
                <div class="metric-value" style="color: #3b82f6;">
                    {st.session_state.training_history['train_acc'][latest_idx]:.2f}%
                </div>
                <div class="metric-change" style="color: #10b981;">
                    ↗ Amélioration
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card" style="border-top-color: #10b981;">
                <div class="metric-label">Val Accuracy</div>
                <div class="metric-value" style="color: #10b981;">
                    {st.session_state.training_history['val_acc'][latest_idx]:.2f}%
                </div>
                <div class="metric-change" style="color: #10b981;">
                    ↗ Amélioration
                </div>
            </div>
            """, unsafe_allow_html=True)

# Graphiques d'apprentissage (pour la simulation)
if len(st.session_state.training_history['epoch']) > 0 and not st.session_state.training_results:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📉 Courbes de Loss</div>', unsafe_allow_html=True)
        
        fig_loss = go.Figure()
        fig_loss.add_trace(go.Scatter(
            x=st.session_state.training_history['epoch'],
            y=st.session_state.training_history['train_loss'],
            name='Train Loss',
            line=dict(color='#ef4444', width=3),
            mode='lines+markers'
        ))
        fig_loss.add_trace(go.Scatter(
            x=st.session_state.training_history['epoch'],
            y=st.session_state.training_history['val_loss'],
            name='Val Loss',
            line=dict(color='#f59e0b', width=3),
            mode='lines+markers'
        ))
        
        fig_loss.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=20, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Epoch', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            yaxis=dict(title='Loss', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_loss, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_chart2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📈 Courbes d\'Accuracy</div>', unsafe_allow_html=True)
        
        fig_acc = go.Figure()
        fig_acc.add_trace(go.Scatter(
            x=st.session_state.training_history['epoch'],
            y=st.session_state.training_history['train_acc'],
            name='Train Accuracy',
            line=dict(color='#3b82f6', width=3),
            mode='lines+markers'
        ))
        fig_acc.add_trace(go.Scatter(
            x=st.session_state.training_history['epoch'],
            y=st.session_state.training_history['val_acc'],
            name='Val Accuracy',
            line=dict(color='#10b981', width=3),
            mode='lines+markers'
        ))
        
        fig_acc.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=20, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Epoch', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            yaxis=dict(title='Accuracy (%)', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_acc, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Logs d'entraînement
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">📋 Logs d\'Entraînement</div>', unsafe_allow_html=True)

log_html = '<div class="log-container">'
for log in reversed(st.session_state.logs[-50:]):  # Afficher les 50 derniers logs
    log_class = f"log-{log['type']}"
    log_html += f'<div class="log-entry"><span class="log-time">[{log["time"]}]</span> <span class="{log_class}">{log["message"]}</span></div>'

if not st.session_state.logs:
    log_html += '<div class="log-entry"><span class="log-info">Aucun log disponible. Démarrez l\'entraînement pour voir les logs.</span></div>'

log_html += '</div>'
st.markdown(log_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Boutons d'action
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("⬅️ Retour Configuration", use_container_width=True):
        st.switch_page("pages/config_model.py")

with col2:
    if st.session_state.training_results or (st.session_state.current_epoch >= st.session_state.total_epochs and not st.session_state.is_training):
        if st.button("📊 Voir Résultats Détaillés", use_container_width=True, type="primary"):
            # Sauvegarder les résultats pour la page suivante
            if st.session_state.training_results:
                st.session_state.final_results = st.session_state.training_results
            else:
                # Créer des résultats simulés pour la démo
                st.session_state.final_results = {
                    'metrics': {
                        'test_accuracy': random.uniform(0.85, 0.95),
                        'precision': random.uniform(0.82, 0.92),
                        'recall': random.uniform(0.83, 0.93),
                        'f1_score': random.uniform(0.84, 0.94),
                        'training_time': st.session_state.total_epochs * 0.3
                    },
                    'model_id': st.session_state.get('model_id', 'demo_model'),
                    'experiment_id': st.session_state.get('experiment_id', 'demo_experiment')
                }
            st.switch_page("pages/Results.py")

with col3:
    if st.button("📋 Liste des Modèles", use_container_width=True):
        st.switch_page("pages/Gestion_model.py")


# Session
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
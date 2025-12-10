import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
from utils.Client import api_client
from utils.Helpers import show_loading, show_success, show_error

# Configuration de la page
st.set_page_config(
    page_title="Gestion des Modèles - FrameML",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation de la session state
if 'selected_model_id' not in st.session_state:
    st.session_state.selected_model_id = None
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "list"  # list or detail
if 'models_list' not in st.session_state:
    st.session_state.models_list = []
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = None

# CSS personnalisé (identique)
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
    
    /* Stats cards */
    .stats-mini {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
        border-top: 4px solid;
    }
    
    .stats-mini-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .stats-mini-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Model card */
    .model-card {
        background: white;
        padding: 1.8rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1.2rem;
        border-left: 5px solid;
        transition: all 0.3s;
        position: relative;
    }
    
    .model-card:hover {
        box-shadow: 0 6px 16px rgba(102,126,234,0.2);
        transform: translateX(5px);
    }
    
    .model-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 1rem;
    }
    
    .model-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.3rem;
    }
    
    .model-subtitle {
        color: #666;
        font-size: 0.95rem;
    }
    
    .model-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-top: 0.3rem;
    }
    
    .model-metrics {
        display: flex;
        gap: 2rem;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
    }
    
    .model-metric-item {
        text-align: center;
    }
    
    .model-metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .model-metric-label {
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.2rem;
    }
    
    /* Status badge */
    .status-badge {
        position: absolute;
        top: 15px;
        right: 15px;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    
    .status-active {
        background: #d1fae5;
        color: #065f46;
    }
    
    .status-deployed {
        background: #dbeafe;
        color: #1e40af;
    }
    
    .status-archived {
        background: #f3f4f6;
        color: #6b7280;
    }
    
    /* Detail view */
    .detail-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Info grid */
    .info-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .info-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 3px solid #667eea;
    }
    
    .info-label {
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }
    
    .info-value {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
    }
    
    /* Code block */
    .code-block {
        background: #1e293b;
        color: #e2e8f0;
        padding: 1.5rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        overflow-x: auto;
        margin: 1rem 0;
    }
    
    .code-comment {
        color: #94a3b8;
    }
    
    .code-keyword {
        color: #c792ea;
    }
    
    .code-string {
        color: #c3e88d;
    }
    
    .code-function {
        color: #82aaff;
    }
    
    /* Download card */
    .download-card {
        background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #667eea;
        margin-bottom: 1rem;
        transition: all 0.3s;
    }
    
    .download-card:hover {
        box-shadow: 0 4px 12px rgba(102,126,234,0.3);
        transform: translateY(-3px);
    }
    
    .download-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .download-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.3rem;
    }
    
    .download-description {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    /* Filter section */
    .filter-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour obtenir la métrique principale selon le type de problème
def get_primary_metric(model_data, problem_type):
    """Obtenir la métrique principale selon le type de tâche"""
    metrics = model_data.get('metrics', {})
    
    if problem_type == 'Régression':
        # Pour la régression, priorité au R²
        return metrics.get('test_r2', metrics.get('train_r2', 0.0))
    else:
        # Pour la classification, priorité à l'accuracy
        return metrics.get('test_accuracy', metrics.get('accuracy', 0.0))

def format_primary_metric(value, problem_type):
    """Formater la métrique principale"""
    if problem_type == 'Regression':
        # R² peut être négatif, on affiche avec 3 décimales
        return f"{value:.3f}"
    else:
        # Accuracy en pourcentage
        return f"{value * 100:.1f}%"

# Fonction pour charger les modèles depuis l'API
def load_models_from_api():
    """Charger la liste des modèles depuis l'API"""
    try:
        models = api_client.list_models()
        st.session_state.models_list = models
        st.session_state.last_refresh = datetime.now()
        return models
    except Exception as e:
        show_error(f"❌ Erreur lors du chargement des modèles: {str(e)}")
        return []

# Fonction pour formater les données des modèles
def format_model_data(api_models):
    """Formatter les données des modèles pour l'affichage"""
    formatted_models = []
    
    for model in api_models:
        # Extraire les métriques
        metrics = model.get('metrics', {})
        
        # Print model
        # print(f"==========MODEL========{model}=============================")
        # Récupérer le problem_type depuis le projet ou les métadonnées
        problem_type = model.get('task_type', 'Classification') #Ou Régression
        
        # Obtenir la métrique principale
        primary_metric = get_primary_metric(model, problem_type)
        
        # Déterminer le statut basé sur l'âge du modèle
        created_at = datetime.fromisoformat(model['created_at'].replace('Z', '+00:00'))
        days_ago = (datetime.now(created_at.tzinfo) - created_at).days
        
        if days_ago <= 7:
            status = 'deployed'
        elif days_ago <= 30:
            status = 'active'
        else:
            status = 'archived'
        
        formatted_models.append({
            'id': model['id'],
            'name': model['name'],
            'type': model['model_type'],
            'task': problem_type,  # ✅ Utiliser le vrai problem_type
            'primary_metric': primary_metric,
            'primary_metric_name': 'R²' if problem_type == 'Régression' else 'Accuracy',
            'date': created_at,
            'size': model.get('size_mb', 10.0),
            'status': status,
            'training_time': metrics.get('training_time', 15),
            'samples': metrics.get('n_samples', 5000),
            'features': metrics.get('n_features', 10),
            'version': '1.0.0',
            'model_data': model,  # Données complètes de l'API
            'problem_type': problem_type  # ✅ Stocker le problem_type
        })
    
    return formatted_models

# Informations du projet depuis l'API
try:
    project = api_client.get_project(st.session_state.project_id)
    st.markdown("#### 📊 Projet Actuel")
    st.markdown(f"**{project['name']}**")
    st.markdown(f"{project['task_type']} • {project['problem_type']}")  
except:
    st.error("❌ Impossible de charger les infos du projet")



# Charger les modèles au démarrage
if not st.session_state.models_list:
    with show_loading("Chargement des modèles..."):
        api_models = load_models_from_api()
        if api_models:
            st.session_state.models_list = format_model_data(api_models)
            show_success(f"✅ {len(api_models)} modèle(s) chargé(s)")

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 FrameML")
    st.markdown("---")
    
    # Statistiques depuis l'API
    total_models = len(st.session_state.models_list)
    deployed_count = sum(1 for m in st.session_state.models_list if m['status'] == 'deployed')
    active_count = sum(1 for m in st.session_state.models_list if m['status'] == 'active')
    
    st.markdown("#### 📊 Vue d'Ensemble")
    st.info(f"**Total Modèles:** {total_models}")
    st.info(f"**Modèles Actifs:** {active_count}")
    st.info(f"**Déployés:** {deployed_count}")
    
    if st.session_state.last_refresh:
        st.caption(f"Dernière mise à jour: {st.session_state.last_refresh.strftime('%H:%M:%S')}")
    
    st.markdown("---")
    
    st.markdown("#### 📍 Navigation")
    if st.button("⬅️ Retour au Dashboard", use_container_width=True):
        st.switch_page("app.py")
    if st.button("➕ Nouveau Modèle", use_container_width=True, type="primary"):
        st.switch_page("pages/config_model.py")
    
    st.markdown("---")
    
    st.markdown("#### 🔄 Actions")
    if st.button("🔄 Actualiser", use_container_width=True):
        with show_loading("Actualisation des modèles..."):
            api_models = load_models_from_api()
            if api_models:
                st.session_state.models_list = format_model_data(api_models)
                st.rerun()
    
    st.markdown("---")
    st.markdown("#### 💾 Stockage")
    total_size = sum(m['size'] for m in st.session_state.models_list)
    storage_limit = 500
    storage_percent = (total_size / storage_limit) * 100 if storage_limit > 0 else 0
    
    st.progress(min(storage_percent / 100, 1.0))
    st.markdown(f"**{total_size:.1f} MB** / {storage_limit} MB")
    st.caption(f"{storage_percent:.1f}% utilisé")

# Header
st.markdown("""
<div class="page-header">
    <h1>🤖 Gestion des Modèles</h1>
    <p>Gérez, déployez et téléchargez vos modèles entraînés</p>
</div>
""", unsafe_allow_html=True)

# Statistiques rapides
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stats-mini" style="border-top-color: #667eea;">
        <div class="stats-mini-label">Total Modèles</div>
        <div class="stats-mini-value" style="color: #667eea;">{len(st.session_state.models_list)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    deployed_count = sum(1 for m in st.session_state.models_list if m['status'] == 'deployed')
    st.markdown(f"""
    <div class="stats-mini" style="border-top-color: #10b981;">
        <div class="stats-mini-label">Déployés</div>
        <div class="stats-mini-value" style="color: #10b981;">{deployed_count}</div>
    </div>
    """, unsafe_allow_html=True)

    

with col3:
    # Calculer la moyenne selon le type de modèle
    if st.session_state.models_list:
        print(f"===========MODEL LIST: {st.session_state.models_list}======================")
        classification_models = [m for m in st.session_state.models_list if m['problem_type'] == 'Classification']
        regression_models = [m for m in st.session_state.models_list if m['problem_type'] == 'Régression']

        if len(classification_models) >= len(regression_models) and classification_models:
            avg_metric = sum(m['primary_metric'] for m in classification_models) / len(classification_models)
            metric_label = "Accuracy Moyenne"
            metric_value = f"{avg_metric * 100:.1f}%"
        elif regression_models:
            avg_metric = sum(m['primary_metric'] for m in regression_models) / len(regression_models)
            metric_label = "R² Moyen"
            metric_value = f"{avg_metric:.3f}"
        else:
            metric_label = "Performance"
            metric_value = "N/A"
    else:
        metric_label = "Performance"
        metric_value = "N/A"
    
    st.markdown(f"""
    <div class="stats-mini" style="border-top-color: #f59e0b;">
        <div class="stats-mini-label">{metric_label}</div>
        <div class="stats-mini-value" style="color: #f59e0b;">{metric_value}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_size = sum(m['size'] for m in st.session_state.models_list)
    st.markdown(f"""
    <div class="stats-mini" style="border-top-color: #ef4444;">
        <div class="stats-mini-label">Stockage Total</div>
        <div class="stats-mini-value" style="color: #ef4444;">{total_size:.1f} MB</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Filtres et recherche
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
col_search, col_filter1, col_filter2, col_filter3 = st.columns([2, 1, 1, 1])

with col_search:
    search_query = st.text_input("🔍 Rechercher un modèle", placeholder="Nom, type, tâche...")

with col_filter1:
    status_filter = st.selectbox("Statut", ["Tous", "Déployé", "Actif", "Archivé"])

with col_filter2:
    task_filter = st.selectbox("Tâche", ["Tous", "Classification", "Regression"])

with col_filter3:
    sort_by = st.selectbox("Trier par", ["Date (récent)", "Date (ancien)", "Performance", "Nom"])

st.markdown('</div>', unsafe_allow_html=True)

# Mode d'affichage
view_col1, view_col2 = st.columns([6, 1])
with view_col2:
    view_mode = st.radio("Vue", ["📋 Liste", "📊 Grille"], horizontal=True, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# Affichage des modèles
if not st.session_state.models_list:
    st.info("ℹ️ Aucun modèle trouvé. Créez votre premier modèle pour commencer!")
    if st.button("➕ Créer un Premier Modèle", type="primary"):
        st.switch_page("pages/config_model.py")

elif "Liste" in view_mode:
    # Vue Liste
    for model in st.session_state.models_list:
        # Appliquer les filtres
        if status_filter != "Tous":
            status_map = {"Déployé": "deployed", "Actif": "active", "Archivé": "archived"}
            if model['status'] != status_map[status_filter]:
                continue
        
        if task_filter != "Tous" and model['problem_type'] != task_filter:
            continue
        
        # Border color selon le statut
        border_color = "#10b981" if model['status'] == "deployed" else "#3b82f6" if model['status'] == "active" else "#9ca3af"
        
        # Status badge
        status_class = f"status-{model['status']}"
        status_text = "🚀 Déployé" if model['status'] == "deployed" else "✅ Actif" if model['status'] == "active" else "📦 Archivé"
        
        # Formater la métrique principale
        metric_display = format_primary_metric(model['primary_metric'], model['problem_type'])
        
        st.markdown(f"""
        <div class="model-card" style="border-left-color: {border_color};">
            <span class="status-badge {status_class}">{status_text}</span>
            <div class="model-header">
                <div>
                    <div class="model-title">{model['name']}</div>
                    <div class="model-subtitle">
                        {model['type']} • {model['problem_type']} • Version {model['version']}
                    </div>
                </div>
            </div>
            
            <div>
                <span class="model-badge" style="background: #dbeafe; color: #1e40af;">
                    📊 {model['primary_metric_name']}: {metric_display}
                </span>
                <span class="model-badge" style="background: #fef3c7; color: #92400e;">
                    💾 {model['size']:.1f} MB
                </span>
                <span class="model-badge" style="background: #e0e7ff; color: #3730a3;">
                    📅 {model['date'].strftime('%d/%m/%Y')}
                </span>
            </div>
            
            <div class="model-metrics">
                <div class="model-metric-item">
                    <div class="model-metric-value">{model['samples']:,}</div>
                    <div class="model-metric-label">Échantillons</div>
                </div>
                <div class="model-metric-item">
                    <div class="model-metric-value">{model['features']}</div>
                    <div class="model-metric-label">Features</div>
                </div>
                <div class="model-metric-item">
                    <div class="model-metric-value">{model['training_time']:.1f}s</div>
                    <div class="model-metric-label">Temps Training</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Boutons d'action
        col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)
        
        with col_btn1:
            if st.button("👁️ Détails", key=f"view_{model['id']}", use_container_width=True):
                st.session_state.selected_model_id = model['id']
                st.session_state.view_mode = "detail"
                st.rerun()
        
        with col_btn2:
            if st.button("📥 Télécharger", key=f"download_{model['id']}", use_container_width=True):
                with show_loading("Préparation du téléchargement..."):
                    try:
                        model_bytes = api_client.download_model(model['id'])
                        st.download_button(
                            label="📥 Télécharger .pkl",
                            data=model_bytes,
                            file_name=f"{model['name'].replace(' ', '_')}.pkl",
                            mime="application/octet-stream",
                            key=f"dl_{model['id']}"
                        )
                        show_success("✅ Modèle prêt au téléchargement!")
                    except Exception as e:
                        show_error(f"❌ Erreur lors du téléchargement: {str(e)}")
        
        with col_btn3:
            if model['status'] != 'deployed':
                if st.button("🚀 Déployer", key=f"deploy_{model['id']}", use_container_width=True):
                    st.success(f"🚀 Déploiement de {model['name']} lancé!")
            else:
                if st.button("⏹️ Arrêter", key=f"stop_{model['id']}", use_container_width=True):
                    st.warning(f"⏹️ Arrêt du déploiement...")
        
        with col_btn4:
            if st.button("📋 Dupliquer", key=f"duplicate_{model['id']}", use_container_width=True):
                st.info(f"📋 Duplication de {model['name']}...")
        
        with col_btn5:
            if st.button("🗑️ Supprimer", key=f"delete_{model['id']}", use_container_width=True):
                with show_loading("Suppression du modèle..."):
                    try:
                        result = api_client.delete_model(model['id'])
                        show_success("✅ Modèle supprimé avec succès!")
                        # Recharger la liste
                        api_models = load_models_from_api()
                        if api_models:
                            st.session_state.models_list = format_model_data(api_models)
                        st.rerun()
                    except Exception as e:
                        show_error(f"❌ Erreur lors de la suppression: {str(e)}")
        
        st.markdown("<br>", unsafe_allow_html=True)

else:
    # Vue Grille
    cols_per_row = 3
    for i in range(0, len(st.session_state.models_list), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(st.session_state.models_list):
                model = st.session_state.models_list[i + j]
                
                # Appliquer les filtres
                if task_filter != "Tous" and model['problem_type'] != task_filter:
                    continue
                
                metric_display = format_primary_metric(model['primary_metric'], model['problem_type'])
                
                with col:
                    st.markdown(f"""
                    <div class="model-card" style="border-left-color: #667eea; height: 280px;">
                        <div class="model-title" style="font-size: 1.1rem;">{model['name'][:25]}...</div>
                        <div class="model-subtitle">{model['type']} • {model['problem_type']}</div>
                        <div style="margin: 1rem 0; text-align: center;">
                            <div style="font-size: 2.5rem; font-weight: bold; color: #667eea;">{metric_display}</div>
                            <div style="color: #666; font-size: 0.9rem;">{model['primary_metric_name']}</div>
                        </div>
                        <div style="font-size: 0.85rem; color: #666; margin-top: 1rem;">
                            💾 {model['size']:.1f} MB<br>
                            📅 {model['date'].strftime('%d/%m/%Y')}<br>
                            ⏱️ {model['training_time']:.1f}s
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Voir Détails", key=f"grid_view_{model['id']}", use_container_width=True, type="primary"):
                        st.session_state.selected_model_id = model['id']
                        st.session_state.view_mode = "detail"
                        st.rerun()

# Vue détaillée d'un modèle
if st.session_state.view_mode == "detail" and st.session_state.selected_model_id:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Trouver le modèle sélectionné
    selected_model = next((m for m in st.session_state.models_list if m['id'] == st.session_state.selected_model_id), None)

    
    if selected_model:
        # Bouton retour
        if st.button("⬅️ Retour à la liste", type="secondary"):
            st.session_state.view_mode = "list"
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Titre du modèle
        problem_type = selected_model['problem_type']
        st.markdown(f"""
        <div class="detail-section">
            <h2 style="color: #667eea; margin-bottom: 0.5rem;">{selected_model['name']}</h2>
            <p style="color: #666; font-size: 1.1rem;">{selected_model['type']} • {problem_type} • Version {selected_model['version']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Informations du modèle
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.markdown('<div class="detail-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📊 Informations Générales</div>', unsafe_allow_html=True)
            
            # Récupérer les données complètes depuis l'API
            try:
                model_details = api_client.get_model(selected_model['id'])
                metrics = model_details.get('metrics', {})
            except:
                model_details = selected_model['model_data']
                metrics = model_details.get('metrics', {})
            
            metric_display = format_primary_metric(selected_model['primary_metric'], problem_type)
            
            st.markdown(f"""
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Type de Modèle</div>
                    <div class="info-value">{selected_model['type']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Type de Tâche</div>
                    <div class="info-value">{problem_type}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">{selected_model['primary_metric_name']}</div>
                    <div class="info-value">{metric_display}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Taille du Modèle</div>
                    <div class="info-value">{selected_model['size']:.1f} MB</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Date de Création</div>
                    <div class="info-value">{selected_model['date'].strftime('%d/%m/%Y %H:%M')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Temps d'Entraînement</div>
                    <div class="info-value">{selected_model['training_time']:.1f} secondes</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Échantillons</div>
                    <div class="info-value">{selected_model['samples']:,}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Features</div>
                    <div class="info-value">{selected_model['features']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_info2:
            st.markdown('<div class="detail-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🎯 Performances</div>', unsafe_allow_html=True)
            
            # ✅ Graphique de performance adapté selon le type de tâche
            if problem_type == 'Classification':
                metrics_data = {
                    'Accuracy': metrics.get('test_accuracy', metrics.get('accuracy', 0)) * 100,
                    'Precision': metrics.get('precision', 0) * 100,
                    'Recall': metrics.get('recall', 0) * 100,
                    'F1-Score': metrics.get('f1_score', 0) * 100
                }
                y_range = [0, 100]
                text_template = '%{text:.1f}%'
            else:  # Regression
                metrics_data = {
                    'R²': metrics.get('test_r2', metrics.get('r2_score', 0)),
                    'RMSE': -metrics.get('rmse', 0),  # Négatif pour visualisation
                    'MAE': -metrics.get('mae', 0),    # Négatif pour visualisation
                    'MAPE': -metrics.get('mape', 0) if metrics.get('mape', 0) <= 100 else -100
                }
                # Pour R², on affiche normalement, pour les erreurs on les affiche en négatif
                y_range = None  # Auto-range
                text_template = '%{text:.3f}'
            
            metrics_df = pd.DataFrame({
                'Métrique': list(metrics_data.keys()),
                'Valeur': list(metrics_data.values())
            })
            
            fig_perf = px.bar(
                metrics_df,
                x='Métrique',
                y='Valeur',
                color='Valeur',
                color_continuous_scale='Purples',
                text='Valeur'
            )
            
            fig_perf.update_traces(texttemplate=text_template, textposition='outside')
            fig_perf.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            
            if y_range:
                fig_perf.update_layout(yaxis=dict(range=y_range))
            
            st.plotly_chart(fig_perf, use_container_width=True)
            
            # ✅ Métriques additionnelles selon le type
            if problem_type == 'Classification':
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    train_acc = metrics.get('train_accuracy', 0)
                    st.metric("Train Accuracy", f"{train_acc*100:.1f}%")
                with col_m2:
                    cv_mean = metrics.get('cv_mean', 0)
                    st.metric("CV Score", f"{cv_mean*100:.1f}%" if cv_mean > 0 else "N/A")
            else:  # Regression
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    train_r2 = metrics.get('train_r2', 0)
                    st.metric("Train R²", f"{train_r2:.3f}")
                with col_m2:
                    cv_r2 = metrics.get('cv_mean', 0)
                    st.metric("CV R²", f"{cv_r2:.3f}" if cv_r2 != 0 else "N/A")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Section Métriques détaillées
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📈 Métriques Détaillées</div>', unsafe_allow_html=True)
        

        if problem_type == 'Classification':
            col_d1, col_d2, col_d3, col_d4 = st.columns(4)
            
            with col_d1:
                st.metric(
                    "Test Accuracy",
                    f"{metrics.get('test_accuracy', 0)*100:.2f}%",
                    delta=f"{(metrics.get('test_accuracy', 0) - metrics.get('train_accuracy', 0))*100:.2f}%"
                )
            with col_d2:
                st.metric(
                    "Precision",
                    f"{metrics.get('precision', 0)*100:.2f}%"
                )
            with col_d3:
                st.metric(
                    "Recall",
                    f"{metrics.get('recall', 0)*100:.2f}%"
                )
            with col_d4:
                st.metric(
                    "F1-Score",
                    f"{metrics.get('f1_score', 0)*100:.2f}%"
                )
        else:  # Regression
            col_d1, col_d2, col_d3, col_d4 = st.columns(4)
            
            with col_d1:
                st.metric(
                    "R² Score",
                    f"{metrics.get('test_r2', 0):.4f}",
                    delta=f"{(metrics.get('test_r2', 0) - metrics.get('train_r2', 0)):.4f}" if metrics.get('train_r2') else None
                )
            with col_d2:
                st.metric(
                    "RMSE",
                    f"{metrics.get('rmse', 0):.4f}",
                    help="Root Mean Squared Error - Plus faible est mieux"
                )
            # with col_d3:
            #     st.metric(
            #         "MAE",
            #         f"{metrics.get('mae', 0):.4f}",
            #         help="Mean Absolute Error - Plus faible est mieux"
            #     )
            # with col_d4:
            #     mape = metrics.get('mape', 0)
            #     st.metric(
            #         "MAPE",
            #         f"{mape:.2f}%" if mape <= 100 else "N/A",
            #         help="Mean Absolute Percentage Error"
            #     )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Section Téléchargement
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📥 Téléchargement du Modèle</div>', unsafe_allow_html=True)
        
        col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)
        
        with col_dl1:
            st.markdown("""
            <div class="download-card">
                <div class="download-icon">📦</div>
                <div class="download-title">Pickle (.pkl)</div>
                <div class="download-description">Format Python natif, compatible scikit-learn</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Télécharger PKL", key="dl_pkl", use_container_width=True):
                with show_loading("Préparation du fichier..."):
                    try:
                        model_bytes = api_client.download_model(selected_model['id'])
                        st.download_button(
                            label="📥 Télécharger .pkl",
                            data=model_bytes,
                            file_name=f"{selected_model['name'].replace(' ', '_')}.pkl",
                            mime="application/octet-stream",
                            key="dl_pkl_file"
                        )
                        show_success("✅ Fichier prêt au téléchargement!")
                    except Exception as e:
                        show_error(f"❌ Erreur: {str(e)}")
        
        with col_dl2:
            st.markdown("""
            <div class="download-card">
                <div class="download-icon">📊</div>
                <div class="download-title">Métriques JSON</div>
                <div class="download-description">Métriques détaillées au format JSON</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Télécharger JSON", key="dl_json", use_container_width=True):
                import json
                metrics_data = {
                    "model_id": selected_model['id'],
                    "model_name": selected_model['name'],
                    "model_type": selected_model['type'],
                    "problem_type": problem_type,
                    "metrics": metrics,
                    "created_at": selected_model['date'].isoformat(),
                    "download_date": datetime.now().isoformat()
                }
                
                st.download_button(
                    label="📥 Télécharger .json",
                    data=json.dumps(metrics_data, indent=2),
                    file_name=f"{selected_model['name'].replace(' ', '_')}_metrics.json",
                    mime="application/json",
                    key="dl_json_file"
                )
        
        with col_dl3:
            st.markdown("""
            <div class="download-card">
                <div class="download-icon">📋</div>
                <div class="download-title">Rapport PDF</div>
                <div class="download-description">Rapport complet d'évaluation</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Générer PDF", key="dl_pdf", use_container_width=True):
                with show_loading("Génération du rapport..."):
                    import time
                    time.sleep(2)
                    show_success("✅ Rapport généré!")
        
        with col_dl4:
            st.markdown("""
            <div class="download-card">
                <div class="download-icon">⚙️</div>
                <div class="download-title">Configuration</div>
                <div class="download-description">Paramètres et configuration</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Télécharger Config", key="dl_config", use_container_width=True):
                st.info("📋 Configuration téléchargée!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Code d'exemple d'utilisation
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💻 Code d\'Exemple d\'Utilisation</div>', unsafe_allow_html=True)
        
        # Tabs pour différents langages
        tab_python, tab_api, tab_curl = st.tabs(["🐍 Python", "🔌 API REST", "📡 cURL"])
        
        with tab_python:
            prediction_example = "prediction = model.predict(X_new)" if problem_type == 'Classification' else "predictions = model.predict(X_new)"
            proba_code = """
<span class="code-comment"># Obtenir les probabilités (Classification uniquement)</span>
<span class="code-keyword">if</span> <span class="code-function">hasattr</span>(model, <span class="code-string">'predict_proba'</span>):
    probabilities = model.<span class="code-function">predict_proba</span>(X_new)
    <span class="code-function">print</span>(<span class="code-string">f"Probabilités: {{probabilities[0]}}"</span>)
            """ if problem_type == 'Classification' else """
<span class="code-comment"># Pour la régression, prédiction directe de valeurs continues</span>
<span class="code-function">print</span>(<span class="code-string">f"Valeurs prédites: {{predictions}}"</span>)
            """
            
            st.markdown(f"""
            <div class="code-block">
<span class="code-comment"># Charger le modèle téléchargé</span>
<span class="code-keyword">import</span> pickle
<span class="code-keyword">import</span> numpy <span class="code-keyword">as</span> np

<span class="code-comment"># Charger le modèle depuis le fichier</span>
<span class="code-keyword">with</span> <span class="code-function">open</span>(<span class="code-string">'{selected_model['name'].replace(' ', '_')}.pkl'</span>, <span class="code-string">'rb'</span>) <span class="code-keyword">as</span> f:
    model = pickle.<span class="code-function">load</span>(f)

<span class="code-comment"># Préparer les données d'entrée ({selected_model['features']} features)</span>
X_new = np.<span class="code-function">array</span>([[feature1, feature2, ..., feature{selected_model['features']}]])

<span class="code-comment"># Faire une prédiction</span>
{prediction_example}
<span class="code-function">print</span>(<span class="code-string">f"Prédiction: {{prediction[0]}}"</span>)

{proba_code}
            </div>
            """, unsafe_allow_html=True)
        
        with tab_api:
            st.markdown(f"""
            <div class="code-block">
<span class="code-comment"># Utiliser l'API FrameML pour les prédictions</span>
<span class="code-keyword">import</span> requests
<span class="code-keyword">import</span> json

url = <span class="code-string">'http://localhost:8000/api/predict'</span>
headers = {{
    <span class="code-string">'Content-Type'</span>: <span class="code-string">'application/json'</span>
}}

data = {{
    <span class="code-string">'model_id'</span>: <span class="code-string">'{selected_model['id']}'</span>,
    <span class="code-string">'problem_type'</span>: <span class="code-string">'{problem_type}'</span>,
    <span class="code-string">'features'</span>: [feature1, feature2, ..., feature{selected_model['features']}]
}}

<span class="code-keyword">try</span>:
    response = requests.<span class="code-function">post</span>(url, json=data, headers=headers)
    response.<span class="code-function">raise_for_status</span>()
    
    result = response.<span class="code-function">json</span>()
    <span class="code-function">print</span>(<span class="code-string">f"Prédiction: {{result['prediction']}}"</span>)
    {'<span class="code-function">print</span>(<span class="code-string">f"Probabilités: {{result.get(\'probabilities\', \'N/A\')}}"</span>)' if problem_type == 'Classification' else '<span class="code-function">print</span>(<span class="code-string">f"Métriques: R²={{result.get(\'r2\', \'N/A\')}}, RMSE={{result.get(\'rmse\', \'N/A\')}}"</span>)'}
    
<span class="code-keyword">except</span> requests.<span class="code-function">RequestException</span> <span class="code-keyword">as</span> e:
    <span class="code-function">print</span>(<span class="code-string">f"Erreur API: {{e}}"</span>)
            </div>
            """, unsafe_allow_html=True)
        
        with tab_curl:
            st.markdown(f"""
            <div class="code-block">
<span class="code-comment"># Requête cURL vers l'API FrameML</span>
curl -X POST <span class="code-string">"http://localhost:8000/api/predict"</span> \\
  -H <span class="code-string">"Content-Type: application/json"</span> \\
  -d <span class="code-string">'{{
    "model_id": "{selected_model['id']}",
    "problem_type": "{problem_type}",
    "features": [feature1, feature2, ..., feature{selected_model['features']}]
  }}'</span>

<span class="code-comment"># Réponse attendue pour {problem_type}:</span>
<span class="code-comment"># {{</span>
<span class="code-comment">#   "status": "success",</span>
<span class="code-comment">#   "prediction": {'[classe_prédite]' if problem_type == 'Classification' else '[valeur_continue]'},</span>
{'<span class="code-comment">#   "probabilities": [liste_probabilités]</span>' if problem_type == 'Classification' else '<span class="code-comment">#   "metrics": {{"r2": ..., "rmse": ...}}</span>'}
<span class="code-comment"># }}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Actions rapides
        st.markdown('<div class="detail-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚡ Actions Rapides</div>', unsafe_allow_html=True)
        
        col_act1, col_act2, col_act3, col_act4 = st.columns(4)
        
        with col_act1:
            if st.button("🚀 Tester le Modèle", key="test_model", use_container_width=True, type="primary"):
                st.info("🧪 Redirection vers l'interface de test...")
        
        with col_act2:
            if st.button("📊 Voir les Résultats", key="view_results", use_container_width=True):
                st.info("📊 Redirection vers les résultats...")
        
        with col_act3:
            if st.button("📋 Dupliquer le Modèle", key="duplicate_model", use_container_width=True):
                st.info("📋 Duplication du modèle...")
        
        with col_act4:
            if st.button("🗑️ Supprimer le Modèle", key="delete_model", use_container_width=True):
                if st.checkbox("Confirmer la suppression", key="confirm_delete"):
                    with show_loading("Suppression du modèle..."):
                        try:
                            result = api_client.delete_model(selected_model['id'])
                            show_success("✅ Modèle supprimé avec succès!")
                            api_models = load_models_from_api()
                            if api_models:
                                st.session_state.models_list = format_model_data(api_models)
                            st.session_state.view_mode = "list"
                            st.rerun()
                        except Exception as e:
                            show_error(f"❌ Erreur lors de la suppression: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Graphique d'évolution des modèles (si en mode liste)
if st.session_state.view_mode == "list" and st.session_state.models_list:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="detail-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Évolution des Performances</div>', unsafe_allow_html=True)
    
    # Séparer les modèles par type
    classification_models = [m for m in st.session_state.models_list if m['problem_type'] == 'Classification']
    regression_models = [m for m in st.session_state.models_list if m['problem_type'] == 'Regression']
    
    tab_class, tab_reg = st.tabs(["📊 Classification", "📈 Régression"])
    
    with tab_class:
        if len(classification_models) > 1:
            models_df = pd.DataFrame(classification_models)
            models_df = models_df.sort_values('date')
            
            fig_evolution = go.Figure()
            
            fig_evolution.add_trace(go.Scatter(
                x=models_df['date'],
                y=models_df['primary_metric'] * 100,  # Convertir en %
                mode='lines+markers',
                name='Accuracy',
                line=dict(color='#667eea', width=3),
                marker=dict(size=10, color='#667eea', line=dict(width=2, color='white')),
                text=models_df['name'],
                hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Accuracy: %{y:.1f}%<extra></extra>'
            ))
            
            fig_evolution.update_layout(
                height=400,
                margin=dict(l=0, r=0, t=20, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title='Date de Création', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                yaxis=dict(title='Accuracy (%)', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                hovermode='closest'
            )
            
            st.plotly_chart(fig_evolution, use_container_width=True)
        else:
            st.info("ℹ️ Plusieurs modèles de classification sont nécessaires pour afficher l'évolution.")
    
    with tab_reg:
        if len(regression_models) > 1:
            models_df = pd.DataFrame(regression_models)
            models_df = models_df.sort_values('date')
            
            fig_evolution = go.Figure()
            
            fig_evolution.add_trace(go.Scatter(
                x=models_df['date'],
                y=models_df['primary_metric'],  # R² (pas de conversion)
                mode='lines+markers',
                name='R² Score',
                line=dict(color='#10b981', width=3),
                marker=dict(size=10, color='#10b981', line=dict(width=2, color='white')),
                text=models_df['name'],
                hovertemplate='<b>%{text}</b><br>Date: %{x}<br>R²: %{y:.3f}<extra></extra>'
            ))
            
            fig_evolution.update_layout(
                height=400,
                margin=dict(l=0, r=0, t=20, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title='Date de Création', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                yaxis=dict(title='R² Score', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
                hovermode='closest'
            )
            
            st.plotly_chart(fig_evolution, use_container_width=True)
        else:
            st.info("ℹ️ Plusieurs modèles de régression sont nécessaires pour afficher l'évolution.")
    
    st.markdown('</div>', unsafe_allow_html=True)



## SESSION
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
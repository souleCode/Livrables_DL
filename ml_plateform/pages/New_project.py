import streamlit as st
import pandas as pd
import numpy as np
import time
from utils.Client import api_client
from utils.Helpers import show_loading, show_success, show_error

# Configuration de la page
st.set_page_config(
    page_title="Nouveau Projet - FrameML",
    page_icon="➕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation de la session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'project_name' not in st.session_state:
    st.session_state.project_name = ""
if 'project_description' not in st.session_state:
    st.session_state.project_description = ""
if 'problem_type' not in st.session_state:
    st.session_state.problem_type = "ML Classique"
if 'task_type' not in st.session_state:
    st.session_state.task_type = "Classification"
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'target_column' not in st.session_state:
    st.session_state.target_column = None
if 'project_id' not in st.session_state:
    st.session_state.project_id = None
if 'data_analysis' not in st.session_state:
    st.session_state.data_analysis = None

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
    
    /* Stepper */
    .stepper-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stepper {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        margin-bottom: 1rem;
    }
    
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
        flex: 1;
        position: relative;
        z-index: 1;
    }
    
    .step-circle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        transition: all 0.3s;
    }
    
    .step-circle.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 8px rgba(102,126,234,0.4);
        transform: scale(1.1);
    }
    
    .step-circle.completed {
        background: #10b981;
        color: white;
    }
    
    .step-circle.inactive {
        background: #e5e7eb;
        color: #9ca3af;
    }
    
    .step-label {
        font-size: 0.9rem;
        font-weight: 600;
        text-align: center;
    }
    
    .step-label.active {
        color: #667eea;
    }
    
    .step-label.completed {
        color: #10b981;
    }
    
    .step-label.inactive {
        color: #9ca3af;
    }
    
    /* Content card */
    .content-card {
        background: white;
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    
    /* Upload zone */
    .upload-zone {
        border: 3px dashed #667eea;
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        background: #f8f9ff;
        transition: all 0.3s;
        cursor: pointer;
    }
    
    .upload-zone:hover {
        background: #f0f2ff;
        border-color: #764ba2;
    }
    
    .upload-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    /* Info box */
    .info-box {
        background: #f0f9ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Variable card */
    .variable-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        border: 1px solid #e5e7eb;
    }
    
    .variable-name {
        font-weight: 600;
        color: #333;
        font-size: 1.1rem;
    }
    
    .variable-type {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 FrameML")
    st.markdown("---")
    st.markdown("#### 📍 Navigation")
    if st.button("⬅️ Retour au Dashboard", use_container_width=True):
        st.session_state.current_step = 1
        st.switch_page("app.py")
    st.markdown("---")
    st.markdown("#### 💡 Aide")
    st.info("**Étape 1**: Définissez les informations de base de votre projet")
    st.info("**Étape 2**: Importez vos données (CSV, Excel, JSON)")
    st.info("**Étape 3**: Configurez les variables et le prétraitement")

# Header
st.markdown("""
<div class="page-header">
    <h1>➕ Créer un Nouveau Projet</h1>
    <p>Suivez les étapes pour configurer votre projet ML/Deep Learning</p>
</div>
""", unsafe_allow_html=True)

# Stepper
step_status = lambda x: "completed" if x < st.session_state.current_step else ("active" if x == st.session_state.current_step else "inactive")

st.markdown(f"""
<div class="stepper-container">
    <div class="stepper">
        <div class="step">
            <div class="step-circle {step_status(1)}">
                {'✓' if st.session_state.current_step > 1 else '1'}
            </div>
            <div class="step-label {step_status(1)}">Informations</div>
        </div>
        <div class="step">
            <div class="step-circle {step_status(2)}">
                {'✓' if st.session_state.current_step > 2 else '2'}
            </div>
            <div class="step-label {step_status(2)}">Upload Données</div>
        </div>
        <div class="step">
            <div class="step-circle {step_status(3)}">
                {'✓' if st.session_state.current_step > 3 else '3'}
            </div>
            <div class="step-label {step_status(3)}">Configuration</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ========== ÉTAPE 1: INFORMATIONS DE BASE ==========
if st.session_state.current_step == 1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📝 Informations de Base du Projet</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.session_state.project_name = st.text_input(
            "Nom du Projet *",
            value=st.session_state.project_name,
            placeholder="Ex: Prédiction Prix Immobilier",
            help="Donnez un nom descriptif à votre projet"
        )
        
        st.session_state.project_description = st.text_area(
            "Description",
            value=st.session_state.project_description,
            placeholder="Décrivez brièvement l'objectif de votre projet...",
            height=120,
            help="Optionnel: Ajoutez une description pour mieux organiser vos projets"
        )
    
    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("**💡 Conseils**")
        st.markdown("- Utilisez un nom clair et descriptif")
        st.markdown("- Mentionnez le domaine d'application")
        st.markdown("- Indiquez le type de problème")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Type de problème et tâche
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Type de Problème")
        st.session_state.problem_type = st.radio(
            "Choisissez le type de problème",
            ["ML Classique", "Deep Learning"],
            horizontal=True,
            help="ML Classique pour des données tabulaires, Deep Learning pour images, texte, séries temporelles"
        )
        
        if st.session_state.problem_type == "ML Classique":
            st.info("🔹 **ML Classique**: Random Forest, XGBoost, SVM, Régression Logistique, etc.")
        else:
            st.info("🔹 **Deep Learning**: CNN, RNN, LSTM, Transformers, AutoEncoders, etc.")
    
    with col2:
        st.markdown("#### 📊 Type de Tâche")
        st.session_state.task_type = st.radio(
            "Choisissez le type de tâche",
            ["Classification", "Régression"],
            horizontal=True,
            help="Classification pour prédire des catégories, Régression pour prédire des valeurs continues"
        )
        
        if st.session_state.task_type == "Classification":
            st.info("📈 **Classification**: Prédire des catégories (Ex: Spam/Non-spam, Fraude/Non-fraude)")
        else:
            st.info("📉 **Régression**: Prédire des valeurs continues (Ex: Prix, Température, Ventes)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Boutons de navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("Suivant ➡️", use_container_width=True, type="primary"):
            if st.session_state.project_name:
                # Créer le projet via API
                with show_loading("Création du projet..."):
                    try:
                        project_id = api_client.create_project(
                            name=st.session_state.project_name,
                            description=st.session_state.project_description,
                            problem_type=st.session_state.problem_type,
                            task_type=st.session_state.task_type
                        )
                        st.session_state.project_id = project_id
                        show_success("✅ Projet créé avec succès!")
                        st.session_state.current_step = 2
                        st.rerun()
                    except Exception as e:
                        show_error(f"❌ Erreur lors de la création du projet: {str(e)}")
            else:
                st.error("⚠️ Veuillez entrer un nom de projet")

# ========== ÉTAPE 2: UPLOAD DES DONNÉES ==========
elif st.session_state.current_step == 2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📤 Upload des Données</div>', unsafe_allow_html=True)
    
    # Vérifier qu'un projet existe
    if not st.session_state.project_id:
        st.error("❌ Aucun projet créé. Veuillez retourner à l'étape 1.")
        if st.button("⬅️ Retour à l'étape 1"):
            st.session_state.current_step = 1
            st.rerun()
        st.stop()
    
    st.markdown("""
    <div class="info-box">
        <strong>📋 Formats supportés:</strong> CSV, Excel (.xlsx, .xls), JSON
        <br><strong>📏 Taille maximale:</strong> 200 MB
    </div>
    """, unsafe_allow_html=True)
    
    # Zone d'upload
    uploaded_file = st.file_uploader(
        "Glissez-déposez votre fichier ici ou cliquez pour parcourir",
        type=['csv', 'xlsx', 'xls', 'json'],
        help="Sélectionnez un fichier contenant vos données d'entraînement"
    )
    
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        
        # Afficher la progression
        with st.spinner("📊 Chargement et analyse des données..."):
            progress_bar = st.progress(0)
            
            try:
                # Upload vers l'API
                response = api_client.upload_data(st.session_state.project_id, uploaded_file)
                
                # Mettre à jour la progression
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Stocker l'analyse des données
                st.session_state.data_analysis = response["analysis"]
                
                # Charger les données localement pour l'affichage
                if uploaded_file.name.endswith('.csv'):
                    st.session_state.df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                    st.session_state.df = pd.read_excel(uploaded_file)
                elif uploaded_file.name.endswith('.json'):
                    st.session_state.df = pd.read_json(uploaded_file)
                
                st.markdown("""
                <div class="success-box">
                    ✅ <strong>Fichier chargé avec succès!</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Informations sur le dataset
                analysis = st.session_state.data_analysis
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📊 Lignes", f"{analysis['rows']:,}")
                with col2:
                    st.metric("📋 Colonnes", analysis['columns'])
                with col3:
                    st.metric("💾 Taille", f"{uploaded_file.size / (1024*1024):.2f} MB")
                with col4:
                    missing = sum(analysis['missing_values'].values())
                    st.metric("❓ Valeurs manquantes", f"{missing:,}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Prévisualisation
                st.markdown("#### 👀 Prévisualisation des Données (10 premières lignes)")
                preview_df = pd.DataFrame(analysis['preview'])
                st.dataframe(preview_df, use_container_width=True, height=300)
                
                # Statistiques descriptives
                with st.expander("📊 Statistiques Descriptives"):
                    if analysis.get('statistics'):
                        stats_df = pd.DataFrame(analysis['statistics'])
                        st.dataframe(stats_df, use_container_width=True)
                
                # Types de colonnes
                with st.expander("🔍 Types de Colonnes"):
                    col_types = analysis['column_types']
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Numériques:**")
                        for col in analysis['numeric_columns']:
                            st.write(f"- `{col}`: {col_types.get(col, 'N/A')}")
                    with col2:
                        st.markdown("**Catégorielles:**")
                        for col in analysis['categorical_columns']:
                            st.write(f"- `{col}`: {col_types.get(col, 'N/A')}")
                
            except Exception as e:
                st.error(f"❌ Erreur lors du chargement du fichier: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Boutons de navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Précédent", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    with col3:
        if st.button("Suivant ➡️", use_container_width=True, type="primary"):
            if st.session_state.df is not None:
                st.session_state.current_step = 3
                st.rerun()
            else:
                st.error("⚠️ Veuillez d'abord uploader un fichier")

# ========== ÉTAPE 3: CONFIGURATION DES DONNÉES ==========
elif st.session_state.current_step == 3:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙️ Configuration des Données</div>', unsafe_allow_html=True)
    
    if st.session_state.df is not None and st.session_state.data_analysis is not None:
        # Sélection de la variable cible
        st.markdown("#### 🎯 Sélection de la Variable Cible")
        st.session_state.target_column = st.selectbox(
            "Choisissez la colonne cible (variable à prédire)",
            options=st.session_state.df.columns.tolist(),
            help="Sélectionnez la variable que vous souhaitez prédire"
        )
        
        if st.session_state.target_column:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Variable cible:** `{st.session_state.target_column}`")
                target_values = st.session_state.df[st.session_state.target_column].nunique()
                st.markdown(f"**Valeurs uniques:** {target_values}")
                
                # Afficher le type de la variable cible
                target_type = st.session_state.data_analysis['column_types'].get(st.session_state.target_column, 'N/A')
                st.markdown(f"**Type:** {target_type}")
                
            with col2:
                if target_values <= 10:
                    st.markdown("**Distribution des valeurs:**")
                    value_counts = st.session_state.df[st.session_state.target_column].value_counts()
                    st.bar_chart(value_counts)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Identification des types de variables
        st.markdown("#### 🔍 Types de Variables Détectés")
        
        analysis = st.session_state.data_analysis
        numeric_cols = analysis['numeric_columns']
        categorical_cols = analysis['categorical_columns']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 🔢 Variables Numériques")
            for col in numeric_cols:
                missing = analysis['missing_values'].get(col, 0)
                st.markdown(f"""
                <div class="variable-card">
                    <span class="variable-name">{col}</span>
                    <span class="variable-type" style="background: #dbeafe; color: #1e40af;">Numérique</span>
                    <br><small>Valeurs manquantes: {missing}</small>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("##### 📝 Variables Catégorielles")
            for col in categorical_cols:
                missing = analysis['missing_values'].get(col, 0)
                st.markdown(f"""
                <div class="variable-card">
                    <span class="variable-name">{col}</span>
                    <span class="variable-type" style="background: #fef3c7; color: #92400e;">Catégorielle</span>
                    <br><small>Valeurs manquantes: {missing}</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Options de prétraitement
        st.markdown("#### 🛠️ Options de Prétraitement")
        
        col1, col2 = st.columns(2)
        
        with col1:
            handle_missing = st.checkbox("Traiter les valeurs manquantes", value=True)
            if handle_missing:
                missing_strategy = st.selectbox(
                    "Stratégie:",
                    ["mean", "median", "drop", "zero"],
                    format_func=lambda x: {
                        "mean": "Moyenne/Médiane",
                        "median": "Médiane",
                        "drop": "Supprimer les lignes",
                        "zero": "Remplir par 0"
                    }[x]
                )
        
        with col2:
            normalize = st.checkbox("Normaliser les données", value=True)
            if normalize:
                norm_method = st.selectbox(
                    "Méthode:",
                    ["StandardScaler", "MinMaxScaler", "RobustScaler"]
                )
        
        encode_categorical = st.checkbox("Encoder les variables catégorielles", value=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Boutons de navigation
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("⬅️ Précédent", use_container_width=True):
                st.session_state.current_step = 2
                st.rerun()
        with col3:
            if st.button("✅ Configurer les Données", use_container_width=True, type="primary"):
                if st.session_state.target_column:
                    with st.spinner("🚀 Configuration des données en cours..."):
                        try:
                            # Configuration via API
                            config_data = {
                                "handle_missing": handle_missing,
                                "missing_strategy": missing_strategy if handle_missing else None,
                                "normalize": normalize,
                                "normalize_method": norm_method if normalize else None
                            }
                            
                            response = api_client.configure_data(
                                project_id=st.session_state.project_id,
                                target_column=st.session_state.target_column,
                                **config_data
                            )
                            
                            show_success("✅ Données configurées avec succès!")
                            st.balloons()
                            
                            # Redirection vers la configuration du modèle
                            time.sleep(2)
                            st.switch_page("pages/config_model.py")
                            
                        except Exception as e:
                            show_error(f"❌ Erreur lors de la configuration: {str(e)}")
                else:
                    st.error("⚠️ Veuillez sélectionner une variable cible")


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
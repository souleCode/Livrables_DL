import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.Client import api_client
from utils.Helpers import show_loading, show_success, show_error

# Configuration de la page
st.set_page_config(
    page_title="Configuration du Modèle - FrameML",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Vérifier qu'un projet existe
if 'project_id' not in st.session_state:
    st.error("❌ Aucun projet trouvé. Veuillez d'abord créer un projet.")
    st.switch_page("pages/New_project.py")

# Récupérer les informations du projet
try:
    project = api_client.get_project(st.session_state.project_id)
    problem_type = project['problem_type']  # 'Classification' ou 'Regression'
except:
    st.error("❌ Impossible de charger les informations du projet")
    st.stop()

# Initialisation de la session state
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = None
if 'model_category' not in st.session_state:
    st.session_state.model_category = "ML Classique"
if 'advanced_mode' not in st.session_state:
    st.session_state.advanced_mode = False
if 'training_config' not in st.session_state:
    st.session_state.training_config = {}

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
    
    /* Model card */
    .model-card {
        background: white;
        padding: 1.8rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 2px solid transparent;
        transition: all 0.3s;
        cursor: pointer;
        height: 100%;
        position: relative;
    }
    
    .model-card:hover {
        border-color: #667eea;
        box-shadow: 0 6px 16px rgba(102,126,234,0.2);
        transform: translateY(-5px);
    }
    
    .model-card.selected {
        border-color: #667eea;
        background: linear-gradient(135deg, rgba(102,126,234,0.05) 0%, rgba(118,75,162,0.05) 100%);
        box-shadow: 0 6px 16px rgba(102,126,234,0.3);
    }
    
    .model-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .model-name {
        font-size: 1.4rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .model-description {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    
    .model-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .recommended-badge {
        position: absolute;
        top: -10px;
        right: 10px;
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    
    /* Section card */
    .section-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    
    /* Info box */
    .info-box {
        background: #f0f9ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Parameter row */
    .param-row {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        border: 1px solid #e5e7eb;
    }
    
    .param-label {
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .param-description {
        color: #666;
        font-size: 0.85rem;
        font-style: italic;
    }
    
    /* Metric display */
    .metric-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 FrameML")
    st.markdown("---")
    
    # Informations du projet
    st.markdown("#### 📊 Projet Actuel")
    st.markdown(f"**{project['name']}**")
    st.markdown(f"{project['task_type']} • {project['problem_type']}")
    st.markdown(f"*ID: {st.session_state.project_id[:8]}...*")
    
    # print(f"=================Project detail CONFIG MODEL:{project}==========================")

    st.markdown("---")
    
    st.markdown("#### 📍 Navigation")
    if st.button("⬅️ Retour au Dashboard", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("📝 Modifier les Données", use_container_width=True):
        st.switch_page("pages/New_project.py")
    
    st.markdown("---")
    
    st.markdown("#### 💡 Aide Rapide")
    if problem_type == "Classification":
        st.info("**Classification**: Prédire des catégories ou classes discrètes")
    else:
        st.info("**Régression**: Prédire des valeurs numériques continues")

# Header
st.markdown(f"""
<div class="page-header">
    <h1>🤖 Configuration du Modèle</h1>
    <p>Choisissez et configurez le modèle pour votre projet de <strong>{problem_type}</strong></p>
</div>
""", unsafe_allow_html=True)

# Tabs pour catégories de modèles
tab1, tab2 = st.tabs(["🔷 ML Classique", "🧠 Deep Learning"])

# ========== ML CLASSIQUE ==========
with tab1:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown(f"**💡 Modèles de Machine Learning Classique pour {problem_type}** - Performants pour les données tabulaires avec des temps d'entraînement rapides")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Modèles ML Classique
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🌲 Random Forest", key="rf_btn", use_container_width=True):
            st.session_state.selected_model = "Random Forest"
            st.session_state.model_category = "ML Classique"
            st.rerun()
        
        is_selected = st.session_state.selected_model == "Random Forest"
        description = "Ensemble d'arbres de décision robuste et performant pour la classification et régression." if problem_type == "Classification" else "Ensemble d'arbres de décision pour prédire des valeurs continues avec précision."
        st.markdown(f"""
        <div class="model-card {'selected' if is_selected else ''}">
            <span class="recommended-badge">⭐ Recommandé</span>
            <div class="model-icon">🌲</div>
            <div class="model-name">Random Forest</div>
            <div class="model-description">
                {description}
            </div>
            <span class="model-badge" style="background: #dbeafe; color: #1e40af;">Robuste</span>
            <span class="model-badge" style="background: #d1fae5; color: #065f46;">Rapide</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("⚡ XGBoost", key="xgb_btn", use_container_width=True):
            st.session_state.selected_model = "XGBoost"
            st.session_state.model_category = "ML Classique"
            st.rerun()
        
        is_selected = st.session_state.selected_model == "XGBoost"
        st.markdown(f"""
        <div class="model-card {'selected' if is_selected else ''}">
            <div class="model-icon">⚡</div>
            <div class="model-name">XGBoost</div>
            <div class="model-description">
                Gradient boosting puissant et optimisé. Excellent pour les compétitions de données.
            </div>
            <span class="model-badge" style="background: #fef3c7; color: #92400e;">Performant</span>
            <span class="model-badge" style="background: #dbeafe; color: #1e40af;">Précis</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if problem_type == "Classification":
            if st.button("📐 SVM", key="svm_btn", use_container_width=True):
                st.session_state.selected_model = "SVM"
                st.session_state.model_category = "ML Classique"
                st.rerun()
            
            is_selected = st.session_state.selected_model == "SVM"
            st.markdown(f"""
            <div class="model-card {'selected' if is_selected else ''}">
                <div class="model-icon">📐</div>
                <div class="model-name">SVM</div>
                <div class="model-description">
                    Support Vector Machine. Efficace pour les problèmes de classification avec marges optimales.
                </div>
                <span class="model-badge" style="background: #e0e7ff; color: #3730a3;">Mathématique</span>
                <span class="model-badge" style="background: #dbeafe; color: #1e40af;">Stable</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button("📐 SVR", key="svr_btn", use_container_width=True):
                st.session_state.selected_model = "SVR"
                st.session_state.model_category = "ML Classique"
                st.rerun()
            
            is_selected = st.session_state.selected_model == "SVR"
            st.markdown(f"""
            <div class="model-card {'selected' if is_selected else ''}">
                <div class="model-icon">📐</div>
                <div class="model-name">SVR</div>
                <div class="model-description">
                    Support Vector Regression. Efficace pour prédire des valeurs continues avec des relations non-linéaires.
                </div>
                <span class="model-badge" style="background: #e0e7ff; color: #3730a3;">Mathématique</span>
                <span class="model-badge" style="background: #dbeafe; color: #1e40af;">Non-linéaire</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        model_name = "Logistic Regression" if problem_type == "Classification" else "Linear Regression"
        button_label = "📊 Régression Logistique" if problem_type == "Classification" else "📊 Régression Linéaire"
        
        if st.button(button_label, key="lr_btn", use_container_width=True):
            st.session_state.selected_model = model_name
            st.session_state.model_category = "ML Classique"
            st.rerun()
        
        is_selected = st.session_state.selected_model == model_name
        description = "Modèle linéaire simple et interprétable. Idéal pour une baseline rapide." if problem_type == "Classification" else "Modèle linéaire simple. Idéal pour les relations linéaires et une baseline rapide."
        st.markdown(f"""
        <div class="model-card {'selected' if is_selected else ''}">
            <div class="model-icon">📊</div>
            <div class="model-name">{button_label.replace('📊 ', '')}</div>
            <div class="model-description">
                {description}
            </div>
            <span class="model-badge" style="background: #d1fae5; color: #065f46;">Simple</span>
            <span class="model-badge" style="background: #fef3c7; color: #92400e;">Rapide</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        if problem_type == "Classification":
            if st.button("🎯 K-Nearest Neighbors", key="knn_btn", use_container_width=True):
                st.session_state.selected_model = "KNN"
                st.session_state.model_category = "ML Classique"
                st.rerun()
            
            is_selected = st.session_state.selected_model == "KNN"
            st.markdown(f"""
            <div class="model-card {'selected' if is_selected else ''}">
                <div class="model-icon">🎯</div>
                <div class="model-name">K-Nearest Neighbors</div>
                <div class="model-description">
                    Classification basée sur la proximité. Simple à comprendre et interpréter.
                </div>
                <span class="model-badge" style="background: #dbeafe; color: #1e40af;">Intuitif</span>
                <span class="model-badge" style="background: #e0e7ff; color: #3730a3;">Non-paramétrique</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button("🎯 KNN Regression", key="knn_btn", use_container_width=True):
                st.session_state.selected_model = "KNN Regression"
                st.session_state.model_category = "ML Classique"
                st.rerun()
            
            is_selected = st.session_state.selected_model == "KNN Regression"
            st.markdown(f"""
            <div class="model-card {'selected' if is_selected else ''}">
                <div class="model-icon">🎯</div>
                <div class="model-name">KNN Regression</div>
                <div class="model-description">
                    Régression basée sur la proximité. Moyenne des valeurs des k plus proches voisins.
                </div>
                <span class="model-badge" style="background: #dbeafe; color: #1e40af;">Intuitif</span>
                <span class="model-badge" style="background: #e0e7ff; color: #3730a3;">Non-paramétrique</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col6:
        if st.button("🚀 Gradient Boosting", key="gb_btn", use_container_width=True):
            st.session_state.selected_model = "Gradient Boosting"
            st.session_state.model_category = "ML Classique"
            st.rerun()
        
        is_selected = st.session_state.selected_model == "Gradient Boosting"
        st.markdown(f"""
        <div class="model-card {'selected' if is_selected else ''}">
            <div class="model-icon">🚀</div>
            <div class="model-name">Gradient Boosting</div>
            <div class="model-description">
                Boosting séquentiel puissant. Combine plusieurs modèles faibles en un modèle fort.
            </div>
            <span class="model-badge" style="background: #fef3c7; color: #92400e;">Puissant</span>
            <span class="model-badge" style="background: #dbeafe; color: #1e40af;">Précis</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Ajouter d'autres modèles pour la régression
    if problem_type == "Regression":
        st.markdown("<br>", unsafe_allow_html=True)
        col7, col8, col9 = st.columns(3)
        
        with col7:
            if st.button("📈 Ridge Regression", key="ridge_btn", use_container_width=True):
                st.session_state.selected_model = "Ridge"
                st.session_state.model_category = "ML Classique"
                st.rerun()
            
            is_selected = st.session_state.selected_model == "Ridge"
            st.markdown(f"""
            <div class="model-card {'selected' if is_selected else ''}">
                <div class="model-icon">📈</div>
                <div class="model-name">Ridge Regression</div>
                <div class="model-description">
                    Régression linéaire avec régularisation L2. Évite le sur-apprentissage.
                </div>
                <span class="model-badge" style="background: #d1fae5; color: #065f46;">Régularisé</span>
                <span class="model-badge" style="background: #dbeafe; color: #1e40af;">Stable</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col8:
            if st.button("📉 Lasso Regression", key="lasso_btn", use_container_width=True):
                st.session_state.selected_model = "Lasso"
                st.session_state.model_category = "ML Classique"
                st.rerun()
            
            is_selected = st.session_state.selected_model == "Lasso"
            st.markdown(f"""
            <div class="model-card {'selected' if is_selected else ''}">
                <div class="model-icon">📉</div>
                <div class="model-name">Lasso Regression</div>
                <div class="model-description">
                    Régression avec régularisation L1. Effectue une sélection automatique de features.
                </div>
                <span class="model-badge" style="background: #fef3c7; color: #92400e;">Sélection</span>
                <span class="model-badge" style="background: #e0e7ff; color: #3730a3;">Sparse</span>
            </div>
            """, unsafe_allow_html=True)

# ========== DEEP LEARNING ==========
with tab2:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown(f"**🧠 Modèles de Deep Learning pour {problem_type}** - Architectures neuronales avancées pour images, texte et données complexes")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🖼️ CNN", key="cnn_btn", use_container_width=True):
            st.session_state.selected_model = "CNN"
            st.session_state.model_category = "Deep Learning"
            st.rerun()
        
        is_selected = st.session_state.selected_model == "CNN"
        description = "Convolutional Neural Network. Parfait pour la vision par ordinateur et classification d'images." if problem_type == "Classification" else "CNN pour la régression. Extrait des features visuelles pour prédire des valeurs continues."
        st.markdown(f"""
        <div class="model-card {'selected' if is_selected else ''}">
            <span class="recommended-badge">⭐ Recommandé</span>
            <div class="model-icon">🖼️</div>
            <div class="model-name">CNN</div>
            <div class="model-description">
                {description}
            </div>
            <span class="model-badge" style="background: #dbeafe; color: #1e40af;">Images</span>
            <span class="model-badge" style="background: #d1fae5; color: #065f46;">Vision</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("📈 RNN/LSTM", key="rnn_btn", use_container_width=True):
            st.session_state.selected_model = "RNN/LSTM"
            st.session_state.model_category = "Deep Learning"
            st.rerun()
        
        is_selected = st.session_state.selected_model == "RNN/LSTM"
        st.markdown(f"""
        <div class="model-card {'selected' if is_selected else ''}">
            <div class="model-icon">📈</div>
            <div class="model-name">RNN/LSTM</div>
            <div class="model-description">
                Réseaux récurrents pour séries temporelles et séquences. Capture les dépendances temporelles.
            </div>
            <span class="model-badge" style="background: #fef3c7; color: #92400e;">Temporel</span>
            <span class="model-badge" style="background: #e0e7ff; color: #3730a3;">Séquences</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🤖 Transformer", key="trans_btn", use_container_width=True):
            st.session_state.selected_model = "Transformer"
            st.session_state.model_category = "Deep Learning"
            st.rerun()
        
        is_selected = st.session_state.selected_model == "Transformer"
        description = "Architecture d'attention pour NLP. État de l'art pour le traitement du langage naturel." if problem_type == "Classification" else "Transformer pour régression. Architecture d'attention pour séquences et prédictions continues."
        st.markdown(f"""
        <div class="model-card {'selected' if is_selected else ''}">
            <div class="model-icon">🤖</div>
            <div class="model-name">Transformer</div>
            <div class="model-description">
                {description}
            </div>
            <span class="model-badge" style="background: #dbeafe; color: #1e40af;">NLP</span>
            <span class="model-badge" style="background: #fef3c7; color: #92400e;">SOTA</span>
        </div>
        """, unsafe_allow_html=True)

# ========== CONFIGURATION DES PARAMÈTRES ==========
if st.session_state.selected_model:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">⚙️ Configuration - {st.session_state.selected_model}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mode basique / avancé
    col1, col2 = st.columns([3, 1])
    with col2:
        st.session_state.advanced_mode = st.toggle("🔧 Mode Avancé", value=st.session_state.advanced_mode)
    
    # Configuration selon le modèle
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        
        # Variables pour stocker les paramètres
        hyperparameters = {}
        
        if not st.session_state.advanced_mode:
            st.markdown("#### 🎯 Paramètres Recommandés")
            st.info("Les paramètres par défaut sont optimisés pour la plupart des cas d'usage")
        else:
            st.markdown("#### 🔧 Paramètres Avancés")
            
            # Paramètres spécifiques selon le modèle
            if st.session_state.selected_model == "Random Forest":
                col1, col2 = st.columns(2)
                with col1:
                    hyperparameters['n_estimators'] = st.slider("Nombre d'arbres", 10, 500, 100, 10)
                    hyperparameters['max_depth'] = st.slider("Profondeur maximale", 1, 50, 10)
                with col2:
                    hyperparameters['min_samples_split'] = st.slider("Min échantillons split", 2, 20, 2)
                    hyperparameters['min_samples_leaf'] = st.slider("Min échantillons feuille", 1, 20, 1)
                
                if problem_type == "Classification":
                    hyperparameters['criterion'] = st.selectbox("Critère", ["gini", "entropy", "log_loss"])
                else:
                    hyperparameters['criterion'] = st.selectbox("Critère", ["squared_error", "absolute_error", "friedman_mse"])
                
            elif st.session_state.selected_model == "XGBoost":
                col1, col2 = st.columns(2)
                with col1:
                    hyperparameters['n_estimators'] = st.slider("Nombre d'estimateurs", 50, 1000, 100, 50)
                    hyperparameters['learning_rate'] = st.slider("Taux d'apprentissage", 0.01, 0.3, 0.1, 0.01)
                with col2:
                    hyperparameters['max_depth'] = st.slider("Profondeur maximale", 3, 15, 6)
                    hyperparameters['subsample'] = st.slider("Subsample", 0.5, 1.0, 0.8, 0.1)
                
            elif st.session_state.selected_model in ["SVM", "SVR"]:
                hyperparameters['C'] = st.slider("Paramètre C", 0.1, 10.0, 1.0, 0.1)
                hyperparameters['kernel'] = st.selectbox("Noyau", ["rbf", "linear", "poly", "sigmoid"])
                if hyperparameters['kernel'] == 'rbf':
                    hyperparameters['gamma'] = st.selectbox("Gamma", ["scale", "auto"])
                
            elif st.session_state.selected_model in ["Logistic Regression", "Linear Regression"]:
                if problem_type == "Classification":
                    hyperparameters['C'] = st.slider("Paramètre C", 0.1, 10.0, 1.0, 0.1)
                    hyperparameters['solver'] = st.selectbox("Solveur", ["lbfgs", "liblinear", "newton-cg"])
                else:
                    hyperparameters['fit_intercept'] = st.checkbox("Fit Intercept", value=True)
                    hyperparameters['normalize'] = st.checkbox("Normaliser", value=False)
                
            elif st.session_state.selected_model in ["KNN", "KNN Regression"]:
                hyperparameters['n_neighbors'] = st.slider("Nombre de voisins", 3, 15, 5)
                hyperparameters['weights'] = st.selectbox("Poids", ["uniform", "distance"])
                hyperparameters['metric'] = st.selectbox("Métrique", ["euclidean", "manhattan", "minkowski"])
                
            elif st.session_state.selected_model == "Gradient Boosting":
                col1, col2 = st.columns(2)
                with col1:
                    hyperparameters['n_estimators'] = st.slider("Nombre d'estimateurs", 50, 500, 100, 50)
                    hyperparameters['learning_rate'] = st.slider("Taux d'apprentissage", 0.01, 0.3, 0.1, 0.01)
                with col2:
                    hyperparameters['max_depth'] = st.slider("Profondeur maximale", 3, 15, 5)
                    hyperparameters['subsample'] = st.slider("Subsample", 0.5, 1.0, 0.8, 0.1)
                
                if problem_type == "Regression":
                    hyperparameters['loss'] = st.selectbox("Fonction de perte", ["squared_error", "absolute_error", "huber"])
            
            elif st.session_state.selected_model == "Ridge":
                hyperparameters['alpha'] = st.slider("Alpha (régularisation)", 0.1, 10.0, 1.0, 0.1)
                hyperparameters['solver'] = st.selectbox("Solveur", ["auto", "svd", "cholesky", "lsqr"])
                
            elif st.session_state.selected_model == "Lasso":
                hyperparameters['alpha'] = st.slider("Alpha (régularisation)", 0.01, 5.0, 1.0, 0.01)
                hyperparameters['max_iter'] = st.slider("Max itérations", 100, 5000, 1000, 100)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Configuration de l'entraînement
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### 🚀 Configuration de l'Entraînement")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="param-row">', unsafe_allow_html=True)
            st.markdown('<div class="param-label">📊 Train/Test Split</div>', unsafe_allow_html=True)
            train_test_split = st.slider("Taille du set d'entraînement", 0.5, 0.95, 0.8, 0.05)
            st.markdown(f'<div class="param-description">Train: {int(train_test_split*100)}% | Test: {int((1-train_test_split)*100)}%</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.session_state.model_category == "Deep Learning":
                st.markdown('<div class="param-row">', unsafe_allow_html=True)
                st.markdown('<div class="param-label">🔄 Nombre d\'Epochs</div>', unsafe_allow_html=True)
                epochs = st.number_input("Epochs", 1, 1000, 50, label_visibility="collapsed")
                st.markdown('<div class="param-description">Nombre de passages complets sur les données</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="param-row">', unsafe_allow_html=True)
            st.markdown('<div class="param-label">✅ Validation Croisée</div>', unsafe_allow_html=True)
            use_cross_validation = st.checkbox("Activer la validation croisée", value=True)
            if use_cross_validation:
                cv_folds = st.number_input("Nombre de folds", 2, 10, 5, label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="param-row">', unsafe_allow_html=True)
            st.markdown('<div class="param-label">🎯 Random State</div>', unsafe_allow_html=True)
            random_state = st.number_input("Seed aléatoire", 0, 1000, 42, label_visibility="collapsed")
            st.markdown('<div class="param-description">Pour la reproductibilité</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        # Résumé de la configuration
        st.markdown('<div class="metric-display">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">✓</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Modèle Configuré</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### 📋 Résumé")
        st.markdown(f"**Modèle:** {st.session_state.selected_model}")
        st.markdown(f"**Tâche:** {problem_type}")
        st.markdown(f"**Catégorie:** {st.session_state.model_category}")
        st.markdown(f"**Mode:** {'Avancé' if st.session_state.advanced_mode else 'Standard'}")
        st.markdown(f"**Split:** {int(train_test_split*100)}/{int((1-train_test_split)*100)}")
        if use_cross_validation:
            st.markdown(f"**CV Folds:** {cv_folds}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("⚡ **Estimation**")
        st.markdown("Temps d'entraînement: ~15 min")
        st.markdown("Ressources: Moyenne")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Boutons d'action
        if st.button("🚀 Lancer l'Entraînement", use_container_width=True, type="primary"):
            with show_loading("Démarrage de l'entraînement..."):
                try:
                    # Préparer la configuration pour l'API
                    training_config = {
                        "project_id": st.session_state.project_id,
                        "model_type": st.session_state.selected_model,
                        "problem_type": problem_type,  # AJOUT IMPORTANT
                        "hyperparameters": hyperparameters,
                        "train_test_split": train_test_split,
                        "cv_folds": cv_folds if use_cross_validation else 5,
                        "use_cross_validation": use_cross_validation,
                        "random_state": random_state
                    }
                    
                    # Appel API pour démarrer l'entraînement
                    response = api_client.start_training(**training_config)
                    
                    # Sauvegarder les infos pour la page d'entraînement
                    st.session_state.training_config = training_config
                    st.session_state.experiment_id = response["experiment_id"]
                    st.session_state.model_id = response["model_id"]
                    
                    show_success("✅ Entraînement démarré avec succès!")
                    
                    # Redirection vers la page d'entraînement
                    st.switch_page("pages/Entrainement.py")
                    
                except Exception as e:
                    show_error(f"❌ Erreur lors du démarrage de l'entraînement: {str(e)}")
        
        if st.button("💾 Sauvegarder la Config", use_container_width=True):
            st.session_state.training_config = {
                "model_type": st.session_state.selected_model,
                "problem_type": problem_type,
                "hyperparameters": hyperparameters,
                "train_test_split": train_test_split,
                "use_cross_validation": use_cross_validation
            }
            show_success("💾 Configuration sauvegardée!")
        
        if st.button("🔄 Réinitialiser", use_container_width=True):
            st.session_state.selected_model = None
            st.session_state.training_config = {}
            st.rerun()

else:
    # Message si aucun modèle sélectionné
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <h3>👆 Sélectionnez un modèle pour commencer</h3>
        <p>Choisissez un modèle dans les onglets ci-dessus pour configurer les paramètres d'entraînement</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tableau comparatif
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f"#### 📊 Comparaison des Modèles pour {problem_type}")
    
    if problem_type == "Classification":
        comparison_data = pd.DataFrame({
            'Modèle': ['Random Forest', 'XGBoost', 'SVM', 'Logistic Regression', 'KNN', 'Gradient Boosting'],
            'Catégorie': ['ML Classique', 'ML Classique', 'ML Classique', 'ML Classique', 'ML Classique', 'ML Classique'],
            'Vitesse': ['⚡⚡⚡', '⚡⚡', '⚡⚡', '⚡⚡⚡', '⚡⚡⚡', '⚡⚡'],
            'Précision': ['⭐⭐⭐⭐', '⭐⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐⭐'],
            'Complexité': ['Moyenne', 'Élevée', 'Moyenne', 'Faible', 'Faible', 'Élevée'],
            'Cas d\'usage': ['Général', 'Compétitions', 'Classification', 'Baseline', 'Petits datasets', 'Haute précision']
        })
    else:
        comparison_data = pd.DataFrame({
            'Modèle': ['Random Forest', 'XGBoost', 'SVR', 'Linear Regression', 'Ridge', 'Lasso', 'Gradient Boosting', 'KNN Regression'],
            'Catégorie': ['ML Classique', 'ML Classique', 'ML Classique', 'ML Classique', 'ML Classique', 'ML Classique', 'ML Classique', 'ML Classique'],
            'Vitesse': ['⚡⚡⚡', '⚡⚡', '⚡⚡', '⚡⚡⚡', '⚡⚡⚡', '⚡⚡⚡', '⚡⚡', '⚡⚡⚡'],
            'Précision': ['⭐⭐⭐⭐', '⭐⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐⭐', '⭐⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐⭐', '⭐⭐⭐'],
            'Complexité': ['Moyenne', 'Élevée', 'Moyenne', 'Faible', 'Faible', 'Faible', 'Élevée', 'Faible'],
            'Cas d\'usage': ['Général', 'Compétitions', 'Non-linéaire', 'Baseline', 'Régularisé', 'Feature selection', 'Haute précision', 'Proximité']
        })
    
    st.dataframe(comparison_data, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

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
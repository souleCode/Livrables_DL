import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# Configuration de la page
st.set_page_config(
    page_title="Historique des Expériences - FrameML",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation de la session state
if 'selected_experiments' not in st.session_state:
    st.session_state.selected_experiments = []
if 'comparison_mode' not in st.session_state:
    st.session_state.comparison_mode = False

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
    
    /* Stats card */
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
        border-top: 4px solid;
    }
    
    .stats-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .stats-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Experiment card */
    .experiment-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-left: 4px solid;
        transition: all 0.3s;
        cursor: pointer;
    }
    
    .experiment-card:hover {
        box-shadow: 0 4px 12px rgba(102,126,234,0.2);
        transform: translateX(5px);
    }
    
    .experiment-card.selected {
        border-left-width: 6px;
        background: linear-gradient(135deg, rgba(102,126,234,0.05) 0%, rgba(118,75,162,0.05) 100%);
    }
    
    .experiment-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .experiment-meta {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    .experiment-metrics {
        display: flex;
        gap: 1.5rem;
        margin-top: 1rem;
    }
    
    .experiment-metric {
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.3rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #666;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    
    .badge-success {
        background: #d1fae5;
        color: #065f46;
    }
    
    .badge-warning {
        background: #fef3c7;
        color: #92400e;
    }
    
    .badge-info {
        background: #dbeafe;
        color: #1e40af;
    }
    
    .badge-purple {
        background: #e0e7ff;
        color: #3730a3;
    }
    
    /* Comparison section */
    .comparison-section {
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
        border-bottom: 3px solid #667eea;
    }
    
    /* Filter section */
    .filter-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    
    /* Timeline */
    .timeline-item {
        position: relative;
        padding-left: 2rem;
        padding-bottom: 1.5rem;
        border-left: 2px solid #e5e7eb;
    }
    
    .timeline-item:last-child {
        border-left: none;
    }
    
    .timeline-dot {
        position: absolute;
        left: -6px;
        top: 0;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #667eea;
    }
    
    .timeline-content {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
    }
    
    /* Config display */
    .config-item {
        background: #f8f9fa;
        padding: 0.8rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .config-label {
        font-weight: 600;
        color: #666;
    }
    
    .config-value {
        color: #333;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Données simulées des expériences
experiments_data = [
    {
        'id': 1,
        'name': 'Exp-001: Random Forest Optimisé',
        'model': 'Random Forest',
        'date': datetime.now() - timedelta(days=1),
        'accuracy': 92.6,
        'precision': 91.8,
        'recall': 90.8,
        'f1_score': 0.913,
        'training_time': 15,
        'status': 'completed',
        'config': {
            'n_estimators': 100,
            'max_depth': 10,
            'train_test_split': 0.8,
            'cv_folds': 5
        }
    },
    {
        'id': 2,
        'name': 'Exp-002: XGBoost avec Feature Engineering',
        'model': 'XGBoost',
        'date': datetime.now() - timedelta(days=3),
        'accuracy': 94.2,
        'precision': 93.5,
        'recall': 92.1,
        'f1_score': 0.928,
        'training_time': 28,
        'status': 'completed',
        'config': {
            'n_estimators': 200,
            'learning_rate': 0.1,
            'train_test_split': 0.8,
            'cv_folds': 5
        }
    },
    {
        'id': 3,
        'name': 'Exp-003: CNN Architecture Simple',
        'model': 'CNN',
        'date': datetime.now() - timedelta(days=5),
        'accuracy': 89.5,
        'precision': 88.2,
        'recall': 87.9,
        'f1_score': 0.881,
        'training_time': 120,
        'status': 'completed',
        'config': {
            'layers': 3,
            'filters': 32,
            'epochs': 50,
            'batch_size': 64
        }
    },
    {
        'id': 4,
        'name': 'Exp-004: Random Forest Baseline',
        'model': 'Random Forest',
        'date': datetime.now() - timedelta(days=7),
        'accuracy': 87.4,
        'precision': 86.1,
        'recall': 85.3,
        'f1_score': 0.857,
        'training_time': 10,
        'status': 'completed',
        'config': {
            'n_estimators': 50,
            'max_depth': 5,
            'train_test_split': 0.8,
            'cv_folds': 3
        }
    },
    {
        'id': 5,
        'name': 'Exp-005: SVM avec RBF Kernel',
        'model': 'SVM',
        'date': datetime.now() - timedelta(days=10),
        'accuracy': 85.7,
        'precision': 84.9,
        'recall': 83.5,
        'f1_score': 0.842,
        'training_time': 8,
        'status': 'completed',
        'config': {
            'kernel': 'rbf',
            'C': 1.0,
            'gamma': 'scale',
            'train_test_split': 0.8
        }
    },
    {
        'id': 6,
        'name': 'Exp-006: LSTM Séries Temporelles',
        'model': 'LSTM',
        'date': datetime.now() - timedelta(days=12),
        'accuracy': 88.3,
        'precision': 87.1,
        'recall': 86.8,
        'f1_score': 0.869,
        'training_time': 95,
        'status': 'completed',
        'config': {
            'units': 128,
            'layers': 2,
            'epochs': 100,
            'batch_size': 32
        }
    },
    {
        'id': 7,
        'name': 'Exp-007: Ensemble Methods Test',
        'model': 'Ensemble',
        'date': datetime.now() - timedelta(days=15),
        'accuracy': 91.2,
        'precision': 90.3,
        'recall': 89.7,
        'f1_score': 0.900,
        'training_time': 45,
        'status': 'completed',
        'config': {
            'models': ['RF', 'XGB', 'SVM'],
            'voting': 'soft',
            'train_test_split': 0.8
        }
    },
    {
        'id': 8,
        'name': 'Exp-008: XGBoost Hyperparameter Tuning',
        'model': 'XGBoost',
        'date': datetime.now() - timedelta(days=18),
        'accuracy': 93.1,
        'precision': 92.4,
        'recall': 91.5,
        'f1_score': 0.919,
        'training_time': 65,
        'status': 'completed',
        'config': {
            'n_estimators': 300,
            'learning_rate': 0.05,
            'max_depth': 8,
            'train_test_split': 0.8
        }
    }
]

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 FrameML")
    st.markdown("---")
    
    st.markdown("#### 📊 Statistiques")
    st.info(f"**Total Expériences:** {len(experiments_data)}")
    st.info(f"**Complétées:** {sum(1 for e in experiments_data if e['status'] == 'completed')}")
    best_acc = max(e['accuracy'] for e in experiments_data)
    st.info(f"**Meilleure Accuracy:** {best_acc}%")
    
    st.markdown("---")
    
    st.markdown("#### 📍 Navigation")
    if st.button("⬅️ Retour au Dashboard", use_container_width=True):
        st.info("Retour au dashboard...")
    if st.button("➕ Nouvelle Expérience", use_container_width=True, type="primary"):
        st.info("Création d'une nouvelle expérience...")
    
    st.markdown("---")
    
    st.markdown("#### 🔄 Actions Rapides")
    if st.button("📊 Exporter CSV", use_container_width=True):
        st.success("📊 Export CSV en cours...")
    if st.button("📈 Rapport PDF", use_container_width=True):
        st.success("📈 Génération du rapport...")
    if st.button("🗑️ Nettoyer Anciennes", use_container_width=True):
        st.warning("🗑️ Nettoyage...")

# Header
st.markdown("""
<div class="page-header">
    <h1>📚 Historique des Expériences</h1>
    <p>Suivez, comparez et réutilisez vos expériences de machine learning</p>
</div>
""", unsafe_allow_html=True)

# Statistiques rapides
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stats-card" style="border-top-color: #667eea;">
        <div class="stats-label">Total Expériences</div>
        <div class="stats-value" style="color: #667eea;">{len(experiments_data)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_accuracy = sum(e['accuracy'] for e in experiments_data) / len(experiments_data)
    st.markdown(f"""
    <div class="stats-card" style="border-top-color: #10b981;">
        <div class="stats-label">Accuracy Moyenne</div>
        <div class="stats-value" style="color: #10b981;">{avg_accuracy:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    best_exp = max(experiments_data, key=lambda x: x['accuracy'])
    st.markdown(f"""
    <div class="stats-card" style="border-top-color: #f59e0b;">
        <div class="stats-label">Meilleur Score</div>
        <div class="stats-value" style="color: #f59e0b;">{best_exp['accuracy']}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_time = sum(e['training_time'] for e in experiments_data)
    st.markdown(f"""
    <div class="stats-card" style="border-top-color: #ef4444;">
        <div class="stats-label">Temps Total</div>
        <div class="stats-value" style="color: #ef4444;">{total_time}min</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Filtres et recherche
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
col_search, col_filter1, col_filter2, col_filter3, col_filter4 = st.columns([2, 1, 1, 1, 1])

with col_search:
    search_query = st.text_input("🔍 Rechercher une expérience", placeholder="Nom, modèle...")

with col_filter1:
    model_filter = st.selectbox("Modèle", ["Tous"] + list(set(e['model'] for e in experiments_data)))

with col_filter2:
    date_range = st.selectbox("Période", ["Tout", "7 derniers jours", "30 derniers jours", "90 derniers jours"])

with col_filter3:
    perf_filter = st.selectbox("Performance", ["Toutes", ">90%", ">85%", "<85%"])

with col_filter4:
    sort_by = st.selectbox("Trier par", ["Date (récent)", "Date (ancien)", "Accuracy", "Temps"])

st.markdown('</div>', unsafe_allow_html=True)

# Mode comparaison
col_mode1, col_mode2 = st.columns([6, 1])
with col_mode2:
    if st.button("🔄 Mode Comparaison", use_container_width=True):
        st.session_state.comparison_mode = not st.session_state.comparison_mode
        if not st.session_state.comparison_mode:
            st.session_state.selected_experiments = []
        st.rerun()

if st.session_state.comparison_mode:
    st.info("📊 **Mode Comparaison Activé** - Sélectionnez jusqu'à 4 expériences à comparer")

st.markdown("<br>", unsafe_allow_html=True)

# Liste des expériences
for exp in experiments_data:
    # Filtres
    if model_filter != "Tous" and exp['model'] != model_filter:
        continue
    
    if perf_filter != "Toutes":
        if perf_filter == ">90%" and exp['accuracy'] <= 90:
            continue
        elif perf_filter == ">85%" and exp['accuracy'] <= 85:
            continue
        elif perf_filter == "<85%" and exp['accuracy'] >= 85:
            continue
    
    # Déterminer la couleur selon la performance
    if exp['accuracy'] >= 90:
        border_color = "#10b981"
        badge_class = "badge-success"
        perf_text = "🏆 Excellent"
    elif exp['accuracy'] >= 85:
        border_color = "#3b82f6"
        badge_class = "badge-info"
        perf_text = "✅ Bon"
    else:
        border_color = "#f59e0b"
        badge_class = "badge-warning"
        perf_text = "⚠️ Moyen"
    
    is_selected = exp['id'] in st.session_state.selected_experiments
    selected_class = "selected" if is_selected else ""
    
    st.markdown(f"""
    <div class="experiment-card {selected_class}" style="border-left-color: {border_color};">
        <div class="experiment-title">{exp['name']}</div>
        <div class="experiment-meta">
            🤖 {exp['model']} • 📅 {exp['date'].strftime('%d/%m/%Y %H:%M')} • ⏱️ {exp['training_time']} min
        </div>
        
        <div>
            <span class="badge {badge_class}">{perf_text}</span>
            <span class="badge badge-info">Accuracy: {exp['accuracy']}%</span>
            <span class="badge badge-purple">F1: {exp['f1_score']:.3f}</span>
        </div>
        
        <div class="experiment-metrics">
            <div class="experiment-metric">
                <div class="metric-value">{exp['accuracy']}%</div>
                <div class="metric-label">Accuracy</div>
            </div>
            <div class="experiment-metric">
                <div class="metric-value">{exp['precision']}%</div>
                <div class="metric-label">Precision</div>
            </div>
            <div class="experiment-metric">
                <div class="metric-value">{exp['recall']}%</div>
                <div class="metric-label">Recall</div>
            </div>
            <div class="experiment-metric">
                <div class="metric-value">{exp['f1_score']:.3f}</div>
                <div class="metric-label">F1-Score</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Boutons d'action
    if st.session_state.comparison_mode:
        col_comp, col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1, 1])
        
        with col_comp:
            if is_selected:
                if st.button("✓ Sélectionné", key=f"sel_{exp['id']}", use_container_width=True, type="secondary"):
                    st.session_state.selected_experiments.remove(exp['id'])
                    st.rerun()
            else:
                if len(st.session_state.selected_experiments) < 4:
                    if st.button("☐ Sélectionner", key=f"sel_{exp['id']}", use_container_width=True):
                        st.session_state.selected_experiments.append(exp['id'])
                        st.rerun()
                else:
                    st.button("☐ Max atteint", key=f"sel_{exp['id']}", use_container_width=True, disabled=True)
        
        with col_btn1:
            if st.button("👁️ Détails", key=f"view_{exp['id']}", use_container_width=True):
                st.info(f"Détails de {exp['name']}")
        
        with col_btn2:
            if st.button("📋 Dupliquer Config", key=f"dup_{exp['id']}", use_container_width=True):
                st.success(f"✅ Configuration dupliquée!")
        
        with col_btn3:
            if st.button("🗑️ Supprimer", key=f"del_{exp['id']}", use_container_width=True):
                st.error(f"🗑️ Suppression de {exp['name']}")
    else:
        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
        
        with col_btn1:
            if st.button("👁️ Voir Détails", key=f"view_{exp['id']}", use_container_width=True):
                st.info(f"Détails de {exp['name']}")
        
        with col_btn2:
            if st.button("📋 Réutiliser Config", key=f"reuse_{exp['id']}", use_container_width=True):
                st.success(f"✅ Configuration réutilisée!")
        
        with col_btn3:
            if st.button("📥 Télécharger", key=f"download_{exp['id']}", use_container_width=True):
                st.success(f"📥 Téléchargement en cours...")
        
        with col_btn4:
            if st.button("🗑️ Supprimer", key=f"delete_{exp['id']}", use_container_width=True):
                st.error(f"🗑️ Suppression...")
    
    st.markdown("<br>", unsafe_allow_html=True)

# Section Comparaison
if st.session_state.comparison_mode and len(st.session_state.selected_experiments) > 1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="comparison-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Comparaison des Expériences Sélectionnées</div>', unsafe_allow_html=True)
    
    # Filtrer les expériences sélectionnées
    selected_exps = [e for e in experiments_data if e['id'] in st.session_state.selected_experiments]
    
    # Tableau de comparaison
    comparison_df = pd.DataFrame({
        'Expérience': [e['name'] for e in selected_exps],
        'Modèle': [e['model'] for e in selected_exps],
        'Accuracy (%)': [e['accuracy'] for e in selected_exps],
        'Precision (%)': [e['precision'] for e in selected_exps],
        'Recall (%)': [e['recall'] for e in selected_exps],
        'F1-Score': [e['f1_score'] for e in selected_exps],
        'Temps (min)': [e['training_time'] for e in selected_exps],
        'Date': [e['date'].strftime('%d/%m/%Y') for e in selected_exps]
    })
    
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graphiques de comparaison
    col_comp1, col_comp2 = st.columns(2)
    
    with col_comp1:
        # Radar chart des métriques
        fig_radar = go.Figure()
        
        for exp in selected_exps:
            fig_radar.add_trace(go.Scatterpolar(
                r=[exp['accuracy'], exp['precision'], exp['recall'], exp['f1_score']*100],
                theta=['Accuracy', 'Precision', 'Recall', 'F1-Score'],
                fill='toself',
                name=exp['name'][:20] + '...'
            ))
        
        fig_radar.update_layout(
            height=400,
            polar=dict(radialaxis=dict(visible=True, range=[75, 100])),
            margin=dict(l=80, r=80, t=40, b=40),
            title="Comparaison des Métriques"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col_comp2:
        # Barres comparatives
        metrics_comp = pd.DataFrame({
            'Expérience': [e['name'][:15] + '...' for e in selected_exps],
            'Accuracy': [e['accuracy'] for e in selected_exps],
            'F1-Score': [e['f1_score']*100 for e in selected_exps]
        })
        
        fig_bars = go.Figure()
        
        fig_bars.add_trace(go.Bar(
            name='Accuracy',
            x=metrics_comp['Expérience'],
            y=metrics_comp['Accuracy'],
            marker_color='#667eea'
        ))
        
        fig_bars.add_trace(go.Bar(
            name='F1-Score',
            x=metrics_comp['Expérience'],
            y=metrics_comp['F1-Score'],
            marker_color='#764ba2'
        ))
        
        fig_bars.update_layout(
            height=400,
            barmode='group',
            title="Accuracy vs F1-Score",
            yaxis=dict(range=[75, 100]),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        st.plotly_chart(fig_bars, use_container_width=True)
    
    # Configurations côte à côte
    st.markdown("#### ⚙️ Configurations")
    cols_config = st.columns(len(selected_exps))
    
    for idx, (col, exp) in enumerate(zip(cols_config, selected_exps)):
        with col:
            st.markdown(f"**{exp['name'][:20]}...**")
            for key, value in exp['config'].items():
                st.markdown(f"""
                <div class="config-item">
                    <span class="config-label">{key}</span>
                    <span class="config-value">{value}</span>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Timeline des expériences
if not st.session_state.comparison_mode:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="comparison-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📅 Timeline des Expériences</div>', unsafe_allow_html=True)
    
    # Graphique temporel
    sorted_exps = sorted(experiments_data, key=lambda x: x['date'])
    
    fig_timeline = go.Figure()
    
    fig_timeline.add_trace(go.Scatter(
        x=[e['date'] for e in sorted_exps],
        y=[e['accuracy'] for e in sorted_exps],
        mode='lines+markers',
        name='Accuracy',
        line=dict(color='#667eea', width=3),
        marker=dict(size=12, color='#667eea', line=dict(width=2, color='white')),
        text=[e['name'] for e in sorted_exps],
        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Accuracy: %{y:.1f}%<extra></extra>'
    ))
    
    fig_timeline.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Date', showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
        yaxis=dict(title='Accuracy (%)', showgrid=True, gridcolor='rgba(0,0,0,0.05)', range=[75, 100]),
        hovermode='closest'
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analyse des tendances
    st.markdown('<div class="comparison-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Analyse des Tendances</div>', unsafe_allow_html=True)
    
    col_trend1, col_trend2 = st.columns(2)
    
    with col_trend1:
        # Performance par modèle
        model_perf = {}
        for exp in experiments_data:
            if exp['model'] not in model_perf:
                model_perf[exp['model']] = []
            model_perf[exp['model']].append(exp['accuracy'])
        
        model_avg = {model: sum(accs)/len(accs) for model, accs in model_perf.items()}
        
        fig_model_perf = px.bar(
            x=list(model_avg.keys()),
            y=list(model_avg.values()),
            labels={'x': 'Modèle', 'y': 'Accuracy Moyenne (%)'},
            title='Performance Moyenne par Type de Modèle',
            color=list(model_avg.values()),
            color_continuous_scale='Purples'
        )
        
        fig_model_perf.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=40, b=0),
            showlegend=False
        )
        
        st.plotly_chart(fig_model_perf, use_container_width=True)
        
        # Insights
        best_model = max(model_avg, key=model_avg.get)
        st.success(f"✅ **Meilleur Modèle en Moyenne:** {best_model} ({model_avg[best_model]:.1f}%)")
    
    with col_trend2:
        # Distribution des temps d'entraînement
        fig_time_dist = px.box(
            y=[e['training_time'] for e in experiments_data],
            x=[e['model'] for e in experiments_data],
            labels={'x': 'Modèle', 'y': 'Temps d\'entraînement (min)'},
            title='Distribution des Temps d\'Entraînement',
            color=[e['model'] for e in experiments_data],
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        fig_time_dist.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=40, b=0),
            showlegend=False
        )
        
        st.plotly_chart(fig_time_dist, use_container_width=True)
        
        # Insights
        avg_time = sum(e['training_time'] for e in experiments_data) / len(experiments_data)
        st.info(f"⏱️ **Temps Moyen d'Entraînement:** {avg_time:.1f} minutes")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Corrélations
    st.markdown('<div class="comparison-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔗 Corrélations et Insights</div>', unsafe_allow_html=True)
    
    col_corr1, col_corr2 = st.columns(2)
    
    with col_corr1:
        # Scatter: Temps vs Performance
        fig_scatter = px.scatter(
            x=[e['training_time'] for e in experiments_data],
            y=[e['accuracy'] for e in experiments_data],
            size=[e['accuracy'] for e in experiments_data],
            color=[e['model'] for e in experiments_data],
            labels={'x': 'Temps d\'entraînement (min)', 'y': 'Accuracy (%)'},
            title='Temps d\'Entraînement vs Performance',
            hover_data={'Expérience': [e['name'] for e in experiments_data]}
        )
        
        fig_scatter.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.markdown("""
        **💡 Observation:** Les modèles Deep Learning (CNN, LSTM) nécessitent plus de temps 
        d'entraînement mais n'offrent pas toujours les meilleures performances sur ce type de données.
        """)
    
    with col_corr2:
        # Heatmap des corrélations entre métriques
        import numpy as np
        
        metrics_matrix = np.array([
            [e['accuracy'] for e in experiments_data],
            [e['precision'] for e in experiments_data],
            [e['recall'] for e in experiments_data],
            [e['f1_score']*100 for e in experiments_data]
        ])
        
        correlation_matrix = np.corrcoef(metrics_matrix)
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=correlation_matrix,
            x=['Accuracy', 'Precision', 'Recall', 'F1-Score'],
            y=['Accuracy', 'Precision', 'Recall', 'F1-Score'],
            colorscale='Purples',
            text=np.round(correlation_matrix, 2),
            texttemplate='%{text}',
            textfont={"size": 14},
            showscale=True
        ))
        
        fig_heatmap.update_layout(
            title='Matrice de Corrélation des Métriques',
            height=350,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.markdown("""
        **💡 Observation:** Forte corrélation entre toutes les métriques, 
        indiquant une cohérence des performances à travers les différentes mesures.
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recommandations basées sur l'historique
    st.markdown('<div class="comparison-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 Recommandations Basées sur l\'Historique</div>', unsafe_allow_html=True)
    
    col_rec1, col_rec2, col_rec3 = st.columns(3)
    
    with col_rec1:
        st.markdown("#### 🏆 Configuration Gagnante")
        best_exp = max(experiments_data, key=lambda x: x['accuracy'])
        st.markdown(f"""
        **{best_exp['name']}**
        - Modèle: {best_exp['model']}
        - Accuracy: {best_exp['accuracy']}%
        - Temps: {best_exp['training_time']} min
        """)
        if st.button("🔄 Réutiliser cette Config", key="reuse_best", use_container_width=True, type="primary"):
            st.success("✅ Configuration chargée!")
    
    with col_rec2:
        st.markdown("#### ⚡ Meilleur Rapport Perf/Temps")
        efficiency = {e['id']: e['accuracy'] / e['training_time'] for e in experiments_data}
        best_efficient_id = max(efficiency, key=efficiency.get)
        best_efficient = next(e for e in experiments_data if e['id'] == best_efficient_id)
        st.markdown(f"""
        **{best_efficient['name']}**
        - Modèle: {best_efficient['model']}
        - Accuracy: {best_efficient['accuracy']}%
        - Temps: {best_efficient['training_time']} min
        """)
        if st.button("🔄 Réutiliser cette Config", key="reuse_efficient", use_container_width=True, type="primary"):
            st.success("✅ Configuration chargée!")
    
    with col_rec3:
        st.markdown("#### 📈 Tendance Recommandée")
        # Calculer la tendance
        recent_exps = sorted(experiments_data, key=lambda x: x['date'], reverse=True)[:3]
        avg_recent = sum(e['accuracy'] for e in recent_exps) / len(recent_exps)
        
        st.markdown(f"""
        **Tendance Récente**
        - Accuracy moyenne: {avg_recent:.1f}%
        - Modèles testés: {len(set(e['model'] for e in recent_exps))}
        - Amélioration: +{avg_recent - avg_accuracy:.1f}%
        """)
        st.info("💡 Continuez avec XGBoost et optimisation des hyperparamètres")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Export et actions globales
    st.markdown('<div class="comparison-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📥 Export et Actions</div>', unsafe_allow_html=True)
    
    col_export1, col_export2, col_export3, col_export4 = st.columns(4)
    
    with col_export1:
        if st.button("📊 Exporter Tout en CSV", use_container_width=True, type="primary"):
            st.success("📊 Export CSV complet en cours...")
    
    with col_export2:
        if st.button("📈 Générer Rapport PDF", use_container_width=True):
            st.success("📈 Génération du rapport détaillé...")
    
    with col_export3:
        if st.button("📧 Envoyer par Email", use_container_width=True):
            st.info("📧 Configuration de l'envoi...")
    
    with col_export4:
        if st.button("🗑️ Nettoyer Anciennes Exp", use_container_width=True):
            st.warning("🗑️ Suppression des expériences >90 jours...")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistiques avancées
    st.markdown('<div class="comparison-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Statistiques Avancées</div>', unsafe_allow_html=True)
    
    stats_data = pd.DataFrame({
        'Métrique': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
        'Moyenne': [
            f"{sum(e['accuracy'] for e in experiments_data) / len(experiments_data):.2f}%",
            f"{sum(e['precision'] for e in experiments_data) / len(experiments_data):.2f}%",
            f"{sum(e['recall'] for e in experiments_data) / len(experiments_data):.2f}%",
            f"{sum(e['f1_score'] for e in experiments_data) / len(experiments_data):.3f}"
        ],
        'Min': [
            f"{min(e['accuracy'] for e in experiments_data):.2f}%",
            f"{min(e['precision'] for e in experiments_data):.2f}%",
            f"{min(e['recall'] for e in experiments_data):.2f}%",
            f"{min(e['f1_score'] for e in experiments_data):.3f}"
        ],
        'Max': [
            f"{max(e['accuracy'] for e in experiments_data):.2f}%",
            f"{max(e['precision'] for e in experiments_data):.2f}%",
            f"{max(e['recall'] for e in experiments_data):.2f}%",
            f"{max(e['f1_score'] for e in experiments_data):.3f}"
        ],
        'Écart-type': [
            f"{np.std([e['accuracy'] for e in experiments_data]):.2f}%",
            f"{np.std([e['precision'] for e in experiments_data]):.2f}%",
            f"{np.std([e['recall'] for e in experiments_data]):.2f}%",
            f"{np.std([e['f1_score'] for e in experiments_data]):.3f}"
        ]
    })
    
    st.dataframe(stats_data, use_container_width=True, hide_index=True)
    
    st.markdown('</div>', unsafe_allow_html=True)



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
print_session_state()
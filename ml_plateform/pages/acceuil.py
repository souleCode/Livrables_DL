import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="FrameML - Plateforme ML/Deep Learning",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour un design moderne
st.markdown("""
<style>
    /* Styles généraux */
    .main {
        padding: 0rem 0rem;
    }
    
    /* Header */
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 3rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .logo {
        font-size: 2rem;
        font-weight: bold;
        color: white;
    }
    
    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 6rem 3rem;
        text-align: center;
        color: white;
    }
    
    .hero h1 {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        line-height: 1.2;
    }
    
    .hero p {
        font-size: 1.3rem;
        margin-bottom: 2rem;
        opacity: 0.95;
    }
    
    /* Bouton CTA */
    .cta-button {
        background: white;
        color: #667eea;
        padding: 1rem 3rem;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 50px;
        border: none;
        cursor: pointer;
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        transition: all 0.3s;
        display: inline-block;
        text-decoration: none;
    }
    
    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.3);
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s;
        height: 100%;
        border: 1px solid #f0f0f0;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(102,126,234,0.2);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: #666;
        line-height: 1.6;
        font-size: 1.1rem;
    }
    
    /* Testimonials */
    .testimonial {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .testimonial-text {
        font-style: italic;
        color: #333;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }
    
    .testimonial-author {
        font-weight: bold;
        color: #667eea;
    }
    
    /* Footer */
    .footer {
        background: #2d3748;
        color: white;
        padding: 3rem;
        text-align: center;
        margin-top: 4rem;
    }
    
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 1rem;
    }
    
    .footer-link {
        color: white;
        text-decoration: none;
        opacity: 0.8;
        transition: opacity 0.3s;
    }
    
    .footer-link:hover {
        opacity: 1;
    }
    
    /* Section spacing */
    .section {
        padding: 4rem 3rem;
    }
    
    .section-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 3rem;
    }
    
    /* Stats */
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 3rem 0;
        text-align: center;
    }
    
    .stat-item {
        padding: 1.5rem;
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 1.2rem;
        color: #666;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <div class="logo">🤖 FrameML</div>
    <div style="display: flex; gap: 2rem; align-items: center;">
        <a href="#fonctionnalites" style="color: white; text-decoration: none;">Fonctionnalités</a>
        <a href="#temoignages" style="color: white; text-decoration: none;">Témoignages</a>
        <a href="#contact" style="color: white; text-decoration: none;">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1>🚀 Créez vos modèles ML en quelques clics</h1>
    <p>La plateforme tout-en-un pour entraîner, évaluer et déployer vos modèles de Machine Learning et Deep Learning sans écrire une ligne de code</p>
</div>
""", unsafe_allow_html=True)

# Bouton CTA centré
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🎯 Commencer Maintenant", use_container_width=True, type="primary"):
        st.switch_page("pages/connexion.py")

# Statistiques
st.markdown("""
<div class="stats-container">
    <div class="stat-item">
        <div class="stat-number">10K+</div>
        <div class="stat-label">Utilisateurs Actifs</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">50K+</div>
        <div class="stat-label">Modèles Entraînés</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">99.9%</div>
        <div class="stat-label">Disponibilité</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Section Fonctionnalités
st.markdown('<div class="section-title" id="fonctionnalites">✨ Fonctionnalités Principales</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Upload Simplifié</div>
        <div class="feature-description">
            Importez vos données en CSV, Excel ou JSON par simple glisser-déposer. 
            Visualisation instantanée et prétraitement automatique.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <div class="feature-title">Modèles Puissants</div>
        <div class="feature-description">
            Accédez à une bibliothèque complète : Random Forest, XGBoost, CNN, RNN, 
            Transformers et bien plus encore.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">Monitoring en Temps Réel</div>
        <div class="feature-description">
            Suivez l'entraînement en direct avec des graphiques interactifs, 
            métriques et logs détaillés.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Évaluation Avancée</div>
        <div class="feature-description">
            Analysez les performances avec des métriques détaillées, matrices de confusion, 
            courbes ROC et importance des features.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🚀</div>
        <div class="feature-title">Déploiement Rapide</div>
        <div class="feature-description">
            Déployez vos modèles en API REST en un clic. Téléchargez en 
            pickle, h5, ONNX ou autres formats.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📚</div>
        <div class="feature-title">Historique Complet</div>
        <div class="feature-description">
            Gardez une trace de toutes vos expériences, comparez les résultats 
            et réutilisez les configurations gagnantes.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Section Témoignages
st.markdown('<br><br><div class="section-title" id="temoignages">💬 Ce que disent nos utilisateurs</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="testimonial">
        <div class="testimonial-text">
            "FrameML a transformé notre workflow ML. Ce qui prenait des jours prend maintenant quelques heures !"
        </div>
        <div class="testimonial-author">⭐⭐⭐⭐⭐ - Sarah M., Data Scientist</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="testimonial">
        <div class="testimonial-text">
            "Interface intuitive et résultats professionnels. Parfait pour prototyper rapidement nos modèles."
        </div>
        <div class="testimonial-author">⭐⭐⭐⭐⭐ - Ahmed K., ML Engineer</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="testimonial">
        <div class="testimonial-text">
            "Le monitoring en temps réel et les visualisations sont exceptionnels. Un must-have pour tout data scientist !"
        </div>
        <div class="testimonial-author">⭐⭐⭐⭐⭐ - Marie L., Researcher</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer" id="contact">
    <h3>🤖 FrameML</h3>
    <p>La plateforme intelligente pour vos projets Machine Learning</p>
    <div class="footer-links">
        <a href="#" class="footer-link">Documentation</a>
        <a href="#" class="footer-link">API</a>
        <a href="#" class="footer-link">Support</a>
        <a href="#" class="footer-link">Blog</a>
    </div>
    <p style="opacity: 0.7; margin-top: 2rem;">© 2024 FrameML. Tous droits réservés.</p>
    <p style="opacity: 0.7;">📧 contact@frameml.com | 📞 +212 XXX XXX XXX</p>
</div>
""", unsafe_allow_html=True)
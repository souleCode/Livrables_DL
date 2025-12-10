import streamlit as st
import pandas as pd
from typing import Dict, Any
import time

def show_loading(message: str = "Chargement..."):
    """Afficher un indicateur de chargement"""
    return st.spinner(message)

def show_success(message: str):
    """Afficher un message de succès"""
    st.success(message)

def show_error(message: str):
    """Afficher un message d'erreur"""
    st.error(message)

def show_warning(message: str):
    """Afficher un message d'avertissement"""
    st.warning(message)

def format_metrics(metrics: Dict[str, Any]) -> str:
    """Formatter les métriques pour l'affichage"""
    if not metrics:
        return "Aucune métrique disponible"
    
    formatted = []
    for key, value in metrics.items():
        if isinstance(value, float):
            formatted.append(f"{key}: {value:.4f}")
        else:
            formatted.append(f"{key}: {value}")
    
    return " | ".join(formatted)

def simulate_progress(duration: int = 5):
    """Simuler une barre de progression (pour les démos)"""
    progress_bar = st.progress(0)
    
    for i in range(100):
        time.sleep(duration / 100)
        progress_bar.progress(i + 1)
    
    progress_bar.empty()
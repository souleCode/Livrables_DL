import requests
import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional
import io

class MLAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Faire une requête à l'API avec gestion d'erreurs"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur API: {str(e)}")
            raise
    
    def health_check(self) -> bool:
        """Vérifier que l'API est en ligne"""
        try:
            response = self._make_request("GET", "/api/health")
            return response.get("status") == "healthy"
        except:
            return False

    # ==================== PROJETS ====================
    
    def create_project(self, name: str, description: str, problem_type: str, task_type: str) -> str:
        """Créer un nouveau projet"""
        data = {
            "name": name,
            "description": description,
            "problem_type": problem_type,
            "task_type": task_type
        }
        response = self._make_request("POST", "/api/projects/create", json=data)
        return response["project_id"]
    
    def list_projects(self) -> List[Dict]:
        """Lister tous les projets"""
        response = self._make_request("GET", "/api/projects/list")
        return response["projects"]
    
    def get_project(self, project_id: str) -> Dict:
        """Obtenir les détails d'un projet"""
        response = self._make_request("GET", f"/api/projects/{project_id}")
        return response["project"]

    # ==================== DONNÉES ====================
    
    def upload_data(self, project_id: str, file: st.runtime.uploaded_file_manager.UploadedFile) -> Dict:
        """Uploader un fichier de données"""
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = self._make_request("POST", f"/api/data/upload?project_id={project_id}", files=files)
        return response
    
    def configure_data(self, project_id: str, target_column: str, **config) -> Dict:
        """Configurer le preprocessing des données"""
        data = {
            "project_id": project_id,
            "target_column": target_column,
            **config
        }
        response = self._make_request("POST", "/api/data/configure", json=data)
        return response

    # ==================== ENTRAÎNEMENT ====================
    
    def start_training(self, project_id: str, model_type: str, hyperparameters: Dict, **config) -> Dict:
        """Démarrer l'entraînement d'un modèle"""
        data = {
            "project_id": project_id,
            "model_type": model_type,
            "hyperparameters": hyperparameters,
            **config
        }
        response = self._make_request("POST", "/api/train/start", json=data)
        return response
    
    def get_training_status(self, experiment_id: str) -> Dict:
        """Obtenir le statut d'un entraînement"""
        response = self._make_request("GET", f"/api/train/status/{experiment_id}")
        return response["experiment"]

    # ==================== MODÈLES ====================
    
    def list_models(self) -> List[Dict]:
        """Lister tous les modèles"""
        response = self._make_request("GET", "/api/models/list")
        return response["models"]
    
    def get_model(self, model_id: str) -> Dict:
        """Obtenir les détails d'un modèle"""
        response = self._make_request("GET", f"/api/models/{model_id}")
        return response["model"]
    
    def download_model(self, model_id: str, format: str = "pkl") -> bytes:
        """Télécharger un modèle"""
        url = f"{self.base_url}/api/models/download/{model_id}?format={format}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.content
    
    def delete_model(self, model_id: str) -> Dict:
        """Supprimer un modèle"""
        response = self._make_request("DELETE", f"/api/models/{model_id}")
        return response

    # ==================== PRÉDICTIONS ====================
    
    def make_prediction(self, model_id: str, features: List[float]) -> Dict:
        """Faire une prédiction avec un modèle"""
        data = {
            "model_id": model_id,
            "features": features
        }
        response = self._make_request("POST", "/api/predict", json=data)
        return response

    # ==================== EXPÉRIENCES ====================
    
    def list_experiments(self) -> List[Dict]:
        """Lister toutes les expériences"""
        response = self._make_request("GET", "/api/experiments/list")
        return response["experiments"]
    
    def get_experiment(self, experiment_id: str) -> Dict:
        """Obtenir les détails d'une expérience"""
        response = self._make_request("GET", f"/api/experiments/{experiment_id}")
        return response["experiment"]
    
    def get_project_experiments(self, project_id: str) -> List[Dict]:
        """Obtenir toutes les expériences d'un projet"""
        response = self._make_request("GET", f"/api/experiments/project/{project_id}")
        return response["experiments"]

# Instance globale du client
api_client = MLAPIClient()

def init_api_client(base_url: str = None):
    """Initialiser le client API avec une URL personnalisée"""
    global api_client
    if base_url:
        api_client = MLAPIClient(base_url)
    return api_client
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
import pickle
import json
import os
from datetime import datetime
import uuid
import io
import uvicorn
# Imports ML
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from sklearn.svm import SVC, SVR
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, mean_squared_error, r2_score
)
import xgboost as xgb

# Configuration
app = FastAPI(
    title="FrameML API",
    description="API Backend pour la plateforme ML/Deep Learning",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dossiers de stockage
UPLOAD_DIR = "data/uploads"
MODELS_DIR = "data/models"
RESULTS_DIR = "data/results"

for directory in [UPLOAD_DIR, MODELS_DIR, RESULTS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Stockage en mémoire (à remplacer par une vraie DB en production)
projects_db = {}
experiments_db = {}
models_db = {}

# ==================== MODÈLES PYDANTIC ====================

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    problem_type: str  # "ML Classique" ou "Deep Learning"
    task_type: str  # "Classification" ou "Régression"

class DataConfig(BaseModel):
    project_id: str
    target_column: str
    handle_missing: bool = True
    missing_strategy: str = "mean"
    normalize: bool = True
    normalize_method: str = "StandardScaler"

class ModelConfig(BaseModel):
    project_id: str
    model_type: str
    hyperparameters: Dict[str, Any]
    train_test_split: float = 0.8
    cv_folds: int = 5
    use_cross_validation: bool = True

class PredictionRequest(BaseModel):
    model_id: str
    features: List[float]

# ==================== ENDPOINTS PROJETS ====================

@app.post("/api/projects/create")
async def create_project(project: ProjectCreate):
    """Créer un nouveau projet ML"""
    project_id = str(uuid.uuid4())
    
    projects_db[project_id] = {
        "id": project_id,
        "name": project.name,
        "description": project.description,
        "problem_type": project.problem_type,
        "task_type": project.task_type,
        "created_at": datetime.now().isoformat(),
        "status": "created",
        "data_uploaded": False
    }
    
    return {
        "status": "success",
        "project_id": project_id,
        "message": "Projet créé avec succès"
    }

@app.get("/api/projects/list")
async def list_projects():
    """Lister tous les projets"""
    return {
        "status": "success",
        "projects": list(projects_db.values())
    }

@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    """Obtenir les détails d'un projet"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    
    return {
        "status": "success",
        "project": projects_db[project_id]
    }

# ==================== ENDPOINTS DONNÉES ====================

@app.post("/api/data/upload")
async def upload_data(project_id: str, file: UploadFile = File(...)):
    """Upload et analyse d'un fichier de données"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    
    try:
        # Lire le fichier
        contents = await file.read()
        
        # Détecter le type de fichier et charger les données
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(contents))
        elif file.filename.endswith('.json'):
            df = pd.read_json(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Format de fichier non supporté")
        
        # Sauvegarder le fichier
        file_path = os.path.join(UPLOAD_DIR, f"{project_id}_{file.filename}")
        df.to_csv(file_path, index=False)
        
        # Analyser les données
        analysis = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "column_types": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=['object']).columns.tolist(),
            "preview": df.head(10).to_dict('records'),
            "statistics": df.describe().to_dict()
        }
        
        # Mettre à jour le projet
        projects_db[project_id]["data_uploaded"] = True
        projects_db[project_id]["file_path"] = file_path
        projects_db[project_id]["data_analysis"] = analysis
        
        return {
            "status": "success",
            "message": "Fichier uploadé et analysé avec succès",
            "analysis": analysis
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'upload: {str(e)}")

@app.post("/api/data/configure")
async def configure_data(config: DataConfig):
    """Configurer le preprocessing des données"""
    if config.project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    
    project = projects_db[config.project_id]
    
    if not project.get("data_uploaded"):
        raise HTTPException(status_code=400, detail="Aucune donnée uploadée pour ce projet")
    
    # Charger les données
    df = pd.read_csv(project["file_path"])
    
    # Vérifier que la colonne cible existe
    if config.target_column not in df.columns:
        raise HTTPException(status_code=400, detail="Colonne cible non trouvée")
    
    # Séparer features et target
    X = df.drop(columns=[config.target_column])
    y = df[config.target_column]
    
    # Gérer les valeurs manquantes
    if config.handle_missing:
        if config.missing_strategy == "mean":
            X = X.fillna(X.mean())
        elif config.missing_strategy == "median":
            X = X.fillna(X.median())
        elif config.missing_strategy == "drop":
            X = X.dropna()
            y = y[X.index]
        elif config.missing_strategy == "zero":
            X = X.fillna(0)
    
    # Encoder les variables catégorielles
    categorical_cols = X.select_dtypes(include=['object']).columns
    label_encoders = {}
    
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
    
    # Normalisation
    scaler = None
    if config.normalize:
        if config.normalize_method == "StandardScaler":
            scaler = StandardScaler()
            X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    
    # Sauvegarder les données preprocessées
    processed_path = os.path.join(UPLOAD_DIR, f"{config.project_id}_processed.csv")
    processed_df = pd.concat([X, y], axis=1)
    processed_df.to_csv(processed_path, index=False)
    
    # Sauvegarder les transformations
    transformations_path = os.path.join(UPLOAD_DIR, f"{config.project_id}_transformations.pkl")
    with open(transformations_path, 'wb') as f:
        pickle.dump({
            'scaler': scaler,
            'label_encoders': label_encoders,
            'target_column': config.target_column
        }, f)
    
    # Mettre à jour le projet
    projects_db[config.project_id]["processed_path"] = processed_path
    projects_db[config.project_id]["transformations_path"] = transformations_path
    projects_db[config.project_id]["target_column"] = config.target_column
    projects_db[config.project_id]["status"] = "configured"
    
    return {
        "status": "success",
        "message": "Données configurées avec succès",
        "shape": X.shape,
        "features": X.columns.tolist()
    }

# ==================== ENDPOINTS ENTRAÎNEMENT ====================

def get_model_instance(model_type: str, task_type: str, hyperparameters: Dict):
    """Instancier un modèle selon le type"""
    if model_type == "Random Forest":
        if task_type == "Classification":
            return RandomForestClassifier(**hyperparameters)
        else:
            return RandomForestRegressor(**hyperparameters)
    
    elif model_type == "XGBoost":
        if task_type == "Classification":
            return xgb.XGBClassifier(**hyperparameters)
        else:
            return xgb.XGBRegressor(**hyperparameters)
    
    elif model_type == "SVM":
        if task_type == "Classification":
            return SVC(**hyperparameters, probability=True)
        else:
            return SVR(**hyperparameters)
    
    elif model_type == "Logistic Regression":
        return LogisticRegression(**hyperparameters)
    
    elif model_type == "Linear Regression":
        return LinearRegression(**hyperparameters)
    
    elif model_type == "KNN":
        return KNeighborsClassifier(**hyperparameters)
    
    elif model_type == "Gradient Boosting":
        return GradientBoostingClassifier(**hyperparameters)
    
    else:
        raise ValueError(f"Type de modèle non supporté: {model_type}")

@app.post("/api/train/start")
async def start_training(config: ModelConfig, background_tasks: BackgroundTasks):
    """Démarrer l'entraînement d'un modèle"""
    if config.project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    
    project = projects_db[config.project_id]
    
    if project.get("status") != "configured":
        raise HTTPException(status_code=400, detail="Les données doivent être configurées d'abord")
    
    try:
        # Charger les données preprocessées
        df = pd.read_csv(project["processed_path"])
        target_column = project["target_column"]
        
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=1-config.train_test_split, random_state=42
        )
        
        # Instancier le modèle
        model = get_model_instance(
            config.model_type,
            project["task_type"],
            config.hyperparameters
        )
        
        # Entraîner le modèle
        start_time = datetime.now()
        model.fit(X_train, y_train)
        training_time = (datetime.now() - start_time).total_seconds()
        
        # Prédictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # Calculer les métriques
        if project["task_type"] == "Classification":
            metrics = {
                "train_accuracy": float(accuracy_score(y_train, y_pred_train)),
                "test_accuracy": float(accuracy_score(y_test, y_pred_test)),
                "precision": float(precision_score(y_test, y_pred_test, average='weighted', zero_division=0)),
                "recall": float(recall_score(y_test, y_pred_test, average='weighted', zero_division=0)),
                "f1_score": float(f1_score(y_test, y_pred_test, average='weighted', zero_division=0)),
                "confusion_matrix": confusion_matrix(y_test, y_pred_test).tolist(),
                "classification_report": classification_report(y_test, y_pred_test, output_dict=True, zero_division=0)
            }
        else:
            metrics = {
                "train_r2": float(r2_score(y_train, y_pred_train)),
                "test_r2": float(r2_score(y_test, y_pred_test)),
                "mse": float(mean_squared_error(y_test, y_pred_test)),
                "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred_test)))
            }
        
        # Cross-validation
        if config.use_cross_validation:
            cv_scores = cross_val_score(model, X, y, cv=config.cv_folds)
            metrics["cv_scores"] = cv_scores.tolist()
            metrics["cv_mean"] = float(cv_scores.mean())
            metrics["cv_std"] = float(cv_scores.std())
        
        # Sauvegarder le modèle
        model_id = str(uuid.uuid4())
        model_path = os.path.join(MODELS_DIR, f"{model_id}.pkl")
        
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        # Créer l'expérience
        experiment = {
            "id": str(uuid.uuid4()),
            "project_id": config.project_id,
            "model_id": model_id,
            "model_type": config.model_type,
            "task_type": project["task_type"],
            "hyperparameters": config.hyperparameters,
            "metrics": metrics,
            "training_time": training_time,
            "created_at": datetime.now().isoformat(),
            "status": "completed"
        }
        
        experiments_db[experiment["id"]] = experiment
        
        # Sauvegarder le modèle dans la DB
        models_db[model_id] = {
            "id": model_id,
            "name": f"{config.model_type} - {project['name']}",
            "project_id": config.project_id,
            "experiment_id": experiment["id"],
            "model_type": config.model_type,
            "model_path": model_path,
            "metrics": metrics,
            "created_at": datetime.now().isoformat(),
            "size_mb": os.path.getsize(model_path) / (1024 * 1024)
        }
        
        return {
            "status": "success",
            "message": "Entraînement terminé avec succès",
            "experiment_id": experiment["id"],
            "model_id": model_id,
            "metrics": metrics,
            "training_time": training_time
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'entraînement: {str(e)}")

@app.get("/api/train/status/{experiment_id}")
async def get_training_status(experiment_id: str):
    """Obtenir le statut d'un entraînement"""
    if experiment_id not in experiments_db:
        raise HTTPException(status_code=404, detail="Expérience non trouvée")
    
    return {
        "status": "success",
        "experiment": experiments_db[experiment_id]
    }

# ==================== ENDPOINTS MODÈLES ====================

@app.get("/api/models/list")
async def list_models():
    """Lister tous les modèles avec task_type et problem_type"""
    models_with_info = []
    
    for model in models_db.values():
        # Récupérer les informations du projet associé
        project_id = model.get("project_id")
        task_type = None
        problem_type = None
        
        if project_id and project_id in projects_db:
            project = projects_db[project_id]
            task_type = project.get("task_type")
            problem_type = project.get("problem_type")
        
        # Créer une copie du modèle avec les nouveaux champs
        model_info = model.copy()
        model_info["task_type"] = task_type
        model_info["problem_type"] = problem_type
        
        models_with_info.append(model_info)
    
    return {
        "status": "success",
        "models": models_with_info
    }

@app.get("/api/models/{model_id}")
async def get_model(model_id: str):
    """Obtenir les détails d'un modèle avec task_type et problem_type"""
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    
    model = models_db[model_id].copy()
    
    # Récupérer les informations du projet associé
    project_id = model.get("project_id")
    if project_id and project_id in projects_db:
        project = projects_db[project_id]
        model["task_type"] = project.get("task_type")
        model["problem_type"] = project.get("problem_type")
    else:
        model["task_type"] = None
        model["problem_type"] = None
    
    return {
        "status": "success",
        "model": model
    }
@app.get("/api/models/download/{model_id}")
async def download_model(model_id: str, format: str = "pkl"):
    """Télécharger un modèle"""
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    
    model_info = models_db[model_id]
    model_path = model_info["model_path"]
    
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Fichier modèle non trouvé")
    
    return FileResponse(
        model_path,
        media_type="application/octet-stream",
        filename=f"{model_id}.{format}"
    )

@app.delete("/api/models/{model_id}")
async def delete_model(model_id: str):
    """Supprimer un modèle"""
    if model_id not in models_db:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    
    model_info = models_db[model_id]
    
    # Supprimer le fichier
    if os.path.exists(model_info["model_path"]):
        os.remove(model_info["model_path"])
    
    # Supprimer de la DB
    del models_db[model_id]
    
    return {
        "status": "success",
        "message": "Modèle supprimé avec succès"
    }

# ==================== ENDPOINTS PRÉDICTIONS ====================

@app.post("/api/predict")
async def make_prediction(request: PredictionRequest):
    """Faire une prédiction avec un modèle"""
    if request.model_id not in models_db:
        raise HTTPException(status_code=404, detail="Modèle non trouvé")
    
    model_info = models_db[request.model_id]
    
    try:
        # Charger le modèle
        with open(model_info["model_path"], 'rb') as f:
            model = pickle.load(f)
        
        # Faire la prédiction
        features = np.array(request.features).reshape(1, -1)
        prediction = model.predict(features)
        
        # Probabilités si classification
        probabilities = None
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(features).tolist()
        
        return {
            "status": "success",
            "prediction": prediction.tolist()[0],
            "probabilities": probabilities
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction: {str(e)}")

# ==================== ENDPOINTS EXPÉRIENCES ====================

@app.get("/api/experiments/list")
async def list_experiments():
    """Lister toutes les expériences"""
    return {
        "status": "success",
        "experiments": list(experiments_db.values())
    }

@app.get("/api/experiments/{experiment_id}")
async def get_experiment(experiment_id: str):
    """Obtenir les détails d'une expérience"""
    if experiment_id not in experiments_db:
        raise HTTPException(status_code=404, detail="Expérience non trouvée")
    
    return {
        "status": "success",
        "experiment": experiments_db[experiment_id]
    }

@app.get("/api/experiments/project/{project_id}")
async def get_project_experiments(project_id: str):
    """Obtenir toutes les expériences d'un projet"""
    project_experiments = [
        exp for exp in experiments_db.values()
        if exp["project_id"] == project_id
    ]
    
    return {
        "status": "success",
        "experiments": project_experiments
    }

# ==================== ENDPOINT RACINE ====================

@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "FrameML API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "projects": "/api/projects",
            "data": "/api/data",
            "train": "/api/train",
            "models": "/api/models",
            "predict": "/api/predict",
            "experiments": "/api/experiments"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "projects": len(projects_db),
        "models": len(models_db),
        "experiments": len(experiments_db)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
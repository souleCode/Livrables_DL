"""
Module de gestion de la base de données SQLite
Fichier: backend/database.py
"""

from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, Boolean, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Configuration de la base de données
DATABASE_URL = "sqlite:///./frameml.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==================== MODÈLES DE DONNÉES ====================

class Project(Base):
    """Table des projets"""
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    problem_type = Column(String, nullable=False)  # ML Classique / Deep Learning
    task_type = Column(String, nullable=False)  # Classification / Régression
    status = Column(String, default="created")  # created, configured, training, completed
    data_uploaded = Column(Boolean, default=False)
    file_path = Column(String, nullable=True)
    processed_path = Column(String, nullable=True)
    transformations_path = Column(String, nullable=True)
    target_column = Column(String, nullable=True)
    data_analysis = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Experiment(Base):
    """Table des expériences d'entraînement"""
    __tablename__ = "experiments"
    
    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, nullable=False, index=True)
    model_id = Column(String, nullable=True)
    name = Column(String, nullable=True)
    model_type = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    hyperparameters = Column(JSON, nullable=True)
    metrics = Column(JSON, nullable=True)
    training_time = Column(Float, nullable=True)
    status = Column(String, default="pending")  # pending, running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class Model(Base):
    """Table des modèles entraînés"""
    __tablename__ = "models"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    project_id = Column(String, nullable=False, index=True)
    experiment_id = Column(String, nullable=True)
    model_type = Column(String, nullable=False)
    model_path = Column(String, nullable=False)
    version = Column(String, default="1.0.0")
    metrics = Column(JSON, nullable=True)
    size_mb = Column(Float, nullable=True)
    status = Column(String, default="active")  # active, deployed, archived
    deployed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Prediction(Base):
    """Table des prédictions"""
    __tablename__ = "predictions"
    
    id = Column(String, primary_key=True, index=True)
    model_id = Column(String, nullable=False, index=True)
    features = Column(JSON, nullable=False)
    prediction = Column(JSON, nullable=False)
    probabilities = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    """Table des utilisateurs (optionnel)"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# ==================== FONCTIONS UTILITAIRES ====================

def init_database():
    """Initialiser la base de données"""
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données initialisée avec succès")

def get_db():
    """Obtenir une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def reset_database():
    """Réinitialiser la base de données (ATTENTION: supprime toutes les données)"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("⚠️ Base de données réinitialisée")

# ==================== CRUD OPERATIONS ====================

class CRUDProject:
    """Opérations CRUD pour les projets"""
    
    @staticmethod
    def create(db, project_data: dict):
        db_project = Project(**project_data)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    
    @staticmethod
    def get(db, project_id: str):
        return db.query(Project).filter(Project.id == project_id).first()
    
    @staticmethod
    def get_all(db):
        return db.query(Project).all()
    
    @staticmethod
    def update(db, project_id: str, update_data: dict):
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project:
            for key, value in update_data.items():
                setattr(db_project, key, value)
            db_project.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_project)
        return db_project
    
    @staticmethod
    def delete(db, project_id: str):
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project:
            db.delete(db_project)
            db.commit()
        return True

class CRUDExperiment:
    """Opérations CRUD pour les expériences"""
    
    @staticmethod
    def create(db, experiment_data: dict):
        db_experiment = Experiment(**experiment_data)
        db.add(db_experiment)
        db.commit()
        db.refresh(db_experiment)
        return db_experiment
    
    @staticmethod
    def get(db, experiment_id: str):
        return db.query(Experiment).filter(Experiment.id == experiment_id).first()
    
    @staticmethod
    def get_all(db):
        return db.query(Experiment).order_by(Experiment.created_at.desc()).all()
    
    @staticmethod
    def get_by_project(db, project_id: str):
        return db.query(Experiment).filter(
            Experiment.project_id == project_id
        ).order_by(Experiment.created_at.desc()).all()
    
    @staticmethod
    def update(db, experiment_id: str, update_data: dict):
        db_experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
        if db_experiment:
            for key, value in update_data.items():
                setattr(db_experiment, key, value)
            db.commit()
            db.refresh(db_experiment)
        return db_experiment
    
    @staticmethod
    def delete(db, experiment_id: str):
        db_experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
        if db_experiment:
            db.delete(db_experiment)
            db.commit()
        return True

class CRUDModel:
    """Opérations CRUD pour les modèles"""
    
    @staticmethod
    def create(db, model_data: dict):
        db_model = Model(**model_data)
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model
    
    @staticmethod
    def get(db, model_id: str):
        return db.query(Model).filter(Model.id == model_id).first()
    
    @staticmethod
    def get_all(db):
        return db.query(Model).order_by(Model.created_at.desc()).all()
    
    @staticmethod
    def get_by_project(db, project_id: str):
        return db.query(Model).filter(
            Model.project_id == project_id
        ).order_by(Model.created_at.desc()).all()
    
    @staticmethod
    def get_active(db):
        return db.query(Model).filter(Model.status == "active").all()
    
    @staticmethod
    def get_deployed(db):
        return db.query(Model).filter(Model.deployed == True).all()
    
    @staticmethod
    def update(db, model_id: str, update_data: dict):
        db_model = db.query(Model).filter(Model.id == model_id).first()
        if db_model:
            for key, value in update_data.items():
                setattr(db_model, key, value)
            db_model.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_model)
        return db_model
    
    @staticmethod
    def delete(db, model_id: str):
        db_model = db.query(Model).filter(Model.id == model_id).first()
        if db_model:
            db.delete(db_model)
            db.commit()
        return True

class CRUDPrediction:
    """Opérations CRUD pour les prédictions"""
    
    @staticmethod
    def create(db, prediction_data: dict):
        db_prediction = Prediction(**prediction_data)
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        return db_prediction
    
    @staticmethod
    def get(db, prediction_id: str):
        return db.query(Prediction).filter(Prediction.id == prediction_id).first()
    
    @staticmethod
    def get_by_model(db, model_id: str, limit: int = 100):
        return db.query(Prediction).filter(
            Prediction.model_id == model_id
        ).order_by(Prediction.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def count_by_model(db, model_id: str):
        return db.query(Prediction).filter(Prediction.model_id == model_id).count()

# ==================== INITIALISATION ====================

if __name__ == "__main__":
    print("Initialisation de la base de données...")
    init_database()
    print("✅ Terminé!")
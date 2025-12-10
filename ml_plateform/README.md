# 🚀 Backend FastAPI - FrameML

Backend API pour la plateforme ML/Deep Learning

## 📁 Structure du Projet

```
backend/
├── main.py                    # Application FastAPI principale
├── database.py                # Gestion SQLite et modèles
├── requirements.txt           # Dépendances Python
├── .env                       # Variables d'environnement (à créer)
├── data/
│   ├── uploads/              # Fichiers uploadés
│   ├── models/               # Modèles ML sauvegardés
│   └── results/              # Résultats d'entraînement
└── frameml.db                # Base de données SQLite
```

## 🔧 Installation

### 1. Créer un environnement virtuel

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Initialiser la base de données

```bash
python database.py
```

### 4. Lancer le serveur

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Le serveur sera accessible sur : **http://localhost:8000**

## 📚 Documentation API

Une fois le serveur lancé, accédez à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🔌 Endpoints Disponibles

### 🏠 Général

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Informations de l'API |
| GET | `/api/health` | Health check |

### 📁 Projets

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/projects/create` | Créer un nouveau projet |
| GET | `/api/projects/list` | Lister tous les projets |
| GET | `/api/projects/{project_id}` | Obtenir un projet |

### 📊 Données

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/data/upload` | Upload fichier de données |
| POST | `/api/data/configure` | Configurer preprocessing |

### 🎯 Entraînement

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/train/start` | Démarrer l'entraînement |
| GET | `/api/train/status/{experiment_id}` | Statut de l'entraînement |

### 🤖 Modèles

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/models/list` | Lister tous les modèles |
| GET | `/api/models/{model_id}` | Détails d'un modèle |
| GET | `/api/models/download/{model_id}` | Télécharger un modèle |
| DELETE | `/api/models/{model_id}` | Supprimer un modèle |

### 🔮 Prédictions

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/predict` | Faire une prédiction |

### 📈 Expériences

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/experiments/list` | Lister toutes les expériences |
| GET | `/api/experiments/{experiment_id}` | Détails d'une expérience |
| GET | `/api/experiments/project/{project_id}` | Expériences d'un projet |

## 📝 Exemples d'Utilisation

### 1. Créer un Projet

```bash
curl -X POST "http://localhost:8000/api/projects/create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Prédiction Prix Immobilier",
    "description": "Projet de classification",
    "problem_type": "ML Classique",
    "task_type": "Classification"
  }'
```

**Réponse:**
```json
{
  "status": "success",
  "project_id": "abc-123-def-456",
  "message": "Projet créé avec succès"
}
```

### 2. Upload des Données

```bash
curl -X POST "http://localhost:8000/api/data/upload?project_id=abc-123-def-456" \
  -F "file=@data.csv"
```

**Réponse:**
```json
{
  "status": "success",
  "message": "Fichier uploadé et analysé avec succès",
  "analysis": {
    "rows": 1000,
    "columns": 15,
    "column_names": ["col1", "col2", ...],
    "missing_values": {...}
  }
}
```

### 3. Configurer les Données

```bash
curl -X POST "http://localhost:8000/api/data/configure" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "abc-123-def-456",
    "target_column": "price",
    "handle_missing": true,
    "missing_strategy": "mean",
    "normalize": true,
    "normalize_method": "StandardScaler"
  }'
```

### 4. Entraîner un Modèle

```bash
curl -X POST "http://localhost:8000/api/train/start" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "abc-123-def-456",
    "model_type": "Random Forest",
    "hyperparameters": {
      "n_estimators": 100,
      "max_depth": 10,
      "random_state": 42
    },
    "train_test_split": 0.8,
    "cv_folds": 5,
    "use_cross_validation": true
  }'
```

**Réponse:**
```json
{
  "status": "success",
  "message": "Entraînement terminé avec succès",
  "experiment_id": "exp-789",
  "model_id": "model-456",
  "metrics": {
    "train_accuracy": 0.95,
    "test_accuracy": 0.92,
    "precision": 0.91,
    "recall": 0.90,
    "f1_score": 0.905
  },
  "training_time": 15.3
}
```

### 5. Faire une Prédiction

```bash
curl -X POST "http://localhost:8000/api/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "model-456",
    "features": [1.5, 2.3, 4.5, 3.2, 5.1]
  }'
```

**Réponse:**
```json
{
  "status": "success",
  "prediction": 1,
  "probabilities": [[0.15, 0.85]]
}
```

### 6. Télécharger un Modèle

```bash
curl -X GET "http://localhost:8000/api/models/download/model-456?format=pkl" \
  -o model.pkl
```

## 🔐 Sécurité (À Implémenter)

Pour la production, ajoutez :
- Authentification JWT
- Rate limiting
- Validation des fichiers
- HTTPS
- Variables d'environnement pour secrets

## 🐍 Utilisation avec Python

```python
import requests
import pandas as pd

# Configuration
BASE_URL = "http://localhost:8000"

# 1. Créer un projet
response = requests.post(
    f"{BASE_URL}/api/projects/create",
    json={
        "name": "Mon Projet ML",
        "problem_type": "ML Classique",
        "task_type": "Classification"
    }
)
project_id = response.json()["project_id"]

# 2. Upload des données
files = {"file": open("data.csv", "rb")}
response = requests.post(
    f"{BASE_URL}/api/data/upload",
    params={"project_id": project_id},
    files=files
)

# 3. Configurer
response = requests.post(
    f"{BASE_URL}/api/data/configure",
    json={
        "project_id": project_id,
        "target_column": "target",
        "normalize": True
    }
)

# 4. Entraîner
response = requests.post(
    f"{BASE_URL}/api/train/start",
    json={
        "project_id": project_id,
        "model_type": "Random Forest",
        "hyperparameters": {
            "n_estimators": 100,
            "max_depth": 10
        }
    }
)
model_id = response.json()["model_id"]

# 5. Prédire
response = requests.post(
    f"{BASE_URL}/api/predict",
    json={
        "model_id": model_id,
        "features": [1.0, 2.0, 3.0, 4.0, 5.0]
    }
)
prediction = response.json()["prediction"]
print(f"Prédiction: {prediction}")
```

## 📦 Modèles Supportés

### ML Classique
- ✅ Random Forest (Classification/Régression)
- ✅ XGBoost (Classification/Régression)
- ✅ SVM (Classification/Régression)
- ✅ Logistic Regression
- ✅ Linear Regression
- ✅ K-Nearest Neighbors
- ✅ Gradient Boosting

### Deep Learning (À ajouter)
- 🔜 CNN (Convolutional Neural Networks)
- 🔜 RNN/LSTM (Recurrent Neural Networks)
- 🔜 Transformers
- 🔜 AutoEncoders

## 🐛 Débogage

### Logs
Les logs sont affichés dans la console. Pour les sauvegarder :

```bash
uvicorn main:app --reload --log-config=logging.conf
```

### Vérifier la santé de l'API

```bash
curl http://localhost:8000/api/health
```

### Réinitialiser la base de données

```python
from database import reset_database
reset_database()
```

## 🚀 Déploiement

### Docker (Recommandé)

Créer un `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build et run:
```bash
docker build -t frameml-backend .
docker run -p 8000:8000 frameml-backend
```

### Production avec Gunicorn

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📊 Performance

- **Upload**: Limite de 200 MB par fichier
- **Entraînement**: Asynchrone en background
- **Prédictions**: < 100ms pour modèles simples

## 🤝 Contribution

Pour contribuer :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

MIT License - voir LICENSE pour plus de détails

## 📧 Support

Pour toute question : support@frameml.com

---

**Fait avec ❤️ pour la communauté ML**
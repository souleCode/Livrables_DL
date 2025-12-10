class ModelConfigurator:
    def __init__(self):
        pass
    
    def get_available_models(self, problem_type, task_type):
        """Retourne les modèles disponibles selon le type de problème"""
        classic_ml = ["Random Forest", "XGBoost", "SVM", "Logistic Regression"]
        deep_learning = ["Neural Network", "CNN", "RNN", "Transformer"]
        
        if problem_type == "Machine Learning Classique":
            return classic_ml
        else:
            return deep_learning
    
    def get_default_params(self, model_name):
        """Retourne les paramètres par défaut pour un modèle"""
        defaults = {
            "Random Forest": {
                "n_estimators": 100,
                "max_depth": 10,
                "min_samples_split": 2
            },
            "XGBoost": {
                "n_estimators": 100,
                "learning_rate": 0.1,
                "max_depth": 6
            },
            "Neural Network": {
                "layers": 3,
                "units": 128,
                "activation": "relu"
            }
        }
        return defaults.get(model_name, {})
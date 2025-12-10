import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer

class DataProcessor:
    def __init__(self, df):
        self.df = df.copy()
        self.original_shape = df.shape
    
    def detect_column_types(self):
        """Détecte automatiquement les types de colonnes"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        datetime_cols = self.df.select_dtypes(include=['datetime64']).columns.tolist()
        
        return {
            'numeric': numeric_cols,
            'categorical': categorical_cols,
            'datetime': datetime_cols
        }
    
    def handle_missing_values(self, strategy='mean'):
        """Gère les valeurs manquantes"""
        strategies = {
            'mean': SimpleImputer(strategy='mean'),
            'median': SimpleImputer(strategy='median'),
            'most_frequent': SimpleImputer(strategy='most_frequent'),
            'constant': SimpleImputer(strategy='constant', fill_value=0)
        }
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if strategy in strategies and len(numeric_cols) > 0:
            imputer = strategies[strategy]
            self.df[numeric_cols] = imputer.fit_transform(self.df[numeric_cols])
        
        # Pour les catégorielles, on remplace par la mode
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if self.df[col].isnull().any():
                self.df[col].fillna(self.df[col].mode()[0], inplace=True)
        
        return self.df
    
    def encode_categorical(self, method='onehot'):
        """Encode les variables catégorielles"""
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        if method == 'label':
            for col in categorical_cols:
                le = LabelEncoder()
                self.df[col] = le.fit_transform(self.df[col])
        elif method == 'onehot':
            self.df = pd.get_dummies(self.df, columns=categorical_cols, prefix=categorical_cols)
        
        return self.df
    
    def normalize_data(self):
        """Normalise les données numériques"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            scaler = StandardScaler()
            self.df[numeric_cols] = scaler.fit_transform(self.df[numeric_cols])
        
        return self.df
    
    def remove_duplicates(self):
        """Supprime les doublons"""
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates()
        removed_count = initial_count - len(self.df)
        
        return self.df, removed_count
    
    def get_summary_stats(self):
        """Retourne les statistiques sommaires"""
        return {
            'original_shape': self.original_shape,
            'current_shape': self.df.shape,
            'missing_values': self.df.isnull().sum().sum(),
            'numeric_columns': len(self.df.select_dtypes(include=[np.number]).columns),
            'categorical_columns': len(self.df.select_dtypes(include=['object']).columns)
        }
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, r2_score,
    confusion_matrix, ConfusionMatrixDisplay, classification_report
)
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

YELLOW = '\033[93m'
STOP = '\033[0m'


class BaseModel:
    def __init__(self, models_dir="models", confmat_dir="confusion_matrices"):
        self.models_dir = models_dir
        self.confmat_dir = confmat_dir
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.confmat_dir, exist_ok=True)
    
    
    
    def preprocess_data(self, df, features, target=None):
        """Common preprocessing for all models"""
        X = df[features].copy()
        
        # Encode categorical features
        for col in X.select_dtypes(include=['object', 'category']).columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
        
        # Check for NaN values
        if X.isnull().any().any():
            print(f"{YELLOW}Warning: NaN values detected after encoding. Please clean your dataset first using the 'clean' command to handle missing values.{STOP}")
            return None, None
        
        if target is not None:
            y = df[target]
            return X, y
        else:
            return X, None
    
    
    # These functions should be protected
    def save_model(self, model, model_name):
        path = os.path.join(self.models_dir, f"{model_name}.joblib")
        joblib.dump(model, path)
    
    
    
    def load_model(self, model_name):
        path = os.path.join(self.models_dir, f"{model_name}.joblib")
    
        if not os.path.exists(path):
            return None
        return joblib.load(path)
    
    
    
    def list_models(self):
        model_files = []
        for f in os.listdir(self.models_dir):
            if f.endswith('.joblib'):
                model_files.append(f)
        return model_files





class LinearRegressionModel(BaseModel):
    def train(self, df, features, target, model_name):
        X, y = self.preprocess_data(df, features, target)
        if X is None:
            return None, None, None, None, None
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        score = r2_score(y_test, y_pred) #This is the R^2 score, it is a measure of how well the model fits the data
        # Thought I'd add here that the rest of the metrics are used for classification tasks (where output is a class/label)
        # Regression predicts continuous values, so those metrics don't apply.
        
        self.save_model(model, model_name)
        return model, score, X_test, y_test, y_pred






class LogisticRegressionModel(BaseModel):
    def train(self, df, features, target, model_name):
        X, y = self.preprocess_data(df, features, target)
        if X is None:
            return None, None, None, None, None, None, None, None, None
        
        # Encode target for classification
        le = LabelEncoder()
        y = le.fit_transform(y)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        report = classification_report(y_test, y_pred)
        
        self.save_model(model, model_name)
        return model, acc, prec, rec, f1, report, X_test, y_test, y_pred
    
    
    
    def save_confusion_matrix(self, y_true, y_pred, model_name):
        cm = confusion_matrix(y_true, y_pred)
    
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    
        disp.plot(cmap=plt.cm.Blues)
        plt.title(f"Confusion Matrix: {model_name}")
        plt.tight_layout()
    
        path = os.path.join(self.confmat_dir, f"{model_name}_confmat.png")
    
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        return path







class KMeansModel(BaseModel):
    def train(self, df, features, n_clusters, model_name):
        X, _ = self.preprocess_data(df, features, None)  # No target for clustering
        if X is None:
            return None, None
        
        model = KMeans(n_clusters=n_clusters, random_state=42)
        model.fit(X)
        labels = model.labels_
        
        self.save_model(model, model_name)
        return model, labels 
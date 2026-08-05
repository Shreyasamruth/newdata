import os
import sys
import time
import json
import joblib
import pandas as pd
import numpy as np

# Ensure app directory is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.feature_extractor import extract_features
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.ensemble import RandomForestClassifier

def train_and_evaluate_models():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data.csv'))
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}")
        return

    print(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path, on_bad_lines='skip')
    print(f"Total raw rows: {len(df)}")
    
    # Drop NA and ensure proper columns
    df = df.dropna(subset=['password', 'strength'])
    df['password'] = df['password'].astype(str)
    df['strength'] = df['strength'].astype(int)

    # Sample 100,000 rows for fast and balanced training if dataset is > 100k
    if len(df) > 100000:
        print("Sampling 100,000 records with stratified sampling...")
        df_sample = df.groupby('strength', group_keys=False).apply(
            lambda x: x.sample(min(len(x), 35000), random_state=42)
        ).reset_index(drop=True)
    else:
        df_sample = df

    print(f"Extracted sample size: {len(df_sample)}")
    print("Class distribution:\n", df_sample['strength'].value_counts())

    print("Extracting 15 password security features...")
    features_list = []
    for pwd in df_sample['password']:
        features_list.append(extract_features(pwd))

    X = pd.DataFrame(features_list)
    y = df_sample['strength'].values

    feature_names = list(X.columns)
    print(f"Extracted features: {feature_names}")

    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Define the 6 models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=500, random_state=42),
        "Support Vector Machine": SGDClassifier(loss='log_loss', max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
    }

    # Dynamically include XGBoost, LightGBM, CatBoost if installed
    try:
        from xgboost import XGBClassifier
        models["XGBoost"] = XGBClassifier(n_estimators=100, max_depth=8, learning_rate=0.1, random_state=42, n_jobs=-1)
    except ImportError:
        print("XGBoost not available during initialization")

    try:
        from lightgbm import LGBMClassifier
        models["LightGBM"] = LGBMClassifier(n_estimators=100, max_depth=8, learning_rate=0.1, random_state=42, n_jobs=-1, verbose=-1)
    except ImportError:
        print("LightGBM not available during initialization")

    try:
        from catboost import CatBoostClassifier
        models["CatBoost"] = CatBoostClassifier(iterations=100, depth=6, learning_rate=0.1, random_state=42, verbose=0)
    except ImportError:
        print("CatBoost not available during initialization")

    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_model_obj = None

    print("\n================ BENCHMARKING 6 MODELS ================")
    for name, model in models.items():
        print(f"\nTraining {name}...")
        start_time = time.time()
        
        # XGBoost and CatBoost work well with unscaled or scaled; using scaled for consistency
        model.fit(X_train_scaled, y_train)
        train_time = round(time.time() - start_time, 3)

        # Inference benchmarking
        inf_start = time.time()
        y_pred = model.predict(X_test_scaled)
        inf_time_ms = round(((time.time() - inf_start) / len(y_test)) * 1000, 4)

        acc = accuracy_score(y_test, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')

        print(f"Results for {name}:")
        print(f"  Accuracy:  {acc:.4f}")
        print(f"  Precision: {prec:.4f}")
        print(f"  Recall:    {rec:.4f}")
        print(f"  F1 Score:  {f1:.4f}")
        print(f"  Training Time: {train_time}s | Inf Latency: {inf_time_ms} ms/sample")

        results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "train_time_sec": train_time,
            "latency_ms": inf_time_ms
        }

        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model_obj = model

    print(f"\n================ WINNING MODEL: {best_model_name} (F1: {best_f1:.4f}) ================")

    # Feature Importance analysis for best tree-based model
    feature_importances = {}
    if hasattr(best_model_obj, 'feature_importances_'):
        importances = best_model_obj.feature_importances_
        for f_name, imp in zip(feature_names, importances):
            feature_importances[f_name] = round(float(imp), 4)

    # Save artifacts
    artifacts_dir = os.path.dirname(__file__)
    os.makedirs(artifacts_dir, exist_ok=True)

    joblib.dump(best_model_obj, os.path.join(artifacts_dir, 'best_model.pkl'))
    joblib.dump(scaler, os.path.join(artifacts_dir, 'scaler.pkl'))

    metrics_payload = {
        "winning_model": best_model_name,
        "feature_names": feature_names,
        "feature_importances": feature_importances,
        "models_benchmark": results
    }

    with open(os.path.join(artifacts_dir, 'metrics.json'), 'w') as f:
        json.dump(metrics_payload, f, indent=2)

    print("Successfully saved best_model.pkl, scaler.pkl, and metrics.json!")

if __name__ == "__main__":
    train_and_evaluate_models()

import os
import json
import joblib
import pandas as pd
from app.services.feature_extractor import extract_features

class MLEngine:
    def __init__ (self):
        self.model = None
        self.scaler = None
        self.metrics = None
        self._load_artifacts()

    def _load_artifacts(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ml_models'))
        model_path = os.path.join(base_dir, 'best_model.pkl')
        scaler_path = os.path.join(base_dir, 'scaler.pkl')
        metrics_path = os.path.join(base_dir, 'metrics.json')

        if os.path.exists(model_path) and os.path.exists(scaler_path):
            try:
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
            except Exception as e:
                print(f"Error loading ML artifacts: {e}")

        if os.path.exists(metrics_path):
            try:
                with open(metrics_path, 'r') as f:
                    self.metrics = json.load(f)
            except Exception as e:
                print(f"Error loading metrics.json: {e}")

    def predict(self, password: str) -> dict:
        """
        Extracts features, runs scaled inference, and returns predicted strength class + probabilities.
        Strength mapping: 0 = Weak, 1 = Medium, 2 = Strong, 3 = Very Strong.
        """
        features_dict = extract_features(password)
        
        # If model artifacts are missing, fallback to entropy-based classification
        if self.model is None or self.scaler is None:
            entropy = features_dict['shannon_entropy']
            length = features_dict['length']
            if length < 6 or entropy < 20:
                cls_id = 0
            elif length < 10 or entropy < 45:
                cls_id = 1
            elif length < 14 or entropy < 70:
                cls_id = 2
            else:
                cls_id = 3
            
            label_map = {0: "Weak", 1: "Medium", 2: "Strong", 3: "Very Strong"}
            return {
                "predicted_class_id": cls_id,
                "predicted_label": label_map[cls_id],
                "confidence": 0.85,
                "features": features_dict,
                "model_used": "Heuristic Fallback"
            }

        df_feat = pd.DataFrame([features_dict])
        X_scaled = self.scaler.transform(df_feat)
        
        pred_class = int(self.model.predict(X_scaled)[0])
        
        # Get class probabilities if available
        confidence = 0.90
        if hasattr(self.model, "predict_proba"):
            probas = self.model.predict_proba(X_scaled)[0]
            confidence = round(float(max(probas)), 4)

        label_map = {0: "Weak", 1: "Medium", 2: "Strong", 3: "Very Strong"}
        pred_label = label_map.get(pred_class, "Medium")

        # Refine Very Strong if score & length are exceptional
        if pred_class == 2 and features_dict['length'] >= 14 and features_dict['shannon_entropy'] >= 65:
            pred_class = 3
            pred_label = "Very Strong"

        winning_model = self.metrics.get('winning_model', 'Trained ML Model') if self.metrics else 'Trained ML Model'

        return {
            "predicted_class_id": pred_class,
            "predicted_label": pred_label,
            "confidence": confidence,
            "features": features_dict,
            "model_used": winning_model
        }

    def get_metrics(self) -> dict:
        return self.metrics if self.metrics else {}

# Singleton instance
ml_engine = MLEngine()

import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime

class AnomalyDetector:
    def __init__(self, contamination=0.05):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_fitted = False
        self.history = []
        self.last_train_size = 0

    def _extract_features(self, value, timestamp):
        if timestamp is None:
            timestamp = datetime.now()
        # Sabato (5) o Domenica (6)
        is_weekend = 1 if timestamp.weekday() >= 5 else 0
        # Notte tra le 20 e le 6 del mattino
        is_night = 1 if timestamp.hour < 6 or timestamp.hour >= 20 else 0
        return [value, is_weekend, is_night]

    def fit(self, data):
        if len(data) > 10:
            X = np.array(data)
            self.model.fit(X)
            self.is_fitted = True

    def predict(self, value, timestamp=None):
        features = self._extract_features(value, timestamp)
        self.history.append(features)
        
        # Limit history to prevent excessive memory and training time
        if len(self.history) > 10000:
            self.history = self.history[-10000:]
            self.last_train_size = min(self.last_train_size, 10000)
            
        current_size = len(self.history)
        
        # Initial fit or periodic retrain
        if not self.is_fitted:
            if current_size > 10:
                self.fit(self.history)
                self.last_train_size = current_size
            else:
                return False, 0.0 # Not enough data to predict
        else:
            # Retrain every 100 new values
            if current_size - self.last_train_size >= 100:
                self.fit(self.history)
                self.last_train_size = current_size

        # Predict anomaly
        X = np.array([features])
        prediction = self.model.predict(X)[0] # 1 for normal, -1 for anomaly
        score = self.model.score_samples(X)[0] # Negative score, lower is more anomalous

        is_anomalia = (prediction == -1)
        return is_anomalia, float(score)

# We will instantiate a global detector for the prototype
detector = AnomalyDetector()

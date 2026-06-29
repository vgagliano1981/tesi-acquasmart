import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self, contamination=0.05):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_fitted = False
        self.history = []

    def fit(self, data):
        if len(data) > 10:
            X = np.array(data).reshape(-1, 1)
            self.model.fit(X)
            self.is_fitted = True

    def predict(self, value):
        self.history.append(value)
        # Retrain every 100 new values if history gets large, or just keep history simple
        if not self.is_fitted:
            if len(self.history) > 10:
                self.fit(self.history)
            else:
                return False, 0.0 # Not enough data to predict

        # Predict anomaly
        X = np.array([[value]])
        prediction = self.model.predict(X)[0] # 1 for normal, -1 for anomaly
        score = self.model.score_samples(X)[0] # Negative score, lower is more anomalous

        is_anomalia = (prediction == -1)
        return is_anomalia, float(score)

# We will instantiate a global detector for the prototype
detector = AnomalyDetector()

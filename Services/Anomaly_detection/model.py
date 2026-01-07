"""
    model module to handle anomaly detection logic.
"""
import numpy as np
from sklearn.ensemble import IsolationForest
from config import ISOLATION_FOREST_PARAMS, MIN_TRAINING_SAMPLES


class AnomalyDetector:
    """
    Handles feature collection, model training, and anomaly prediction
    using an Isolation Forest.
    """

    def __init__(self) -> None:
        self.model = IsolationForest(**ISOLATION_FOREST_PARAMS)
        self.feature_buffer: list[np.ndarray] = []
        self.model_fitted: bool = False

    def add_features(self, features: dict) -> np.ndarray:
        """
        Convert feature dict to a numeric vector and store in buffer.

        Args:
            features (dict): Sensor feature values

        Returns:
            np.ndarray: Feature vector ready for prediction
        """
        vector = np.array([
            float(features["temperature"]),
            float(features["humidity"]),
            float(features["vibration"]),
            float(features["temp_humidity_ratio"]),
            float(features["vibration_squared"])
        ]).reshape(1, -1)

        self.feature_buffer.append(vector.flatten())
        return vector

    def fit_if_ready(self) -> bool:
        """
        Fit the model if enough data has been collected.

        Returns:
            bool: True if model was trained in this call, False otherwise
        """
        if not self.model_fitted and len(self.feature_buffer) >= MIN_TRAINING_SAMPLES:
            self.model.fit(np.array(self.feature_buffer))
            self.model_fitted = True
            print("[AnomalyDetector] Model trained successfully")
            return True
        return False

    def predict(self, vector: np.ndarray) -> int:
        """
        Predict whether a feature vector is an anomaly.

        Args:
            vector (np.ndarray): Feature vector

        Returns:
            int: 1 for normal, -1 for anomaly
        """
        if not self.model_fitted:
            raise RuntimeError("Model not trained yet")
        return int(self.model.predict(vector)[0])

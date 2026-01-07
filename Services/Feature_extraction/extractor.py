"""
    extractor module to handle feature extraction logic.
"""

class FeatureExtractor:
    """
    Handles feature engineering for raw sensor data.
    """

    @staticmethod
    def extract_features(raw_data: dict) -> dict:
        """
        Compute derived features from raw sensor data.

        Args:
            raw_data (dict): Raw sensor data

        Returns:
            dict: Extracted feature message ready for Kafka
        """
        features = raw_data["features"]
        temp = features["temperature"]
        humidity = features["humidity"]
        vibration = features["vibration"]

        extracted = {
            "sensor_id": raw_data["sensor_id"],
            "timestamp": raw_data["timestamp"],
            "location": raw_data["location"],
            "features": {
                "temperature": temp,
                "humidity": humidity,
                "vibration": vibration,
                "temp_humidity_ratio": temp / (humidity + 0.01),
                "vibration_squared": vibration ** 2
            }
        }
        return extracted

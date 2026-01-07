"""
    validator module to hande checks whether messages are valid.
"""
from config import REQUIRED_FEATURES


class MessageValidator:
    """Validates that incoming sensor messages contain required features."""

    @staticmethod
    def is_valid_message(data: dict) -> bool:
        """
        Validate a Kafka message.

        Args:
            data (dict): Parsed Kafka message

        Returns:
            bool: True if message contains all required features
        """
        if "features" not in data:
            return False

        features = data["features"]
        for key in REQUIRED_FEATURES:
            if key not in features or features[key] is None:
                return False

        return True

# ============================================
# File: machine_learning/risk_predictor.py
# Description:
# Predicts environmental risk levels using
# simple AI logic.
# ============================================


class RiskPredictor:
    """
    Simulates AI-based risk estimation.
    """

    def predict_risk(self, victim_severity):
        """
        Predict risk score.
        """

        risk_mapping = {
            "critical": 0.9,
            "moderate": 0.6,
            "minor": 0.3
        }

        return risk_mapping[victim_severity]
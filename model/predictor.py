# predictor.py
# This is the module that the Streamlit app imports to make predictions.
# It loads the saved models and turns survey answers into a risk level.

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from model.preprocessing import FEATURE_COLUMNS, preprocess_survey_input


# Messages shown to the user for each risk level
RISK_MESSAGES = {
    'Low': (
        "Your responses suggest a lower risk level. That's encouraging! "
        "Remember that everyone faces challenges sometimes, and it's always "
        "okay to reach out if you need support."
    ),
    'Moderate': (
        "Some of your responses suggest moderate risk factors. It might be "
        "helpful to talk to someone you trust, such as a parent, teacher, or "
        "school counsellor, about how you're feeling."
    ),
    'Elevated': (
        "Your responses indicate several risk factors that deserve attention. "
        "We strongly encourage you to speak with a school counsellor, parent, "
        "or another trusted adult soon. You don't have to go through this alone."
    ),
}

RISK_COLORS = {
    'Low': 'green',
    'Moderate': 'orange',
    'Elevated': 'red',
}


class MentalHealthPredictor:
    """Loads the trained models and makes predictions from survey answers."""

    def __init__(self, model_dir=None):
        # Default to the trained/ folder next to this file
        if model_dir is None:
            model_dir = Path(__file__).resolve().parent / 'trained'
        else:
            model_dir = Path(model_dir)

        # Load the config file; raise a clear error if it is missing
        config_path = model_dir / 'model_config.json'
        try:
            with open(config_path) as f:
                self.config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Model config not found at {config_path}. "
                "Run model/train_model.py first to train and save the models."
            )

        # Load both trained models; raise a clear error if files are missing
        try:
            self.lgb_model = joblib.load(model_dir / self.config['lgb_path'])
            self.xgb_model = joblib.load(model_dir / self.config['xgb_path'])
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"Trained model file not found: {e}. "
                "Run model/train_model.py first to train and save the models."
            )

        self.threshold = self.config['threshold']
        self.risk_cutoffs = self.config['risk_cutoffs']

    def predict_probability(self, features):
        """Run both models and average their predictions."""
        lgb_prob = self.lgb_model.predict_proba(features)[:, 1][0]
        xgb_prob = self.xgb_model.predict_proba(features)[:, 1][0]
        return float((lgb_prob + xgb_prob) / 2)

    def get_risk_level(self, probability):
        """Turn a probability into Low/Moderate/Elevated."""
        if probability < self.risk_cutoffs['low_medium']:
            return 'Low'
        elif probability < self.risk_cutoffs['medium_high']:
            return 'Moderate'
        else:
            return 'Elevated'

    def predict(self, raw_answers):
        """Main method - takes survey answers and returns the risk assessment.

        If gender is non-binary or 'prefer not to say', we run the prediction
        twice (once as male, once as female) and average the results."""

        gender = raw_answers.get('gender')

        if gender is not None and gender in (0, 1):
            # Normal case - just run prediction
            features = preprocess_survey_input(raw_answers)
            probability = self.predict_probability(features)
        else:
            # Non-binary / prefer not to say - average both
            answers_male = raw_answers.copy()
            answers_male['gender'] = 0
            answers_female = raw_answers.copy()
            answers_female['gender'] = 1

            prob_m = self.predict_probability(preprocess_survey_input(answers_male))
            prob_f = self.predict_probability(preprocess_survey_input(answers_female))
            probability = (prob_m + prob_f) / 2

        risk_level = self.get_risk_level(probability)

        return {
            'probability': round(probability, 4),
            'risk_level': risk_level,
            'risk_color': RISK_COLORS[risk_level],
            'message': RISK_MESSAGES[risk_level],
        }

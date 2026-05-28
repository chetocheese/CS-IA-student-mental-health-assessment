# preprocessing.py
# Cleans the raw training data and prepares features for the ML model.
# Adapted from the original Kaggle competition code but filtered to students only.

import pandas as pd
import numpy as np
from pathlib import Path


# Mappings to convert text categories into numbers
GENDER_MAP = {'Male': 0, 'Female': 1}

SLEEP_MAP = {
    'Less than 5 hours': 0,
    '5-6 hours': 1,
    '7-8 hours': 2,
    'More than 8 hours': 3,
}

DIET_MAP = {
    'Unhealthy': 0,
    'Moderate': 1,
    'Healthy': 2,
}

BINARY_YES_NO = {'No': 0, 'Yes': 1}

# The 14 features our model uses (in order)
FEATURE_COLUMNS = [
    'Gender',
    'Age',
    'Academic_Pressure',
    'CGPA',
    'Study_Satisfaction',
    'Sleep_Duration',
    'Dietary_Habits',
    'Have_you_ever_had_suicidal_thoughts_',
    'Work_Study_Hours',
    'Financial_Stress',
    'Family_History_of_Mental_Illness',
    'Stress_Indicator',
    'Poor_Sleep',
    'High_Financial_Stress',
]


def preprocess_training_data(df):
    """Takes the raw CSV dataframe, filters to students, cleans it up,
    encodes categories as numbers, and adds engineered features."""
    df = df.copy()

    # Only keep student rows (remove working professionals)
    if 'Working Professional or Student' in df.columns:
        df = df[df['Working Professional or Student'] == 'Student'].copy()

    # Clean up column names - replace spaces and special chars with underscores
    df.columns = df.columns.str.replace(' ', '_').str.replace('?', '', regex=False).str.replace('/', '_')

    # Drop columns that aren't useful for students
    drop_cols = [
        'Name', 'City', 'Profession', 'Degree',
        'Working_Professional_or_Student',
        'Work_Pressure', 'Job_Satisfaction',
    ]
    for col in drop_cols:
        if col in df.columns:
            df = df.drop(columns=[col])

    # Fill in missing values
    for col in ['Academic_Pressure', 'CGPA', 'Study_Satisfaction']:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    if 'Dietary_Habits' in df.columns and df['Dietary_Habits'].isnull().any():
        df['Dietary_Habits'] = df['Dietary_Habits'].fillna(df['Dietary_Habits'].mode()[0])

    if 'Financial_Stress' in df.columns and df['Financial_Stress'].isnull().any():
        df['Financial_Stress'] = df['Financial_Stress'].fillna(df['Financial_Stress'].median())

    # Convert categories to numbers
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].map(GENDER_MAP)

    if 'Sleep_Duration' in df.columns:
        df['Sleep_Duration'] = df['Sleep_Duration'].map(SLEEP_MAP)
        df['Sleep_Duration'] = df['Sleep_Duration'].fillna(1)  # default to 5-6 hours

    if 'Dietary_Habits' in df.columns:
        df['Dietary_Habits'] = df['Dietary_Habits'].map(DIET_MAP)
        df['Dietary_Habits'] = df['Dietary_Habits'].fillna(1)  # default to Moderate

    if 'Have_you_ever_had_suicidal_thoughts_' in df.columns:
        df['Have_you_ever_had_suicidal_thoughts_'] = df['Have_you_ever_had_suicidal_thoughts_'].map(BINARY_YES_NO)

    if 'Family_History_of_Mental_Illness' in df.columns:
        df['Family_History_of_Mental_Illness'] = df['Family_History_of_Mental_Illness'].map(BINARY_YES_NO)

    # Create new features from existing ones
    df['Stress_Indicator'] = df['Academic_Pressure'] - df['Study_Satisfaction']
    df['Poor_Sleep'] = (df['Sleep_Duration'] <= 1).astype(int)  # 5-6 hours or less
    df['High_Financial_Stress'] = (df['Financial_Stress'] >= 4).astype(int)

    return df


def preprocess_survey_input(answers):
    """Takes a dictionary of survey answers and turns it into a dataframe
    that the model can use for prediction. Used by the Streamlit app."""

    # Map the survey answers to the feature names the model expects
    row = {
        'Gender': answers['gender'],
        'Age': answers['age'],
        'Academic_Pressure': answers['academic_pressure'],
        'CGPA': answers['cgpa'],
        'Study_Satisfaction': answers['study_satisfaction'],
        'Sleep_Duration': answers['sleep_duration'],
        'Dietary_Habits': answers['dietary_habits'],
        'Have_you_ever_had_suicidal_thoughts_': answers['suicidal_thoughts'],
        'Work_Study_Hours': answers['study_hours'],
        'Financial_Stress': answers['financial_stress'],
        'Family_History_of_Mental_Illness': answers['family_history'],
    }

    # Calculate the engineered features (same as in training)
    row['Stress_Indicator'] = row['Academic_Pressure'] - row['Study_Satisfaction']
    row['Poor_Sleep'] = int(row['Sleep_Duration'] <= 1)
    row['High_Financial_Stress'] = int(row['Financial_Stress'] >= 4)

    # Make it a dataframe with the right column order
    df = pd.DataFrame([row], columns=FEATURE_COLUMNS)
    return df

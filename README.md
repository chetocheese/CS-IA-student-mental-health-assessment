# CS-IA-student-mental-health-assessment

A Streamlit web app that screens students for depression risk using a short 5-step survey. It returns a **Low / Moderate / Elevated** risk level and links to Canadian crisis resources.

## Try it live

# [helpingminds.ca/check-in](https://www.helpingminds.ca/check-in/)

> **Disclaimer:** This tool is not a clinical diagnosis. It uses a statistical model trained on survey data and cannot account for your full personal situation. If you are struggling, please reach out to a trusted adult or one of the crisis resources listed in the app.

## How It Works

Users answer questions across five steps:

1. About You — gender, age
2. School Life — academic pressure, grades, study satisfaction, study hours
3. Lifestyle — sleep duration, dietary habits
4. Stress & Support — financial stress, family history of mental illness
5. One More Thing — history of suicidal thoughts (crisis resources shown immediately if yes)

The app then runs an ensemble of LightGBM + XGBoost models (trained on the Kaggle Playground Series S4E11 depression dataset) and maps the averaged probability to a risk level.

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Crisis Resources

| Resource | Contact |
|----------|---------|
| Kids Help Phone | 1-800-668-6868 (call or text) |
| Crisis Text Line | Text HELLO to 686868 |
| 9-8-8 Suicide Crisis Helpline | Call or text 9-8-8 |

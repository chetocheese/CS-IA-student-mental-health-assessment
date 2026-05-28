import streamlit as st

from model.predictor import MentalHealthPredictor

st.set_page_config(
    page_title="Student Mental Health Check-In",
    page_icon=":brain:",
    layout="centered",
)

TOTAL_STEPS = 5

GRADE_TO_CGPA = {
    "90% and above": 9.5,
    "80 - 89%": 8.5,
    "70 - 79%": 7.5,
    "60 - 69%": 6.5,
    "Below 60%": 5.5,
}

SLEEP_OPTIONS = {
    "Less than 5 hours": 0,
    "5 - 6 hours": 1,
    "7 - 8 hours": 2,
    "More than 8 hours": 3,
}

DIET_OPTIONS = {
    "Mostly unhealthy": 0,
    "Mixed": 1,
    "Mostly healthy": 2,
}

GENDER_OPTIONS = {
    "Male": 0,
    "Female": 1,
    "Non-binary": None,
    "Prefer not to say": None,
}

CRISIS_RESOURCES = """
**If you are in crisis, please reach out now:**

| Resource | Contact |
|----------|---------|
| Kids Help Phone | **1-800-668-6868** (call or text) |
| Crisis Text Line | Text **HELLO** to **686868** |
| 9-8-8 Suicide Crisis Helpline | Call or text **9-8-8** |

You are not alone. Help is available 24/7.
"""


@st.cache_resource
def load_predictor():
    return MentalHealthPredictor()


def init_state():
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "result" not in st.session_state:
        st.session_state.result = None


def go_next():
    st.session_state.step += 1

def go_back():
    st.session_state.step -= 1

def reset():
    st.session_state.step = 1
    st.session_state.answers = {}
    st.session_state.result = None


def step_about_you():
    st.subheader("Step 1 of 5 — About You")
    st.progress(1 / TOTAL_STEPS)

    ans = st.session_state.answers

    gender_label = st.selectbox(
        "What is your gender?",
        list(GENDER_OPTIONS.keys()),
        index=list(GENDER_OPTIONS.keys()).index(ans.get("gender_label", "Male")),
    )
    ans["gender_label"] = gender_label
    ans["gender"] = GENDER_OPTIONS[gender_label]

    age = st.selectbox(
        "How old are you?",
        list(range(14, 20)),
        index=ans.get("age", 16) - 14,
    )
    ans["age"] = age

    st.button("Next", on_click=go_next, use_container_width=True)


def step_school_life():
    st.subheader("Step 2 of 5 — School Life")
    st.progress(2 / TOTAL_STEPS)

    ans = st.session_state.answers

    ans["academic_pressure"] = st.slider(
        "How much academic pressure do you feel?",
        min_value=1, max_value=5, value=ans.get("academic_pressure", 3),
        help="1 = very little, 5 = overwhelming",
    )

    grade_label = st.selectbox(
        "What are your approximate grades?",
        list(GRADE_TO_CGPA.keys()),
        index=list(GRADE_TO_CGPA.keys()).index(ans.get("grade_label", "80 - 89%")),
    )
    ans["grade_label"] = grade_label
    ans["cgpa"] = GRADE_TO_CGPA[grade_label]

    ans["study_satisfaction"] = st.slider(
        "How satisfied are you with your studies?",
        min_value=1, max_value=5, value=ans.get("study_satisfaction", 3),
        help="1 = very unsatisfied, 5 = very satisfied",
    )

    ans["study_hours"] = st.selectbox(
        "How many hours do you study per day outside of class?",
        list(range(0, 13)),
        index=ans.get("study_hours", 3),
    )

    col1, col2 = st.columns(2)
    col1.button("Back", on_click=go_back, use_container_width=True)
    col2.button("Next", on_click=go_next, use_container_width=True)


def step_lifestyle():
    st.subheader("Step 3 of 5 — Lifestyle")
    st.progress(3 / TOTAL_STEPS)

    ans = st.session_state.answers

    sleep_label = st.radio(
        "How much sleep do you usually get?",
        list(SLEEP_OPTIONS.keys()),
        index=list(SLEEP_OPTIONS.keys()).index(ans.get("sleep_label", "7 - 8 hours")),
    )
    ans["sleep_label"] = sleep_label
    ans["sleep_duration"] = SLEEP_OPTIONS[sleep_label]

    diet_label = st.radio(
        "How would you describe your eating habits?",
        list(DIET_OPTIONS.keys()),
        index=list(DIET_OPTIONS.keys()).index(ans.get("diet_label", "Mixed")),
    )
    ans["diet_label"] = diet_label
    ans["dietary_habits"] = DIET_OPTIONS[diet_label]

    col1, col2 = st.columns(2)
    col1.button("Back", on_click=go_back, use_container_width=True)
    col2.button("Next", on_click=go_next, use_container_width=True)


def step_stress_support():
    st.subheader("Step 4 of 5 — Stress & Support")
    st.progress(4 / TOTAL_STEPS)

    ans = st.session_state.answers

    ans["financial_stress"] = st.slider(
        "How much financial stress do you or your family experience?",
        min_value=1, max_value=5, value=ans.get("financial_stress", 3),
        help="1 = none, 5 = severe",
    )

    family_label = st.radio(
        "Does anyone in your family have a history of mental illness?",
        ["No", "Yes", "Not sure"],
        index=["No", "Yes", "Not sure"].index(ans.get("family_label", "No")),
    )
    ans["family_label"] = family_label
    ans["family_history"] = 1 if family_label == "Yes" else 0

    col1, col2 = st.columns(2)
    col1.button("Back", on_click=go_back, use_container_width=True)
    col2.button("Next", on_click=go_next, use_container_width=True)


def step_one_more_thing():
    st.subheader("Step 5 of 5 — One More Thing")
    st.progress(5 / TOTAL_STEPS)

    ans = st.session_state.answers

    suicidal_label = st.radio(
        "Have you ever had thoughts of hurting yourself or ending your life?",
        ["No", "Yes"],
        index=["No", "Yes"].index(ans.get("suicidal_label", "No")),
    )
    ans["suicidal_label"] = suicidal_label
    ans["suicidal_thoughts"] = 1 if suicidal_label == "Yes" else 0

    if suicidal_label == "Yes":
        st.error(CRISIS_RESOURCES)

    col1, col2 = st.columns(2)
    col1.button("Back", on_click=go_back, use_container_width=True)
    col2.button("See My Results", on_click=compute_result, type="primary",
                use_container_width=True)


def compute_result():
    ans = st.session_state.answers
    predictor = load_predictor()
    st.session_state.result = predictor.predict(ans)
    st.session_state.step = TOTAL_STEPS + 1


def show_results():
    result = st.session_state.result
    ans = st.session_state.answers

    st.subheader("Your Results")

    level = result["risk_level"]
    color = result["risk_color"]

    st.markdown(
        f'<div style="background-color:{color}; color:white; '
        f'padding:20px; border-radius:10px; text-align:center; '
        f'font-size:24px; font-weight:bold; margin-bottom:20px;">'
        f'Risk Level: {level}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(result["message"])

    if ans.get("suicidal_thoughts") == 1:
        st.error(CRISIS_RESOURCES)

    st.markdown("---")
    st.markdown("### Resources")
    st.markdown(
        "No matter your result, these resources are always available:\n\n"
        "- **Kids Help Phone**: 1-800-668-6868\n"
        "- **Crisis Text Line**: Text HELLO to 686868\n"
        "- **9-8-8 Suicide Crisis Helpline**: Call or text 9-8-8\n"
        "- **Talk to a school counsellor** — they are there to help."
    )

    st.markdown("---")
    st.caption(
        "This tool is not a clinical diagnosis. It uses a statistical model "
        "trained on survey data and cannot account for your full personal "
        "situation. If you are struggling, please reach out to a trusted adult "
        "or one of the resources listed above."
    )

    st.button("Take Again", on_click=reset, use_container_width=True)


def main():
    init_state()

    st.title("Student Mental Health Check-In")

    st.caption(
        "Your answers are not stored or shared — this tool does not save any information."
    )

    step = st.session_state.step

    if step == 1:
        step_about_you()
    elif step == 2:
        step_school_life()
    elif step == 3:
        step_lifestyle()
    elif step == 4:
        step_stress_support()
    elif step == 5:
        step_one_more_thing()
    else:
        show_results()


if __name__ == "__main__":
    main()

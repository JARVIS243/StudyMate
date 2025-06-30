import streamlit as st
from datetime import datetime, timedelta
from supabase_client import (
    register_user,
    login_user,
    save_study_plan,
    get_all_user_plans,
    save_progress,
    get_progress,
)
from charts import get_progress_summary

st.set_page_config(page_title="StudyMate", layout="wide")

# --- Futuristic UI Styling ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: #e0e0e0;
        font-family: 'Segoe UI', sans-serif;
    }
    .block-container {
        padding: 2rem 3rem;
    }
    .stButton>button {
        background-color: #1f2937;
        color: #ffffff;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        border: none;
        transition: background 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2563eb;
        color: white;
    }
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stDateInput>div>input {
        background-color: #1e293b;
        color: white;
        border-radius: 8px;
        padding: 0.5rem;
    }
    .stCodeBlock {
        background-color: #1f1f2e;
        color: #ffffff;
    }
    h1, h2, h3, h4 {
        color: #60a5fa;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 StudyMate")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "mode" not in st.session_state:
    st.session_state.mode = "login"  # or "register"

def login_ui():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = user["username"]
            st.session_state.name = user["name"]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")
    if st.button("Don't have an account? Register"):
        st.session_state.mode = "register"
        st.rerun()

def register_ui():
    st.subheader("📝 Register")
    name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(username, password, name):
            st.success("Registered successfully! Please login. Nanniyunde 🙏")
            st.session_state.mode = "login"
            st.rerun()
        else:
            st.error("Username already exists")
    if st.button("Already have an account? Login"):
        st.session_state.mode = "login"
        st.rerun()

if not st.session_state.logged_in:
    if st.session_state.mode == "login":
        login_ui()
    else:
        register_ui()
    st.stop()

# -------------------------
# Dashboard after login
# -------------------------

username = st.session_state.username
name = st.session_state.name
st.success(f"Welcome, {name} 😎")

st.subheader("📅 Create Study Plan")
subject = st.text_input("Subject")
modules = st.number_input("Number of Modules", min_value=1, step=1)
days = st.number_input("Days to Complete", min_value=1, step=1)
start_date = st.date_input("Start Date", datetime.now().date())

if st.button("Generate Plan"):
    plan = []
    current_day = start_date
    modules_per_day = modules // days
    leftover = modules % days
    index = 1

    for day in range(days):
        count = modules_per_day + (1 if day < leftover else 0)
        daily_modules = [f"{subject} - M{index + i}" for i in range(count)]
        plan.append((current_day.isoformat(), daily_modules))
        current_day += timedelta(days=1)
        index += count

    plan_md = ""
    for day, tasks in plan:
        plan_md += f"📅 {day}\n" + "\n".join(f"- {task}" for task in tasks) + "\n\n"

    st.markdown("### Plan Preview")
    st.code(plan_md)
    save_study_plan(username, plan_md)
    st.success("✅ Plan saved to Database!")

st.divider()
st.subheader("✅ Daily Checklist")

all_plans = get_all_user_plans(username)
progress_data = get_progress(username)
completed_set = set(f"{entry['subject']} - {entry['topic']}" for entry in progress_data)

if all_plans:
    st.markdown("#### 📖 All Saved Study Plans")
    for idx, plan_md in enumerate(all_plans):
        with st.expander(f"📘 Plan #{len(all_plans) - idx}"):
            st.markdown(plan_md)
            st.markdown("**Checklist:**")
            for line in plan_md.splitlines():
                if line.startswith("- "):
                    topic = line[2:]
                    checked = topic in completed_set
                    if st.checkbox(topic, value=checked, key=topic + str(idx)):
                        if not checked:
                            parts = topic.split(" - ")
                            if len(parts) == 2:
                                save_progress(username, parts[0], parts[1])
                                st.toast(f"✅ Saved: {topic}")
else:
    st.info("No study plans yet.")

st.divider()
st.subheader("📊 Progress Summary")
summary = get_progress_summary(username)
if summary:
    for subject, topics in summary.items():
        st.write(f"**{subject}**: {', '.join(topics)}")
else:
    st.info("No completed topics yet.")

st.markdown("<div style='text-align:center; color:#999; margin-top: 30px;'>© 2025 | Published by Aju Krishna</div>", unsafe_allow_html=True)

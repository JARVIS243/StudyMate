import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials
url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]

# Create Supabase client
supabase = create_client(url, key)

# ------------------------------
# Function: Register a new user
# ------------------------------
def register_user(username, password, name):
    existing = supabase.table("users").select("*").eq("username", username).execute()
    if existing.data:
        return False
    supabase.table("users").insert({
        "username": username,
        "password": password,
        "name": name
    }).execute()
    return True

# --------------------------
# Function: Login user
# --------------------------
def login_user(username, password):
    res = supabase.table("users").select("*")\
        .eq("username", username).eq("password", password).execute()
    if res.data:
        return res.data[0]  # Return user record
    return None

# ------------------------------------
# Function: Save a study plan
# ------------------------------------
def save_study_plan(username, plan_md):
    supabase.table("study_plans").insert({
        "username": username,
        "plan_md": plan_md
    }).execute()

# --------------------------------------------
# Function: Get all plans for a user
# --------------------------------------------
def get_all_user_plans(username):
    res = supabase.table("study_plans").select("*")\
        .eq("username", username).order("created_at", desc=True).execute()
    return [r["plan_md"] for r in res.data]

# ---------------------------------
# Function: Save progress
# ---------------------------------
def save_progress(username, subject, topic):
    supabase.table("study_progress").insert({
        "username": username,
        "subject": subject,
        "topic": topic
    }).execute()

# ---------------------------------------
# Function: Get all progress for user
# ---------------------------------------
def get_progress(username):
    res = supabase.table("study_progress").select("*")\
        .eq("username", username).execute()
    return res.data

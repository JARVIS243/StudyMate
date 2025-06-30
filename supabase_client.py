# supabase_client.py
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]
supabase = create_client(url, key)

# Register new user
def register_user(username, password, name):
    existing = supabase.table("users").select("*").eq("username", username).execute()
    if existing.data:
        return False
    supabase.table("users").insert({"username": username, "password": password, "name": name}).execute()
    return True

# Login
def login_user(username, password):
    res = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
    if res.data:
        return res.data[0]  # return the whole user record
    return None

# Save plan with username now
def save_study_plan(username, plan_md):
    supabase.table("study_plans").insert({
        "username": username,
        "plan_md": plan_md
    }).execute()

# Get plans for user
def get_all_user_plans(username):
    res = supabase.table("study_plans").select("*").eq("username", username).order("created_at", desc=True).execute()
    return [r["plan_md"] for r in res.data]

# Save progress
def save_progress(username, subject, topic):
    supabase.table("study_progress").insert({
        "username": username,
        "subject": subject,
        "topic": topic
    }).execute()

# Get all progress
def get_progress(username):
    res = supabase.table("study_progress").select("*").eq("username", username).execute()
    return res.data

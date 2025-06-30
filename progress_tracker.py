from supabase_client import supabase
import pandas as pd

def save_progress(phone, subject, topic, completed):
    try:
        supabase.table("study_progress").insert({
            "phone": phone,
            "subject": subject,
            "topic": topic,
            "completed": completed,
            "date": pd.Timestamp.now().date()
        }).execute()
    except Exception as e:
        print("❌ Error saving progress:", e)

def get_progress(phone):
    try:
        response = supabase.table("study_progress") \
            .select("*") \
            .eq("phone", phone) \
            .execute()
        return response.data if response.data else []
    except Exception as e:
        print("❌ Error fetching progress:", e)
        return []

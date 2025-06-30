from collections import defaultdict
from supabase_client import get_progress

def get_progress_summary(phone):
    progress = get_progress(phone)
    summary = defaultdict(list)
    for row in progress:
        summary[row["subject"]].append(row["topic"])
    return summary

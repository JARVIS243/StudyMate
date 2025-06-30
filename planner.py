# planner.py

from datetime import timedelta
import pandas as pd

def parse_subjects(subject_text):
    """
    Input: Math: Algebra, Geometry\nPhysics: Motion, Optics
    Output: {'Math': ['Algebra', 'Geometry'], 'Physics': ['Motion', 'Optics']}
    """
    subjects = {}
    for line in subject_text.strip().split("\n"):
        if ":" in line:
            subject, topics = line.split(":")
            subjects[subject.strip()] = [t.strip() for t in topics.split(",")]
    return subjects

def generate_study_plan(subject_text, hours_per_day, exam_date):
    subjects = parse_subjects(subject_text)
    exam_date = pd.to_datetime(exam_date)
    today = pd.to_datetime("today").normalize()
    total_days = (exam_date - today).days

    if total_days <= 0:
        return "❌ Invalid exam date. Please select a future date."

    all_topics = [(subj, topic) for subj, topics in subjects.items() for topic in topics]
    plan = []
    topic_index = 0
    day = today

    while topic_index < len(all_topics):
        daily_tasks = []
        for _ in range(hours_per_day):
            if topic_index >= len(all_topics):
                break
            subject, topic = all_topics[topic_index]
            daily_tasks.append(f"{subject} - {topic}")
            topic_index += 1
        plan.append((day.strftime("%Y-%m-%d"), daily_tasks))
        day += timedelta(days=1)

    # Format to Markdown
    result = ""
    for d, tasks in plan:
        result += f"📅 **{d}**\n"
        for t in tasks:
            result += f"- {t}\n"
        result += "\n"
    return result

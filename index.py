import re
import json
from datetime import datetime


def add_entry(project: str, activity: str, time: str):
    """Add a time entry with project, activity, and duration."""
    try:
        minutes = parse_time(time)

        # Save time_logs in a file
        save_entry(activity, project, minutes)

        print(f"Added: {activity} ({project}) - {time}")
    except ValueError as e:
        print(f"Invalid time format. Use '25m' or '1h 05m'. Error: {e}")


def load_logs():
    """Returns the previously saved logs if any"""
    previous_logs = []

    try:
        with open("time_entries.json", "r") as json_file:
            previous_logs = json.load(json_file)  # Load locally saved logs
    except FileNotFoundError:
        pass

    return previous_logs


def parse_time(time: str):
    """Parse time string to minutes (e.g., '25m' or '1h 05m')."""
    time = time.strip().lower()
    if re.search(r"[hm]", time):
        match = re.search(r"(?:(\d+)h)?\s*(?:(\d+)m)?", time)
        if not match:
            raise ValueError("Invalid format")
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        if hours < 0 or minutes < 0:
            raise ValueError("Hours and minutes must be non-negative")
        total = hours * 60 + minutes
    else:
        try:
            total = int(time)
        except ValueError:
            raise ValueError("Time must be a number")
        if total not in [25, 30, 35, 40, 45]:
            raise ValueError("Pomodoro must be 25, 30, 35, 40, or 45 minutes")
    if total <= 0:
        raise ValueError("Time must be positive")
    return total


def print_summary():
    """Print total time per activity and project."""
    time_logs = load_logs()
    if not time_logs:
        print("No entries yet.")
        return
    activity_totals = {}
    project_totals = {}
    for entry in time_logs:
        activity_totals[entry["activity"]] = (
            activity_totals.get(entry["activity"], 0) + entry["minutes"]
        )
        project_totals[entry["project"]] = (
            project_totals.get(entry["project"], 0) + entry["minutes"]
        )
    print("\nActivity Summary:")
    for activity, minutes in activity_totals.items():
        print(f"{activity}: {minutes // 60}h {minutes % 60:02d}m")
    print("\nProject Summary:")
    for project, minutes in project_totals.items():
        print(f"Project {project}: {minutes // 60}h {minutes % 60:02d}m")


def save_entry(activity, project, time):
    """Saves a time entry locally in a JSON"""
    try:
        previous_logs = load_logs()

        now = datetime.now()
        formatted_now = now.strftime("%H:%M %d-%m-%Y")
        time_entry = {
            "activity": activity,
            "project": project,
            "minutes": time,
            "date": formatted_now,
        }

        previous_logs.append(time_entry)

        # Add a new Entry
        with open("time_entries.json", "w", encoding="utf-8") as json_file:
            json.dump(previous_logs, json_file, indent=4)

    except TypeError as e:
        print("Error:", e)


while True:
    action = input("Enter action (add/summary/quit): ").lower()
    if action == "quit":
        print("Goodbye.")
        break
    elif action == "add":
        project = input("Enter the project related: ").strip()
        activity = input("Enter an activity: ").strip()
        time = input("Enter time (e.g., '25m' or '1h 05m'): ").strip()
        add_entry(
            project,
            activity,
            time,
        )
    elif action == "summary":
        print_summary()
    else:
        print("Invalid action.")

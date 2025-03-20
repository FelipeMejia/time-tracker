import re
import json
from datetime import datetime

time_logs: list[dict[str, str | int]] = (
    []
)  # List to store all time entries as dictionaries


def load_logs() -> list[dict[str, str | int]]:
    """Load time entries from a JSON file on startup."""
    previous_logs = []
    try:
        with open("time_entries.json", "r", encoding="utf-8") as json_file:
            previous_logs = json.load(json_file)  # Load locally saved logs
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return previous_logs


def save_entry(activity: str, project: str, minutes: int, date: str):
    """Save a time entry to a JSON file."""
    try:
        previous_logs = load_logs()
        time_entry = {
            "activity": activity,
            "project": project,
            "minutes": minutes,
            "date": date,
        }
        previous_logs.append(time_entry)
        with open("time_entries.json", "w", encoding="utf-8") as json_file:
            json.dump(previous_logs, json_file, indent=4)
    except TypeError as e:
        print("Error:", e)


def add_entry(project: str, activity: str, time: str):
    """Add a time entry with project, activity, and duration."""
    try:
        minutes = parse_time(time)  # Parse the time input into minutes
        now = datetime.now()
        formatted_now = now.strftime("%H:%M %d-%m-%Y")
        entry = {
            "project": project,
            "activity": activity,
            "minutes": minutes,
            "date": formatted_now,
        }
        time_logs.append(entry)  # Add to in-memory log
        save_entry(activity, project, minutes, formatted_now)  # Save to file
        print(f"Added: {activity} ({project}) - {time} on {formatted_now}")
    except ValueError as e:
        print(f"Invalid time format. Use '25m' or '1h 05m'. Error: {e}")


def parse_time(time: str) -> int:
    """Parse time string to minutes (e.g., '25m' or '1h 05m'). Returns an integer."""
    time = time.strip().lower()  # Normalize input
    if re.search(r"[hm]", time):
        match = re.search(r"(?:(\d+)h)?\s*(?:(\d+)m)?", time)
        if not match:
            raise ValueError("Invalid format")
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        if hours < 0 or minutes < 0:
            raise ValueError("Hours and minutes must be non-negative")
        total = hours * 60 + minutes  # Convert to total minutes
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


def print_summary_by_date(date_str: str):
    """Print summary for entries on a specific date (format: YYYY-MM-DD)."""
    if not time_logs:
        print("No entries yet.")
        return
    filtered_logs = [entry for entry in time_logs if entry["date"].startswith(date_str)]
    if not filtered_logs:
        print(f"No entries found for {date_str}.")
        return
    activity_totals = {}
    project_totals = {}
    for entry in filtered_logs:
        activity_totals[entry["activity"]] = (
            activity_totals.get(entry["activity"], 0) + entry["minutes"]
        )
        project_totals[entry["project"]] = (
            project_totals.get(entry["project"], 0) + entry["minutes"]
        )
    print(f"\nActivity Summary for {date_str}:")
    for activity, minutes in activity_totals.items():
        print(f"{activity}: {minutes // 60}h {minutes % 60:02d}m")
    print(f"\nProject Summary for {date_str}:")
    for project, minutes in project_totals.items():
        print(f"Project {project}: {minutes // 60}h {minutes % 60:02d}m")


# Load existing logs on startup
time_logs = load_logs()

while True:
    action = input("Enter action (add/summary/summary_by_date/quit): ").lower()
    if action == "quit":
        print("Goodbye.")
        break
    elif action == "add":
        project = input("Enter the project related: ").strip()
        activity = input("Enter an activity: ").strip()
        time = input("Enter time (e.g., '25m' or '1h 05m'): ").strip()
        add_entry(project, activity, time)
    elif action == "summary":
        print_summary()
    elif action == "summary_by_date":
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        print_summary_by_date(date_str)
    else:
        print("Invalid action.")

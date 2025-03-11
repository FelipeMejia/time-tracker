import re

time_logs: list[dict] = []


def add_entry(project: str, activity: str, time: str):
    try:
        minutes = parse_time(time)
        time_logs.append({"project": project, "activity": activity, "minutes": minutes})
        print(f"Added: {activity} ({project}) - {time}")
    except ValueError:
        print("Invalid time format. Use '25m' or '1h 05m'.")


def parse_time(time: str):
    # Remove extra spaces
    time = time.strip().lower()
    if re.search(r"[hm]", time):
        match = re.search(r"(?:(\d+)h)?(?:(\d+)m)?$", time)

        if not match:
            raise ValueError("Invalid format")

        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0

        total = hours * 60 + minutes
    else:
        total = int(time)

        if total not in [25, 30, 35, 40, 45]:
            raise ValueError("Pomodoro must be 25, 30, 35, 40, or 45 minutes")

        total = int(time)

    if total <= 0:
        raise ValueError("Time must be positive")
    return total


def print_summary():
    activity_totals = {}
    project_totals = {}

    if not time_logs:
        print("No entries yet.")
        return
    for entry in time_logs:
        activity_totals[entry["activity"]] = (
            activity_totals.get(entry["activity"], 0) + entry["minutes"]
        )
        project_totals[entry["project"]] = (
            project_totals.get(entry["project"], 0) + entry["minutes"]
        )
    for activity, minutes in activity_totals.items():
        print(f"{activity}: {minutes // 60}h {minutes % 60:02d}m")
    for project, minutes in project_totals.items():
        print(f"Project {project}: {minutes // 60}h {minutes % 60:02d}m")


while True:
    action = input("Enter action (add/summary/quit): ").lower()
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
    else:
        print("Invalid action.")

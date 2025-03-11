import re

time_logs: list[dict[str, str]] = []


def add_entry(project: str, activity: str, time: str):
    try:
        minutes = parse_time(time)
        time_logs.append({"project": project, "activity": activity, "minutes": minutes})
        print(f"Added: {activity} ({project}) - {time}")
    except ValueError:
        print("Invalid time format. Use '25m' or '1h 05m'.")


def parse_time(time: str):
    # Remove extra spaces
    time = time.replace(" ", "")
    if re.search(r"[hm]", time):
        match = re.search(r"(?:(\d+)h)?(?:(\d+)m)?$", time)

        if not match:
            raise ValueError

        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0

        return hours * 60 + minutes
    else:
        return int(time)


def print_summary():
    print(time_logs)
    for entry in time_logs:
        time = entry["minutes"]
        print(
            f"{entry["activity"]}: {time // 60}h {time % 60}m",
            f"Project {entry["project"]}: {time // 60}h {time % 60}m",
        )


while True:
    action = input("Enter action (add/summary/quit): ").lower()
    if action == "quit":
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


# try:
#     print(parse_time(time))
#     # time_entries: list[dict[str, str]] = []
#     # time_entries.append({"activiy": activity, "project": project, "minutes": time})
# except ValueError:
#     print("Please provide numbers")

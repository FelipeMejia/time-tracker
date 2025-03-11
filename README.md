# Time Tracker

A CLI tool to log time spent on activities and projects.

## About

This is a basic backend for tracking time, associating activities with projects, and calculating totals. It supports pomodoro sessions (25, 30, 35, 40, 45 minutes) and custom durations (e.g., "1h 05m").

## Installation

1. Clone the repository: `git clone https://github.com/FelipeMejia/time-tracker.git`
2. Navigate to the folder: `cd time-tracker`
3. Run the script: `python index.py`

## Usage

- Start the program with `python index.py`.
- Choose an action:
  - `add`: Log a new entry. Enter project name, activity name, and time (e.g., "25m" or "1h 05m").
    ```
    Enter action (add/summary/quit): add
    Enter the project related: Python Mastery
    Enter an activity: Studying Python
    Enter time (e.g., '25m' or '1h 05m'): 25m
    Added: Studying Python (Python Mastery) - 25m
    ```
  - `summary`: View total time per activity and project.
    ```
    Enter action (add/summary/quit): summary
    Activity Summary:
    Studying Python: 0h 25m
    Reading: 1h 05m
    Project Summary:
    Python Mastery: 0h 25m
    Personal Growth: 1h 05m
    ```
  - `quit`: Exit the program with "Goodbye."

## Features

- Logs time entries with project and activity associations.
- Validates pomodoro durations (25, 30, 35, 40, or 45 minutes).
- Aggregates and displays totals per activity and project.

## Future Work

- Persist data to a file (e.g., JSON or SQLite).
- Add CLI argument support for batch entries.
- Implement date-based tracking.

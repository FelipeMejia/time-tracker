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
  - `summary`: prints all the time entries with its project and activiy.
  - `quit`: exits the app

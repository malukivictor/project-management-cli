# Project-Tracking System

A command-line tool for adding users, projects and tasks. all data is saved to a local JSON file.

## Setup

Requires Python 3.10 or newer version of.

    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install python-dateutil

## Usage

Run `python3 main.py COMMAND`. put the quotes around values with spaces.

    python3 main.py add-user --name victor
    python3 main.py add-project --user victor --title "My Project"
    python3 main.py add-task --project "My Project" --title "First task" --assign victor
    python3 main.py complete-task --id 1

    python3 main.py list-users
    python3 main.py list-projects
    python3 main.py list-tasks --project "My Project"

Add `-h` to any command for help, for example `python3 main.py add-task -h`.

## Commands

| Command | What it does |
|---|---|
| add-user | Create a user |
| add-project | Add a project to a user |
| add-task | Add a task to a project |
| complete-task | Mark a task complete |
| list-users | Show all users |
| list-projects | Show all projects (or one user's, with `--user victor`) |
| list-tasks | Show the tasks in a project |

## Files

    main.py           command-line interface
    models/           User, Project and Task classes
    utils/storage.py  saves and loads the JSON data
    data/             tracker.json is created here
    tests/            pytest tests

## Notes

- A user has many projects, and a project has many tasks.
- Due dates for tasks (`--due "Oct 19 2026"`) are stored as YYYY-MM-DD.


## Testing

Tests use pytest and live in the `tests/` folder. 

    python3 -m pip install pytest
    python3 -m pytest -v

The tests check that users, projects and tasks are created correctly

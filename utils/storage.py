import json
import os

from models import User, Project, Task

DATA_FILE = "data/tracker.json"

def save():
    data = {
        "users": {str(u.id): u.to_dict() for u in User.all()},
        "projects": {str(p.id): p.to_dict() for p in Project.all()},
        "tasks": {str(t.id): t.to_dict() for t in Task.all()},
    }
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def _records(section):
    return section.values() if isinstance(section, dict) else section


def load():
    for cls in (User, Project, Task):
        cls.reset()
    try:
        with open(DATA_FILE) as f:
            data = json.load(f)
        for u in _records(data["users"]):
            User.from_dict(u)
        for p in _records(data["projects"]):
            Project.from_dict(p, User.get(p["user_id"]))
        for t in _records(data["tasks"]):
            Task.from_dict(t, Project.get(t["project_id"]), User.get(t["assigned_to"]))
    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError, ValueError):
        print("Warning: data file is damaged, starting empty.")
        for cls in (User, Project, Task):
            cls.reset()

import json
import os

from models import User, Project, Task

DATA_FILE = "data/tracker.json"

def save():
    data = {
        "users": [u.to_dict() for u in User.all()],
        "projects": [p.to_dict() for p in Project.all()],
        "tasks": [t.to_dict() for t in Task.all()],
    }
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load():
    for cls in (User, Project, Task):
        cls.reset()
    try:
        with open(DATA_FILE) as f:
            data = json.load(f)
        for u in data["users"]:
            User(u["name"], u["email"], u["id"])
        for p in data["projects"]:
            Project(User.get(p["user_id"]), p["title"], p["description"], p["due_date"], p["id"])
        for t in data["tasks"]:
            Task(Project.get(t["project_id"]), t["title"], User.get(t["assigned_to"]), t["status"], t["id"])
    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError, ValueError):
        print("Warning: data file is damaged, starting empty.")
        for cls in (User, Project, Task):
            cls.reset()
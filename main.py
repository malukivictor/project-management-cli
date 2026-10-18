import argparse
import sys
from models import User, Project, Task
from utils import storage

def find_user(name):
    user = User.find_by_name(name)
    if not user:
        raise ValueError(f"no user called '{name}'")
    return user

def find_project(title):
    project = Project.find(title)
    if not project:
        raise ValueError(f"no project titled '{title}'")
    return project


def add_user(args):
    print("Added a user:", User.create(args.name, args.email))
    return True


def list_users(args):
    for user in User.all():
        print(user)


def add_project(args):
    owner = find_user(args.user)
    if Project.find(args.title):
        raise ValueError(f"a project titled '{args.title}' already exists")
    print("Added a project:", Project(owner, args.title, args.description, args.due))
    return True


def list_projects(args):
    projects = find_user(args.user).projects if args.user else Project.all()
    for project in projects:
        print(project)


def add_task(args):
    project = find_project(args.project)
    assignee = find_user(args.assign) if args.assign else None
    task = project.add_task(args.title, assignee)
    print(f"added task no. {task.id} to '{project.title}'")
    return True

def list_tasks(args):
    project = find_project(args.project)
    for t in project.tasks:
        who = t.assigned_to.name if t.assigned_to else "unassigned"
        print(f"no. {t.id} {t.title} [{t.status}] - {who}")
    done, total = project.progress
    print(f"{done}/{total} complete")

def complete_task(args):
    task = Task.get(args.id)
    if not task:
        raise ValueError(f"no task with ID {args.id}")
    task.complete()
    print("Completed:", task)
    return True

def build_parser():
    parser = argparse.ArgumentParser(prog="main.py", description="Project-tracking system")
    sub = parser.add_subparsers(dest="command", required=True, metavar="Pick any command: ")
    p = sub.add_parser("add-user", help="create a user")
    p.add_argument("--name", required=True, help=" add the user's name")
    p.add_argument("--email", default="", help="add the user's email ( is optional)")
    p.set_defaults(func=add_user)

    p = sub.add_parser("list-users", help="list all the users in the system")
    p.set_defaults(func=list_users)

    p = sub.add_parser("add-project", help="add a project to the user")
    p.add_argument("--user", required=True, help="owner's name")
    p.add_argument("--title", required=True, help="project title")
    p.add_argument("--description", default="", help="project description (is optional)")
    p.add_argument("--due", help="due date, mm/dd/yyyy (is optional)")
    p.set_defaults(func=add_project)

    p = sub.add_parser("list-projects", help="list projects, optionally for one user")
    p.add_argument("--user", help="only show this user's projects")
    p.set_defaults(func=list_projects)

    p = sub.add_parser("add-task", help="add a task to the project")
    p.add_argument("--project", required=True, help="project title")
    p.add_argument("--title", required=True, help="task title")
    p.add_argument("--assign", help="assign task to: user name (is optional)")
    p.set_defaults(func=add_task)

    p = sub.add_parser("list-tasks", help="list of tasks in a project")
    p.add_argument("--project", required=True, help="project title")
    p.set_defaults(func=list_tasks)

    p = sub.add_parser("complete-task", help="mark the task as complete")
    p.add_argument("--id", type=int, required=True, help="task ID")
    p.set_defaults(func=complete_task)
    return parser

if __name__ == "__main__":
    args = build_parser().parse_args()
    storage.load()
    try:
        if args.func(args):
            storage.save()
    except ValueError as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)

import argparse
import sys
from models import User, Project
from utils import storage

def find_user(name):
    user = User.find_by_name(name)
    if not user:
        raise ValueError(f"no user named '{name}'")
    return user

def add_user(args):
    print("Added user:", User.create(args.name, args.email))
    return True

def list_users(args):
    for user in User.all():
        print(user)

def add_project(args):
    owner = find_user(args.user)
    if Project.find(args.title):
        raise ValueError(f"a project called '{args.title}' already exists")
    print("Added project:", Project(owner, args.title, args.description, args.due))
    return True

def list_projects(args):
    projects = find_user(args.user).projects if args.user else Project.all()
    for project in projects:
        print(project)

def build_parser():
    parser = argparse.ArgumentParser(prog="main.py", description="Project tracker")
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    p = sub.add_parser("add-user", help="create a user")
    p.add_argument("--name", required=True, help="user's name")
    p.add_argument("--email", default="", help="user's email (optional)")
    p.set_defaults(func=add_user)

    p = sub.add_parser("list-users", help="list all users")
    p.set_defaults(func=list_users)

    p = sub.add_parser("add-project", help="add a project to a user")
    p.add_argument("--user", required=True, help="owner's name")
    p.add_argument("--title", required=True, help="project title")
    p.add_argument("--description", default="", help="project description (optional)")
    p.add_argument("--due", help="due date, e.g. 2026-12-01 or 'Dec 1 2026' (optional)")
    p.set_defaults(func=add_project)

    p = sub.add_parser("list-projects", help="list projects, optionally for one user")
    p.add_argument("--user", help="only show this user's projects")
    p.set_defaults(func=list_projects)

    return parser

def main():
    args = build_parser().parse_args()
    storage.load()
    try:
        if args.func(args):
            storage.save()
    except ValueError as e:
        print("Error:", e, file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())

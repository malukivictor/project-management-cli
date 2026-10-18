from models import User, Project, Task
from utils import storage

def add_user():
    name = input("Name: ")
    email = input("Email (optional): ")
    print("Added user:", User.create(name, email))


def list_users():
    for user in User.all():
        print(user)


def find_project():
    project = Project.find(input("Project title: "))
    if not project:
        raise ValueError("no such project")
    return project


def add_project():
    owner = User.find_by_name(input("Owner name: "))
    if not owner:
        raise ValueError("no such user exists")
    title = input("Project title: ").strip()
    if not title:
        raise ValueError("project title cannot be empty")
    if Project.find(title):
        raise ValueError("a project with that title already exists")
    description = input("Description (optional): ")
    due_date = input("Due date (optional): ").strip() or None
    print("Added project:", Project(owner, title, description, due_date))


def list_projects():
    for project in Project.all():
        print(project)


def list_user_projects():
    user = User.find_by_name(input("User name: "))
    if not user:
        raise ValueError("no such user")
    for project in user.projects:
        print(project)


def add_task():
    project = find_project()
    title = input("Task title: ")
    name = input("Assign to (optional user name): ").strip()
    assignee = None
    if name:
        assignee = User.find_by_name(name)
        if not assignee:
            raise ValueError("no such user")
    task = project.add_task(title, assignee)
    print(f"Added task #{task.id} to '{project.title}'")


def list_tasks():
    project = find_project()
    for t in project.tasks:
        who = t.assigned_to.name if t.assigned_to else "unassigned"
        print(f"#{t.id} {t.title} [{t.status}] - {who}")
    done, total = project.progress
    print(f"{done}/{total} complete")


def complete_task():
    text = input("Task ID: ").strip()
    task = Task.get(int(text)) if text.isdigit() else None
    if not task:
        raise ValueError("no task with that ID")
    task.complete()
    print("Completed:", task)


Menu = {
    "1": ("Add user", add_user),
    "2": ("List users", list_users),
    "3": ("Add project", add_project),
    "4": ("List all projects", list_projects),
    "5": ("List a user's projects", list_user_projects),
    "6": ("Add task", add_task),
    "7": ("List tasks in a project", list_tasks),
    "8": ("Complete task", complete_task),
}


def main():
    storage.load()
    while True:
        print()
        for key, (label, _) in Menu.items():
            print(f"{key}. {label}")
        print("q. Quit")
        choice = input("> ").strip()
        if choice == "q":
            break
        if choice not in Menu:
            print("Invalid choice, try again.")
            continue
        try:
            Menu[choice][1]()
            storage.save()
        except ValueError as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
import pytest
from models import User, Project, Task

@pytest.fixture
def user():
    for cls in (User, Project, Task):
        cls.reset()
    return User.create("victor", "victor@example.com")

def test_user_created(user):
    assert user.id == 1
    assert user.name == "victor"
    assert user.email == "victor@example.com"

def test_project_belongs_to_user(user):
    project = Project(user, "My Project", due_date="Oct 19 2026")
    assert project.owner == user
    assert user.projects == [project]
    assert project.due_date == "2026-10-19"

def test_add_task(user):
    project = Project(user, "My Project")
    task = project.add_task("First task", user)
    assert task.status == "pending"
    assert task.assigned_to == user
    assert project.tasks == [task]



#add_user works
#add project check
#add_task passed
#task update progress fail
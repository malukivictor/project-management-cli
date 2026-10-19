from .base import Entity

project_status = ("pending", "in-progress", "complete")

class Task(Entity):
    def __init__(self, project, title, assigned_to=None, status="pending", entity_id=None):
        self.title = title
        self.status = status
        self.project = project
        self.assigned_to = assigned_to
        super().__init__(entity_id)
        project.tasks.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        value = (value or "").strip()
        if not value:
            raise ValueError("task title cannot be empty")
        self._title = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in project_status:
            raise ValueError(f"status must be one of: {', '.join(project_status)}")
        self._status = value

    @property
    def is_complete(self):
        return self._status == "complete"

    def complete(self):
        self.status = "complete"

    def assign(self, user):
        self.assigned_to = user

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project.id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to.id if self.assigned_to else None,
        }

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title!r}, status={self.status!r})"
    @classmethod
    def from_dict(cls, data, project, assigned_to=None):
        return cls(project, data["title"], assigned_to,
                   data.get("status", "pending"), data["id"])

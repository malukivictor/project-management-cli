from .base import Entity
from .tasks import Task
from dateutil import parser


class Project(Entity):
    def __init__(self, owner, title, description="", due_date=None, entity_id=None):
        self.owner = owner
        self.title = title.strip()
        self.description = description
        self.due_date = due_date
        super().__init__(entity_id)
        self.tasks = []
        owner.projects.append(self)

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        value = (value or "").strip()
        if not value:
            self._due_date = None
            return
        try:
            self._due_date = parser.parse(value).date().isoformat()
        except (ValueError, OverflowError):
            raise ValueError("could not read that date, try 2026-12-01 or 'Dec 1 2026'") from None

    @property
    def progress(self):
        return sum(t.is_complete for t in self.tasks), len(self.tasks)

    @classmethod
    def find(cls, title):
        key = (title or "").strip().lower()
        return next((p for p in cls._registry if p.title.lower() == key), None)

    def add_task(self, title, assigned_to=None):
        return Task(self, title, assigned_to)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.owner.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
        }

    def __str__(self):
        due = self.due_date or "no due date"
        done, total = self.progress
        return f"#{self.id} {self.title} (owner: {self.owner.name}, due: {due}, {done}/{total} done)"
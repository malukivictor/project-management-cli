from .person import Person


class User(Person):
    def __init__(self, name, email="", entity_id=None):
        super().__init__(name, email, entity_id)
        self.projects = []

    @classmethod
    def create(cls, name, email=""):
        if cls.find_by_name(name):
            raise ValueError(f"User with name '{name}' already exists.")
        return cls(name, email)

    @classmethod
    def find_by_name(cls, name):
        key = (name or "").strip().lower()
        return next((u for u in cls._registry if u.name.lower() == key), None)

    def __str__(self):
        email = f" <{self.email}>" if self.email else ""
        return f"#{self.id} {self.name}{email} ({len(self.projects)} projects)"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}
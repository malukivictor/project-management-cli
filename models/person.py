import re
from .base import Entity

email_pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Person(Entity):
    def __init__(self, name, email="", entity_id=None):
        self.name = name
        self.email = email
        super().__init__(entity_id)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        value = (value or "").strip()
        if not value:
            raise ValueError("name cannot be empty.")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        value = (value or "").strip()
        if value and not email_pattern.match(value):
            raise ValueError("Invalid email format.")
        self._email = value
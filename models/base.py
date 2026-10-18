class Entity:
    _next_id = 1
    _registry = []

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls._next_id = 1
        cls._registry = []

    def __init__(self, entity_id=None):
        cls = type(self)
        if entity_id is None:
            entity_id = cls._next_id
        cls._next_id = max(cls._next_id, entity_id + 1)
        self.id = entity_id
        cls._registry.append(self)

    @classmethod
    def all(cls):
        return list(cls._registry)

    @classmethod
    def get(cls, entity_id):
        return next((e for e in cls._registry if e.id == entity_id), None)

    @classmethod
    def reset(cls):
        cls._registry = []
        cls._next_id = 1
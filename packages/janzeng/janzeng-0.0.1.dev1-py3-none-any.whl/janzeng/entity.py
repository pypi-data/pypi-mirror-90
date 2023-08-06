class EntityManager:
    def __init__(self):
        self.entities = []

    def add(self, entity):
        self.entities.append(entity)


entity_manager = EntityManager()


class Entity:
    def __init__(self):
        entity_manager.add(self)

    def update(self, dt):
        pass

    def render(self, surface):
        pass

import pygame

# Set of callbacks registered via decorators
from janzeng.event import PygameEvent
from janzeng.entity import entity_manager


class Game:
    def __init__(self, *, screen_size=(800, 600), fps=60):
        self.screen_width, self.screen_height = self.screen_size = screen_size
        self.fps = fps

        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.background = pygame.Color("black")
        self.dt = 0.0
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(self.fps) / 1000.0
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                ev = PygameEvent(event.type)
                func_name = f"on_{ev.name.lower()}"
                func = getattr(self, func_name, None)
                if func:
                    func(**event.dict)
                for entity in entity_manager.entities:
                    func = getattr(entity, func_name, None)
                    if func:
                        func(**event.dict)

            for entity in entity_manager.entities:
                entity.update(self.dt)

            self.screen.fill(self.background)

            for entity in entity_manager.entities:
                entity.render(self.screen)

            pygame.display.flip()

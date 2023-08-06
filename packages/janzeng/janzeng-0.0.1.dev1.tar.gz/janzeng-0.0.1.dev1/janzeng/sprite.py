from pathlib import Path

import pygame

from janzeng.entity import Entity

PIVOTS = [
    "topleft",
    "topcenter",
    "topright",
    "midleft",
    "center",
    "midright",
    "bottomleft",
    "bottomcenter",
    "bottomright",
]


class Sprite(Entity):
    def __init__(self, *, image, pos, pivot="bottomcenter", alpha=True):
        super().__init__()
        if isinstance(image, Path):
            self.image = pygame.image.load(image)
        elif isinstance(image, str):
            self.image = pygame.image.load(Path(image))
        elif isinstance(image, pygame.Surface):
            self.image = image
        else:
            raise TypeError(f"Image must be Path-object or string, got {type(image)}")
        if alpha:
            self.image = self.image.convert_alpha()
        else:
            self.image = self.image.convert()
        self.pivot = pivot
        self.rect = self.image.get_rect(**{pivot: pos})
        self._position = pygame.Vector2(pos)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        setattr(self.rect, self.pivot, (int(value[0]), int(value[1])))

    def render(self, surface):
        surface.blit(self.image, self.rect)

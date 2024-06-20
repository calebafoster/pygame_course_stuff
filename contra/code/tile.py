import pygame
from pygame.math import Vector2 as vector
import settings as ss

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

class CollisionTile(Tile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups, ss.LAYERS['Level'])
        self.old_rect = self.rect.copy()

class MovingPlatform(CollisionTile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

        self.direction = vector(0,-1)
        self.speed = 200
        self.pos = vector(self.rect.topleft)

    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))


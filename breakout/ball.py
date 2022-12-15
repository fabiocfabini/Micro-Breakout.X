from random import randint

import pygame

from themes import *

class Ball(pygame.sprite.Sprite):    
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.vel_x = randint(-6,6)
        self.vel_y = randint(4,6)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def bounce(self):
        self.vel_y = -self.vel_y + randint(-2,2)
        self.vel_x += randint(-2,2)

        if abs(self.vel_x) < 3:
            if self.vel_x < 0:
                self.vel_x = -3
            else:
                self.vel_x = 3
        if abs(self.vel_y) < 3:
            if self.vel_y < 0:
                self.vel_y = -3
            else:
                self.vel_y = 3
import pygame
import numpy as np

from themes import *

class Paddle(pygame.sprite.Sprite):
    x_rest = 128
    y_rest = 127
    # [-123, -82, -41, 0, 41, 82, 123]
    x_velocities = np.array([-3, -2, -1, 0, 1, 2, 3])*2
    x_ranges = [
        range(-130,-82), range(-82, -41), range(-41, 0),    # Move left
        range(0, 1),                                        # Don't move
        range(1, 41), range(41, 82), range(82, 130)         # Move right
    ]


    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def move(self, x_read: int):
        self.rect.x += self._get_velocity(x_read - self.x_rest)

        self._check_bounds()

    def _get_velocity(self, x_read: int):
        for i, r in enumerate(self.x_ranges):
            if x_read in r:
                return self.x_velocities[i]

    def _check_bounds(self):
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 700:
            self.rect.x = 700

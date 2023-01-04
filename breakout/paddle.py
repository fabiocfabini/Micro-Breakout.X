import pygame
import numpy as np

from themes import *

class Paddle(pygame.sprite.Sprite):
    # Map y_read to x_velocity
    # [-123, -82, -41, 0, 41, 82, 123]
    x_velocities = np.array([-3, -2, -1, 0, 1, 2, 3])*4
    x_ranges = [
        range(-130,-82), range(-82, -41), range(-41, -10),  # Move left
        range(-10, 11),                                     # Don't move
        range(11, 41), range(41, 82), range(82, 130)        # Move right
    ]

    def __init__(self, color, width, height, y_rest):
        super().__init__()

        self.y_rest = y_rest
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def move(self, y_read: int):
        """
        Move the paddle based on the y_read value.
        """
        self.rect.x += self._get_velocity(y_read - self.y_rest)

        # Make sure the paddle doesn't go off the screen
        self._check_bounds()

    def _get_velocity(self, y_read: int):
        """
        Map the y_read value to a velocity.
        """
        for i, r in enumerate(self.x_ranges):
            if y_read in r:
                return self.x_velocities[i]

    def _check_bounds(self):
        """
        Make sure the paddle doesn't go off the screen.
        """
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width

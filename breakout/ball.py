from random import randint

import pygame

from themes import *

class Ball(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player
    controls. It derives from the "Sprite" class in Pygame.
    """
    def __init__(self, color, width, height):
        """
        In the constructor we create the image of the block,
        and fill it with a color.
        """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.vel_x = randint(-6,6)
        self.vel_y = randint(4,6)
        self.rect = self.image.get_rect()

    def update(self):
        """
        Update the position of the ball by adding the velocity to the position.
        """
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def bounce(self):
        """
        This function will bounce the ball off a horizontal surface (not a vertical one)
        """
        # Add a little randomness to the bounce
        self.vel_y = -self.vel_y + randint(-2,2)
        self.vel_x += randint(-2,2)

        # Make sure the ball doesn't go too fast
        if abs(self.vel_x) < 4:
            if self.vel_x < 0:
                self.vel_x = -4
            else:
                self.vel_x = 4
        if abs(self.vel_y) < 4:
            if self.vel_y < 0:
                self.vel_y = -4
            else:
                self.vel_y = 4
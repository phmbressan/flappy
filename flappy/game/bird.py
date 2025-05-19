"""The Bird class for the game containing its state."""

import pygame

from . import BIRD_RADIUS, GRAVITY, HEIGHT, JUMP_STRENGTH, WIDTH


class Bird:
    """A class representing the bird in the Flappy Bird game."""

    def __init__(self):
        """Initialize the bird's position, velocity, and state."""
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.vel = 0
        self.alive = True
        self.score = 0

    def flap(self):
        """Make the bird flap, which gives it an upward velocity."""
        self.vel = JUMP_STRENGTH

    def update(self):
        """Update the bird's position based on its velocity and gravity."""
        self.vel += GRAVITY
        self.y += self.vel
        if self.y < 0 or self.y > HEIGHT:
            self.alive = False

    def draw(self, screen: pygame.Surface):
        """Draw the bird on the screen."""
        pygame.draw.circle(
            screen, (255, 255, 0), (int(self.x), int(self.y)), BIRD_RADIUS
        )

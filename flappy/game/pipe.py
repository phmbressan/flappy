"""A class for the obstacles of the game and collision handling."""

import random
from typing import TYPE_CHECKING

import pygame

from . import GAP_HEIGHT, HEIGHT, PIPE_SPEED, PIPE_WIDTH, WIDTH

if TYPE_CHECKING:
    from .bird import Bird


class Pipe:
    """A class representing a pipe as a game obstacle."""

    def __init__(self, x: int = WIDTH):
        """Initialize the pipe's position and gap height.

        Parameters
        ----------
        x : int
            The x-coordinate of the pipe. Default is the width of the screen.
        """
        self.x = x
        self.pipe_center = random.randint(200, HEIGHT - 200)

    def update(self):
        """Update the pipe's position by moving it to the left."""
        self.x -= PIPE_SPEED

    def draw(self, screen: pygame.Surface):
        """Draw the pipe on the screen.

        Parameters
        ----------
        screen : pygame.Surface
            The screen to draw the pipe on.
        """
        bottom_of_top_pipe = self.pipe_center - GAP_HEIGHT // 2
        top_of_bottom_pipe = self.pipe_center + GAP_HEIGHT // 2
        pygame.draw.rect(
            screen, (0, 255, 0), (self.x, 0, PIPE_WIDTH, bottom_of_top_pipe)
        )
        pygame.draw.rect(
            screen, (0, 255, 0), (self.x, top_of_bottom_pipe, PIPE_WIDTH, HEIGHT)
        )

    def collide(self, bird: "Bird") -> bool:
        """Check if the bird collides with the pipe.

        Parameters
        ----------
        bird : Bird
            The bird object to check for collision with the pipe.

        Returns
        -------
        bool
            True if the bird collides with the pipe, False otherwise.
        """
        in_x = self.x < bird.x < self.x + PIPE_WIDTH
        top_hit = bird.y < self.pipe_center - GAP_HEIGHT // 2
        bottom_hit = bird.y > self.pipe_center + GAP_HEIGHT // 2
        return in_x and (top_hit or bottom_hit)

"""The main game functions for its routine and rendering."""

import sys
from typing import Iterable

import pygame

from . import FPS, HEIGHT, WIDTH
from .bird import Bird
from .pipe import Pipe

font = pygame.font.SysFont(None, 36)


def draw_game(
    screen: pygame.Surface,
    bird: Bird,
    pipes: Iterable[Pipe],
    score: int,
    info: str = "",
):
    """Draw the game state on the screen. The scene is filled with a sky
    color, and the bird and pipes are drawn. The score is displayed at
    the top left corner.

    Parameters
    ----------
    screen : pygame.Surface
        The screen to draw on.
    bird : Bird
        The bird object to draw.
    pipes : Iterable[Pipe]
        An iterable of pipe objects to draw.
    """
    screen.fill((135, 206, 235))
    bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)
    text = font.render(f"Score: {score} {info}", True, (0, 0, 0))
    screen.blit(text, (10, 10))
    pygame.display.flip()


def play_game():
    """Main game loop for playing the game."""
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    score = 0

    while bird.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.flap()

        if pipes[-1].x < WIDTH - 300:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.update()
        pipes = [p for p in pipes if p.x + 60 > 0]

        bird.update()
        if any(p.collide(bird) for p in pipes):
            bird.alive = False

        for pipe in pipes:
            if not hasattr(pipe, "passed") and pipe.x + 60 < bird.x:
                bird.score += 1
                score += 1
                pipe.passed = True

        draw_game(screen, bird, pipes, score, info="You")
        clock.tick(FPS)

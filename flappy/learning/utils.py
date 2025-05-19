"""Utility function for integrating the model with the game."""

from typing import Iterable

import pygame
import torch
from game import GAP_HEIGHT, HEIGHT, WIDTH
from game.bird import Bird
from game.game import draw_game
from game.pipe import Pipe

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
clock = pygame.time.Clock()


def extract_state(bird: Bird, pipe: Pipe) -> torch.Tensor:
    """Extract the state from the bird and pipe objects.

    Parameters
    ----------
    bird : Bird
        The bird object to extract the state from.
    pipe : Pipe
        The pipe object to extract the state from.

    Returns
    -------
    torch.Tensor
        A tensor representing the state of the game.
    """
    return torch.tensor(
        [
            bird.y / HEIGHT,
            bird.vel / 10.0,
            (pipe.x - bird.x) / WIDTH,
            (pipe.pipe_center - GAP_HEIGHT // 2) / HEIGHT,
            (pipe.pipe_center + GAP_HEIGHT // 2) / HEIGHT,
        ],
        dtype=torch.float32,
    ).to(device)


def run_episode(model: torch.nn.Module, render: bool = False) -> tuple:
    """Run a single episode of the game using the given model.

    Parameters
    ----------
    model : torch.nn.Module
        The model to use for making decisions in the game.
    render : bool, optional
        Whether to render the game on the screen. Default is False.

    Returns
    -------
    tuple
        A tuple containing the rewards, log probabilities, and score
        achieved during the episode.
    """
    screen = None
    if render:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    bird = Bird()
    pipes = [Pipe()]
    rewards = []
    log_probs = []

    while bird.alive:
        if pipes[-1].x < WIDTH - 300:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.update()
        pipes = [p for p in pipes if p.x + 60 > 0]

        next_pipe = next((p for p in pipes if p.x + 60 > bird.x), pipes[0])
        state = extract_state(bird, next_pipe)
        prob = model(state)
        m = torch.distributions.Bernoulli(prob)
        action = m.sample()
        log_probs.append(m.log_prob(action))

        if action.item() == 1.0:
            bird.flap()
        bird.update()
        if any(p.collide(bird) for p in pipes):
            bird.alive = False

        reward = 0.1
        for pipe in pipes:
            if not hasattr(pipe, "passed") and pipe.x + 60 < bird.x:
                reward += 10.0
                bird.score += 1
                pipe.passed = True
        rewards.append(reward)

        if render:
            draw_game(screen, bird, pipes, int(bird.score), info="AI")
            clock.tick(60)

    return rewards, log_probs, bird.score


def compute_loss(
    rewards: Iterable[float], log_probs: Iterable[float], gamma: float = 0.99
) -> torch.Tensor:
    """Compute the loss for the model based on the rewards and log
    probabilities.

    Parameters
    ----------
    rewards : Iterable[float]
        An iterable of rewards received during the episode.
    log_probs : Iterable[float]
        An iterable of log probabilities of the actions taken.
    gamma : float, optional
        The discount factor for future rewards. Default is 0.99.

    Returns
    -------
    torch.Tensor
        The computed loss for the model.
    """
    g_value = 0
    returns = []
    for r in reversed(rewards):
        g_value = r + gamma * g_value
        returns.insert(0, g_value)
    returns = torch.tensor(returns).to(device)
    returns = (returns - returns.mean()) / (returns.std() + 1e-9)
    loss = torch.stack([-lp * R for lp, R in zip(log_probs, returns)]).sum()
    return loss

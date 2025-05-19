import argparse

import pygame
import torch
from game.game import play_game
from learning.model import MLPNetwork
from learning.train import train
from learning.utils import run_episode

pygame.init()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def watch_ai(model: torch.nn.Module):
    """Watch the AI play the game.

    Parameters
    ----------
    model : torch.nn.Module
        The trained model to use for playing the game.
    """
    model.eval()
    with torch.no_grad():
        while True:
            run_episode(model, render=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["play", "train", "watch"])
    args = parser.parse_args()

    model = MLPNetwork().to(device)

    if args.mode == "train":
        train(model)
    elif args.mode == "watch":
        model.load_state_dict(torch.load("data/flappy_ai.pt", map_location=device))
        watch_ai(model)
    elif args.mode == "play":
        play_game()

"""Training functions for the network model."""

import torch
import torch.optim as optim

from .utils import compute_loss, run_episode


def train(model, episodes=10_000, lr=1e-3):
    """Train the model using reinforcement learning.

    Parameters
    ----------
    model : torch.nn.Module
        The model to be trained.
    episodes : int, optional
        The number of episodes to train the model. Default is 10,000.
    lr : float, optional
        The learning rate for the optimizer. Default is 0.001.
    """
    optimizer = optim.Adam(model.parameters(), lr=lr)
    best_score = 0
    try:
        for ep in range(episodes):
            rewards, log_probs, score = run_episode(model, render=False)
            loss = compute_loss(rewards, log_probs)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if score > best_score:
                best_score = score
                torch.save(model.state_dict(), "data/flappy_ai.pt")

            if ep % 50 == 0:
                print(f"Episode {ep} | Score: {score} | Best: {best_score}")
    except KeyboardInterrupt:
        print("Training interrupted. Saving model...")
        torch.save(model.state_dict(), "data/flappy_ai.pt")
        print("Model saved.")

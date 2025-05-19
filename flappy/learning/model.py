"""A simple neural network model for reinforcement learning."""

import torch
import torch.nn as nn


class MLPNetwork(nn.Module):
    """A simple neural network model."""

    def __init__(self):
        """Initialize the model with a sequential structure."""
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(5, 32), nn.ReLU(), nn.Linear(32, 1), nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the model.

        Parameters
        ----------
        x : torch.Tensor
            The input tensor.

        Returns
        -------
        torch.Tensor
            The output tensor after passing through the model.
        """
        return self.model(x)

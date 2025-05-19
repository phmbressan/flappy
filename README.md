# Flappy

The repository aims to use Pytorch to use a Multi-Layer Perceptron (MLP) to play the Flappy Bird game. The goal is to train the MLP to learn how to play the game by using reinforcement learning techniques.

## Usage

The main script is `flappy.py`.

Usage:
```bash
    python flappy.py <mode>
```
Mode options:
* `play`  - Launch the game in manual mode for user control.
* `train` - Initiate the training process for the AI model.
* `watch` - Load a pre-trained AI model and watch it play the game autonomously.

## Model
The model is a simple MLP with the following architecture:
- Input layer: 5 neurons (representing the state of the game)
- Hidden layer: 32 neurons
- Output layer: 1 neuron (representing the action to take)
The model uses ReLU activation for the hidden layer and a sigmoid activation for the output layer.

## Results Preview

Training the model for 5000 episodes took about 20 minutes on a standard laptop without GPU acceleration. The model was able to achieve a score of 232 in the game.

| Episode | Score | Best |
|---------|-------|------|
| 1000    | 0     | 0    |
| 2000    | 1     | 1    |
| 3000    | 5     | 12   |
| 4000    | 37    | 67   |
| 5000    | 82    | 232  |

The model weights are saved in the `data` directory (`data/flappy_ai.pt`).

## Sample Execution

Executing the script in `watch` mode with the pre-trained model:

https://github.com/user-attachments/assets/2d21a7a5-f6a2-4099-a9b1-5edf531d444e


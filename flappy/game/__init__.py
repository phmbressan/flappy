import pygame

WIDTH, HEIGHT = 400, 600
PIPE_WIDTH = 60
GAP_HEIGHT = 250
PIPE_SPEED = 2
BIRD_RADIUS = 20
GRAVITY = 0.4
JUMP_STRENGTH = -10
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

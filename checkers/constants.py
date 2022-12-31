import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# frames per second
FPS = 60

# RGB
DARK_BLUE = (0, 0, 51)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (121, 45, 13)
BEIGE = (240, 178, 102)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
GREEN = (25, 102, 25)

CROWN = pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'), (44, 25))

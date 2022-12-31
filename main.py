"""
A game of checkers.
"""

import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, FPS
from checkers.game import Game

# window to display the game
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


def get_col_row_from_mouse(mouse_position: tuple[int, int]) -> tuple[int, int]:
    """
    Function change mouse position on the screen to a field on the board.

    :param mouse_position: tuple contains (x, y) position on the screen
    :return: tuple contains (column, row) position of the field on the board
    """
    x, y = mouse_position
    return x // SQUARE_SIZE, y // SQUARE_SIZE


def run_game(clock: pygame.time.Clock, game: Game) -> None:
    """
    Function managing interaction between the player and the game
    and show the game on the window.
    It will run until player pres Close.

    :param clock: clock for smooth view
    :param game: object managing Checkers game action
    :return: None
    """
    while True:
        clock.tick(FPS)
        # draw game in window
        game.update()

        # if player change anything in the game
        for event in pygame.event.get():
            # if close the window
            if event.type == pygame.QUIT:
                return

            # if click a mouse button on something
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                column, row = get_col_row_from_mouse(position)
                game.select(row, column)


def main():
    """
    Main function to manage all actions to play the game of checkers in window.

    :return: None
    """
    # Initialize the pygame for printing text
    pygame.init()
    # window title caption
    pygame.display.set_caption('Checkers')

    clock = pygame.time.Clock()
    game = Game(WINDOW)

    run_game(clock, game)

    pygame.quit()


if __name__ == '__main__':
    main()

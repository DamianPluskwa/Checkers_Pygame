import pygame.draw

from .constants import WHITE, SQUARE_SIZE, GREY, CROWN, DARK_BLUE, ROWS


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        """
        Calculate position a pawn on board
        :return: None
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        """
        When a pawn is on the last row, it turns into a king piece
        :return:
        """
        if (self.row == ROWS - 1 and self.color == WHITE) or (self.row == 0 and self.color == DARK_BLUE):
            self.king = True

    def draw(self, window):
        """
        Draw a pawn on the board
        :param window: window on the screen
        :return: None
        """
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(window, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        if self.king:
            window.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        """
        Move the pawn to different square
        :param row: new row position
        :param col: new column position
        :return: None
        """
        self.row = row
        self.col = col
        self.calculate_position()

    # for debugging
    def __repr__(self):
        if self.color == WHITE:
            color_name = "WHITE"
        else:
            color_name = "DARK_BLUE"
        color_name += f" ({self.row}, {self.col})"
        return color_name




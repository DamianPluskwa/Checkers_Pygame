"""
File contains class with rules of checkers
"""

import pygame

from checkers.board import Board
from checkers.constants import DARK_BLUE, WHITE, RED, SQUARE_SIZE, GREEN


class Game:
    """
    Class managing the rule of playing a game of checkers
    """
    def __init__(self, window: pygame.Surface):
        self.selected_piece = None
        self.board = Board()
        self.turn = WHITE  # the game starts with white pawns
        self.valid_move = dict()  # valid moves for one piece
        self.all_valid_moves = self.board.get_all_valid_moves(self.turn)  # dictionary of valid moves for all pieces
        self.winner = None
        self.without_capturing_a_pawn = 0  # when over 30 game ends with tie
        self.window = window

    def update(self):
        """
        Draw game on the window.

        :return: None
        """

        self.board.draw(self.window, self.selected_piece)
        self.draw_valid_moves(self.valid_move)
        self.show_winner()
        pygame.display.update()

    def show_winner(self):
        """
        Draw winner on the window if game ends.

        :return: None
        """
        if self.winner is not None:
            font = pygame.font.Font('freesansbold.ttf', 64)
            winner_text = font.render(self.winner, True, RED)
            self.window.blit(winner_text, (200, 350))

    def select(self, row: int, col: int):
        """
        Function manage field on the board selected by the player.
        The function does not allow you to select a field after the game is over.

        :param row: field row on the board
        :param col: field column on the board
        :return: None
        """
        # if game end
        if self.winner:
            return
        # if player selected_piece piece before
        if self.selected_piece:
            # move thad piece in the selected_piece field
            self._move(row, col)

        # if player don't selected_piece piece before
        piece = self.board.get_piece(row, col)
        # if selected_piece piece can be moved by current player
        if piece != 0 and piece.color == self.turn:
            self.selected_piece = piece
            self.valid_move = self.all_valid_moves[piece]

        return

    def _move(self, row, col):
        """
        move the piece on the board if move is valid

        :param row: row on the board
        :param col: column on the board
        :return: None
        """
        piece = self.board.get_piece(row, col)
        if self.selected_piece and piece == 0 and (row, col) in self.valid_move:
            self.board.move(self.selected_piece, row, col)
            skipped = self.valid_move[(row, col)]
            self.without_capturing_a_pawn += 1
            if skipped:
                self.board.remove(skipped)
                self.without_capturing_a_pawn = 0
            self._change_turn()

        return

    def draw_valid_moves(self, moves: dict):
        """
        Draw valid moves for one pawn

        :param moves: list of valid moves for one piece
        :return: None
        """
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, GREEN,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 30)

    def _change_turn(self):
        """
        Change player to opposite and check if game ends.

        :return: None
        """
        self.valid_move = dict()
        self.selected_piece = None
        past_turn = self.turn
        if self.turn == DARK_BLUE:
            self.turn = WHITE
        else:
            self.turn = DARK_BLUE

        self.all_valid_moves = self.board.get_all_valid_moves(self.turn)

        if not self._have_possible_moves():
            if past_turn == DARK_BLUE:
                self.winner = "DARK WON"
            else:
                self.winner = "WHITE WON"

        if self.without_capturing_a_pawn >= 30:
            self.winner = "    TIE"

    def _have_possible_moves(self) -> bool:
        """
        Checking if player have valid moves

        :return: True if player have valid moves, False otherwise.
        """
        can_move = False
        for moves in self.all_valid_moves.values():
            if moves:
                can_move = True
                break

        return can_move

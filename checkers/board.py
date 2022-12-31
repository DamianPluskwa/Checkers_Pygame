"""
The file contains class with board fore game of checkers
"""


import pygame

from checkers.constants import BLACK, ROWS, SQUARE_SIZE, COLS, WHITE, BEIGE, DARK_BLUE, GREEN
from checkers.piece import Piece


class Board:
    """
    Class managing the board for game of checkers
    """
    def __init__(self):
        self.board = []
        self.blue_left = self.white_left = 12
        self.create_board()

    @staticmethod
    def _draw_squares(window: pygame.Surface):
        """
        Draw empty board on the window with game

        :param window: window for printing on the screen
        :return: None
        """
        window.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, BEIGE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    @staticmethod
    def _draw_selected(window: pygame.Surface, selected: Piece):
        """
        Change color under the selected piece

        :param window: window for printing on the screen
        :param selected: Piece selected by Player
        :return: None
        """
        if selected is not None:
            pygame.draw.rect(window, GREEN,
                             (selected.col * SQUARE_SIZE, selected.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece: Piece, row: int, col: int):
        """
        Change position of the piece and make piece a king if is in the end of board

        :param piece: selected piece
        :param row: new row position of the piece
        :param col: new column position of the piece
        :return: None
        """
        # move the piece
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        # making a king piece
        piece.make_king()

    def get_piece(self, row: int, col: int):
        """
        Returns what is on the checking field

        :param row: row of the field
        :param col: column of the
        :return: object on the field
        """
        return self.board[row][col]

    def create_board(self):
        """
        Create piece on board in the start positions
        :return: None
        """
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, DARK_BLUE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, window: pygame.Surface, selected: Piece):
        """
        Drawing board in the window on screen
        :param window: window on the screen
        :param selected: piece selected by player
        :return: None
        """
        self._draw_squares(window)
        self._draw_selected(window, selected)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece.color == DARK_BLUE:
                self.blue_left -= 1
            else:
                self.white_left -= 1

    # return winner or None
    def winner(self):
        """
        Check if player have pieces on the bord, if he isn't return the winner
        :return: None or str with winner
        """
        if self.blue_left <= 0:
            return "WHITE WON"
        elif self.white_left <= 0:
            return "DARK WON"

        return None

    # give all valid moves for eny piece
    def get_valid_moves(self, piece):
        """

        :param piece: piece that wont to make a move
        :return: dict width valid moves
        """
        moves = dict()

        if piece.color == DARK_BLUE:
            moves.update(self._traverse((piece.row, piece.col), (-1, -1), piece))
            moves.update(self._traverse((piece.row, piece.col), (-1, 1), piece))
            moves.update(self._taking_pawn_backwards((piece.row, piece.col), (1, -1), piece))
            moves.update(self._taking_pawn_backwards((piece.row, piece.col), (1, 1), piece))

        if piece.color == WHITE:
            moves.update(self._traverse((piece.row, piece.col), (1, -1), piece))
            moves.update(self._traverse((piece.row, piece.col), (1, 1), piece))
            moves.update(self._taking_pawn_backwards((piece.row, piece.col), (-1, -1), piece))
            moves.update(self._taking_pawn_backwards((piece.row, piece.col), (-1, 1), piece))

        if piece.king:
            moves.update(self._traverse_king_piece(piece, (-1, -1)))
            moves.update(self._traverse_king_piece(piece, (-1, 1)))
            moves.update(self._traverse_king_piece(piece, (1, -1)))
            moves.update(self._traverse_king_piece(piece, (1, 1)))

        # if player can take a pawn
        necessary_moves = dict()
        for move, taking_pawn in moves.items():
            if taking_pawn:
                necessary_moves[move] = taking_pawn

        if necessary_moves:
            return necessary_moves

        return moves

    def get_all_valid_moves(self, turn):
        """
        Getting all the moves possible for a player
        :param turn: which player's turn
        :return: dic with all valid moves for one player
        """
        all_valid_moves = dict()
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == turn:
                    moves = self.get_valid_moves(piece)
                    all_valid_moves[piece] = moves

        have_necessary_move = False
        for piece, moves in all_valid_moves.items():
            for taking_pawn in moves.values():
                if taking_pawn:
                    have_necessary_move = True

        if have_necessary_move:
            for piece, moves in all_valid_moves.items():
                tmp_moves = dict()
                for move, taking_pawn in moves.items():
                    if taking_pawn:
                        tmp_moves[move] = taking_pawn
                all_valid_moves[piece] = tmp_moves

        return all_valid_moves

    def _check_square(self, row: int, column: int):
        """
        Checking what is on the field and return it, if square isn't in the board return None
        :param row: on the board
        :param column: on the board
        :return: None or piece
        """

        # checking if square is in the board
        if row < 0 or row >= 8:
            return None
        if column < 0 or column >= 8:
            return None

        return self.board[row][column]

    #
    def _traverse(self, start_square: tuple, direction: tuple, piece: Piece, taking_pawns=None) -> dict:
        """
        Checking if is possible to move in that direction and return possible moves
        :param start_square: in the board
        :param direction: in which the pawn can move
        :param piece: a piece
        :param taking_pawns: enemy pieces that can by taken
        :return: dict with move in given directions
        """
        if taking_pawns is None:
            taking_pawns = list()
        # create dictionary for possible moves
        move = dict()
        # create mouse_position of checking square
        row, column = start_square[0] + direction[0], start_square[1] + direction[1]
        # checking what is in the square
        checking_square = self._check_square(row, column)

        # if pawn already taken
        if checking_square is piece or checking_square in taking_pawns:
            pass
        # if the square is outside the board
        elif checking_square is None:
            pass
        # if the square is empty
        elif checking_square == 0:
            move[(row, column)] = None
        # if on the square is piece of the same color
        elif checking_square.color is piece.color:
            pass
        # if in the square is pawn of the enemy
        else:
            behind_row, behind_column = row + direction[0], column + direction[1]
            checking_square_behind = self._check_square(behind_row, behind_column)
            if checking_square_behind == 0:
                taking_pawns.append(self.get_piece(row, column))
                move[behind_row, behind_column] = taking_pawns[:]
                move.update(self._traverse_after_taking_a_pawn(piece, (behind_row, behind_column), taking_pawns))

        return move

    def _traverse_after_taking_a_pawn(self, piece: Piece, start_square, taking_pawns: list) -> dict:
        """
        Moving further after taking an enemy pawn
        :param piece: moving piece
        :param start_square: on a board
        :param taking_pawns: list of enemy taken pawns
        :return: dict of valid moves
        """
        moves = dict()

        down_left = (1, -1)
        down_right = (1, 1)
        up_left = (-1, -1)
        up_right = (-1, 1)
        directions = [down_left, down_right, up_left, up_right]

        for direction in directions:
            moves.update(self._traverse(start_square, direction, piece, taking_pawns))

        valid_moves = dict()
        for key, values in moves.items():
            if values is not None:
                valid_moves.update({key: values})

        return valid_moves

    def _traverse_king_piece(self, piece: Piece, direction: tuple) -> dict:
        """
        Possible moves foe a king piece
        :param piece: moving piece
        :param direction: in which the pawn can move
        :return: dict of valid moves for that pawn
        """
        moves = dict()
        run = True
        start_square = (piece.row, piece.col)
        while run:
            move = self._traverse(start_square, direction, piece)
            start_square = (start_square[0] + direction[0], start_square[1] + direction[1])
            moves.update(move)
            if move == {} or None not in move.values():
                run = False

        return moves

    def _taking_pawn_backwards(self, starts_square: tuple, direction: tuple, piece: Piece) -> dict:
        """
        when a pawn can take a enemy pawn backwards
        :param starts_square: of a moving pawn
        :param direction: of a moving pawn
        :param piece: a moving piece
        :return: dict with possible moves
        """
        moves = dict()

        moves.update(self._traverse(starts_square, direction, piece))

        for taking_pawn in moves.values():
            if taking_pawn:
                return moves

        return dict()

    # tests
    def _show_square(self, square):
        if square == 0:
            print('checking_square empty')
        elif square is None:
            print('Outside the board')
        elif square.color == DARK_BLUE:
            print('checking_square Dark Blue')
        elif square.color == WHITE:
            print('checking_square White')

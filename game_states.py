from random import choice


class GameState(object):
    """GameState generic base class.

    This class represents the interface that other game classes must conform to.
    It assumes a two-player game. The players are numbered 0 and 1, with the
    first move always going to player 0. Game results are expected to be in the
    range [0.0, 1.0] representing whether player 0 or 1 is the victor.
    In the case of a draw the result should be 0.5.
    """

    def __init__(self):
        self.next_turn_player = 0

    @property
    def game_result(self):
        return None

    def get_moves(self):
        return set()

    def get_random_move(self):
        moves = self.get_moves()
        return choice(tuple(moves)) if moves != set() else None

    def play_move(self, move):
        pass


class TicTacToeState(GameState):
    """Tic Tac Toe game state.

    An implementation of the rules of tic tac toe. This serves as a simple
    example of a two-player turn-based game to illustrate the mechanics of
    the MCTS algorithm.
    """

    def __init__(self):
        super(TicTacToeState, self).__init__()

        self.board = [ None, ] * 9

    @property
    def game_result(self):
        win_positions  = [[0, 1, 2], [3, 4, 5], [6, 7, 8]] # Horizontal
        win_positions += [[0, 3, 6], [1, 4, 7], [2, 5, 8]] # Vertical
        win_positions += [[0, 4, 8], [2, 4, 6]] # Diagonal

        for pos in win_positions:
            if self.board[pos[0]] == self.board[pos[1]] == self.board[pos[2]] \
              and self.board[pos[0]] is not None:

              return self.board[pos[0]]

        if all([pos is not None for pos in self.board]): # Draw
            return 0.5

        return None

    def get_moves(self):
        return set({i for i in xrange(len(self.board))
            if self.board[i] is None})
    
    def play_move(self, move):
        assert self.board[move] is None

        self.board[move] = self.next_turn_player
        self.next_turn_player = 1 - self.next_turn_player

    def __repr__(self):
        s = ''
        for i in xrange(9):
            if self.board[i] is None:
                s += '.'
            else:
                s += ('O', 'X')[self.board[i]]

            s += '\n' if i % 3 == 2 else ' '
        return s

class ConnectFourGameState(GameState):
    """Connect Four Game State.

    Implements the classic children's game of "Connect Four". Players alternate
    dropping coloured discs into a grid-shaped frame from above until one player
    forms a row, column or diagonal of four discs.
    """
    def __init__(self, board_width=7, board_height=6):
        super(ConnectFourGameState, self).__init__()

        assert board_width > 3
        assert board_height > 3

        self.board_width, self.board_height = board_width, board_height
        self.board = [ None, ] * (board_width * board_height)

    def get_cell(self, x, y):
        return self.board[y * self.board_width + x]

    def set_cell(self, x, y, state):
        self.board[y * self.board_width + x] = state

    @property
    def game_result(self):
        def check_segment(segment):
            for cell in segment:
                if cell is None or cell != segment[0]:
                    return None
            return segment[0]

        # Rows
        def row_segment(x, y):
            return [self.get_cell(x + dx, y) for dx in xrange(4)]

        for x in xrange(0, self.board_width - 4 + 1):
            for y in xrange(0, self.board_height):
                segment_result = check_segment(row_segment(x, y))
                if segment_result is not None:
                    return segment_result

        # Columns
        def column_segment(x, y):
            return [self.get_cell(x, y + dy) for dy in xrange(4)]

        for x in xrange(0, self.board_width):
            for y in xrange(0, self.board_height - 4 + 1):
                segment_result = check_segment(column_segment(x, y))
                if segment_result is not None:
                    return segment_result

        # Forward Diagonals (i.e. like forward slash /)
        def forward_diagonal_segment(x, y):
            return [self.get_cell(x + delta, y + 3 - delta)
                for delta in xrange(4)]

        # Back Diagonals (i.e. like back slash \)
        def back_diagonal_segment(x, y):
            return [self.get_cell(x + delta, y + delta)
                for delta in xrange(4)]

        for x in xrange(0, self.board_width - 4 + 1):
            for y in xrange(0, self.board_height - 4 + 1):
                segment_result = check_segment(forward_diagonal_segment(x, y))
                if segment_result is not None:
                    return segment_result

                segment_result = check_segment(back_diagonal_segment(x, y))
                if segment_result is not None:
                    return segment_result

        # Draw if the board got filled without any winner
        return 0.5 if self.get_moves() == set() else None

    def get_moves(self):
        return set(x for x in xrange(self.board_width)
            if self.get_cell(x, 0) is None)

    def play_move(self, x):
        # A move in connect 4 is an x ordinate specifying which column to drop
        # the disc in from above. Thus we scan from the bottom up for the first
        # empty cell.
        for y in xrange(self.board_height - 1, -1, -1):
            if self.get_cell(x, y) is None:
                self.set_cell(x, y, self.next_turn_player)
                self.next_turn_player = 1 - self.next_turn_player
                return

        assert False # TODO: should raise InvalidMoveException

    def __repr__(self):
        s = ''
        for y in xrange(self.board_height):
            for x in xrange(self.board_width):
                if self.get_cell(x, y) is None:
                    s += '.'
                else:
                    s += ('O', 'X')[self.get_cell(x, y)]
                s += ' '
            s += '\n'
        return s

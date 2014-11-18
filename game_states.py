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
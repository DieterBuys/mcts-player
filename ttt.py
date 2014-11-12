from random import choice
from time import clock


class GameState(object):
	@property
	def game_over(self):
		return True

	def get_moves(self):
		return []

	def play_move(self, move):
		return self


class TicTacToeState(GameState):
	def __init__(self):
		self.board = [ None, ] * 9
		self.next_turn_player = 0

	@property
	def game_over(self):
		win_positions  = [[0, 1, 2], [3, 4, 5], [6, 7, 8]] # Horizontal
		win_positions += [[0, 3, 6], [1, 4, 7], [2, 5, 8]] # Verical
		win_positions += [[0, 4, 8], [2, 4, 6]] # Diagonal

		for pos in win_positions:
			if self.board[pos[0]] == self.board[pos[1]] == self.board[pos[2]] \
			  and self.board[pos[0]] is not None:
			  return True

		if all([p is not None for p in self.board]): # Draw
			return True

		return False

	def get_moves(self):
		assert not self.game_over

		valid_moves = []
		for move_cell in enumerate(self.board):
			if move_cell[1] is None:
				valid_moves.append(move_cell[0])
		return valid_moves
	
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

# ----- #

class GameController(object):
	def __init__(self, game_state):
		self.game_state = game_state

	def get_next_move(self):
		assert not self.game_state.game_over


class RandomGameController(GameController):
	def get_next_move(self):
		super(RandomGameController, self).get_next_move()
		return choice(self.game_state.get_moves())

# ----- #

class MCTSNode(object):
	def __init__(self):
		self.plays = 0
		self.wins = 0

		self.children = []

class MCTSGameController(GameController):
	def __init__(self, game_state):
		super(MCTSGameController, self).__init__(game_state)
		self.game_tree = MCTSNode()
	
	def select_child_ucb(self):
		pass

	def get_next_move(self, time_allowed=0.5):
		super(MCTSGameController, self).get_next_move()

		# Repeat while there is time
		start_time = clock()
		while clock() < start_time + time_allowed:
			# Select
			child = self.select_child_ucb()

			# Expand
			# Simulate
			# Update
			pass
		
		return choice(self.game_state.get_moves())

# ----- #

def main():
	ttts = TicTacToeState()
	players = (MCTSGameController(ttts), RandomGameController(ttts))

	while not ttts.game_over:
		next_move = players[ttts.next_turn_player].get_next_move()
		ttts.play_move(next_move)
	
		print ttts


if __name__ == '__main__':
	main()

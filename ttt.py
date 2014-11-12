import math
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
	def __init__(self, parent=None):
		self.state = None
		self.move = None

		self.plays = 0
		self.wins = 0

		self.parent = parent
		self.children = []
		self.pending_moves = []

	def select_child_ucb(self):
		def ucb(child):
			win_ratio = child.wins / child.plays \
			    + math.sqrt(2 * math.log(self.plays) / child.plays)

		return max(self.children, key=ucb)

	def expand_move(self, move):
		assert move in self.pending_moves
		self.pending_moves = [m for m in pending_moves if m != move]

		child_state = deepcopy(self.state)
		child_state.play_move(move)
		child_state.pending_moves = child_state.get_moves()

		child = MCTSNode(parent=self, move=move)

class MCTSGameController(GameController):
	def __init__(self, game_state):
		super(MCTSGameController, self).__init__(game_state)
		self.game_tree = MCTSNode()

	# ----- #

	def select(self):
		node = self.game_tree

		# Descend until we find a node that has pending moves, or is terminal
		while node.pending_moves == [] and node.children != []:
			node = self.game_tree.select_child_ucb()

		return node
	
	def expand(self, node):
		return node # choice(node.children).move

	def simulate(self):
		pass

	def update(self):
		pass

	# ----- #
	
	def get_next_move(self, time_allowed=0.5):
		super(MCTSGameController, self).get_next_move()

		# Repeat while there is time
		start_time = clock()
		while clock() < start_time + time_allowed:

			# Select based on UCB
			node = self.select()

			# Expand a child at random
			if node.children != []:
				node = self.expand()

			# Simulate until we reach a terminal state
			result = self.simulate()

			# Update (propagate results up the tree)
			self.update(node, result)

		# Return most visited node's move
		# return max(self.game_tree.children, key=lambda n: n.plays)
		return choice(self.game_state.get_moves())

# ----- #

def random_play():
	ttts = TicTacToeState()
	players = (MCTSGameController(ttts), RandomGameController(ttts))

	while not ttts.game_over:
		next_move = players[ttts.next_turn_player].get_next_move()
		ttts.play_move(next_move)
	
		print ttts

def sequenced_play():
	ttts = TicTacToeState()
	players = (MCTSGameController(ttts), RandomGameController(ttts))

	moves = [4, 2, 6, 1, 0, 3, 8] # Player 0 wins

	for move in moves:
		print 'Player %s\n' % ttts.next_turn_player
		ttts.play_move(move)

		print ttts

def main():
	sequenced_play()


if __name__ == '__main__':
	main()

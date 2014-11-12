import math
from random import choice
from time import clock
from copy import deepcopy


class GameState(object):
	# TODO: Convert from predicate into a value in the set {-1, 0, 1}
	@property
	def game_over(self):
		return True

	def get_moves(self):
		return set()

	def get_random_move(self):
		moves = self.get_moves()
		return choice(tuple(moves)) if moves != set() else None

	def play_move(self, move):
		pass


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

# ----- #

class GameController(object):
	def __init__(self, game_state):
		self.game_state = game_state

	def get_next_move(self):
		assert not self.game_state.game_over


class RandomGameController(GameController):
	def get_next_move(self):
		super(RandomGameController, self).get_next_move()
		return choice(tuple(self.game_state.get_moves()))

# ----- #

class MCTSNode(object):
	def __init__(self, state, parent=None, move=None):
		self.parent = parent
		self.move = move
		self.state = state

		self.plays = 0
		self.wins = 0

		self.pending_moves = state.get_moves()
		self.children = []

	def select_child_ucb(self):
		# Note that each node's plays count is equal
		# to the sum of its children's plays
		def ucb(child):
			win_ratio = child.wins / child.plays \
			    + math.sqrt(2 * math.log(self.plays) / child.plays)

		return max(self.children, key=ucb)

	def expand_move(self, move):
		self.pending_moves.remove(move) # raises KeyError

		child_state = deepcopy(self.state)
		child_state.play_move(move)

		child = MCTSNode(state=child_state, parent=self, move=move)
		self.children.append(child)
		return child

	def __repr__(self):
		s = 'ROOT\n' if self.parent is None else ''

		children_moves = [c.move for c in self.children]

		s += """Win ratio: {wins} / {plays}
Pending moves: {pending_moves}
Children's moves: {children_moves}
State:
{state}\n""".format(children_moves=children_moves, **self.__dict__)

		return s


class MCTSGameController(GameController):
	def __init__(self, game_state):
		super(MCTSGameController, self).__init__(game_state)
		self.root_node = MCTSNode(game_state)

	# ----- #

	def select(self):
		node = self.root_node

		# Descend until we find a node that has pending moves, or is terminal
		while node.pending_moves == [] and node.children != []:
			node = self.root_node.select_child_ucb()

		return node
	
	def expand(self, node):
		assert node.pending_moves != []

		move = choice(tuple(node.pending_moves))
		return node.expand_move(move)

	def simulate(self, state, max_iterations=1000):
		move = state.get_random_move()
		while move is not None:
			state.play_move(move)
			move = state.get_random_move()

			max_iterations -= 1
			if max_iterations <= 0:
				return 0.5 # raise exception?

		return state.game_over # state.game_result
		
	def update(self, node, result):
		while node.parent is not None:
			# TODO: Update result based on each node's point of view
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
			if node.pending_moves != []:
				node = self.expand()

			# Simulate until we reach a terminal state
			result = self.simulate(node.state)

			# Update (propagate results up the tree)
			self.update(node, result)

		# Return most visited node's move
		return max(self.root_node.children, key=lambda n: n.plays).move

# ----- #

def test_play():
	ttts = TicTacToeState()
	players = (MCTSGameController(ttts), RandomGameController(ttts))

	while not ttts.game_over:
		next_move = players[ttts.next_turn_player].get_next_move()
		ttts.play_move(next_move)
	
		print ttts

def state_sequence():
	ttts = TicTacToeState()
	moves = [4, 2, 6, 1, 0, 3, 8] # Player 0 wins

	for move in moves:
		print 'Player %s\n' % ttts.next_turn_player
		ttts.play_move(move)

		print ttts

def test_steps():
	root = MCTSNode(TicTacToeState())

	print root
	root.expand_move(4)
	print root
	root.expand_move(1)
	print root

def main():
	test_steps()


if __name__ == '__main__':
	main()

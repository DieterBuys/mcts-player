import math
from random import choice
from time import clock
from copy import deepcopy
from collections import defaultdict


class GameState(object):
	# The players are 0 and 1. Player 0 always moves first.
	# Game results are in the range 0-1 accordingly with 0.5 for a draw.

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
	def __init__(self):
		super(TicTacToeState, self).__init__()

		self.board = [ None, ] * 9

	@property
	def game_result(self):
		win_positions  = [[0, 1, 2], [3, 4, 5], [6, 7, 8]] # Horizontal
		win_positions += [[0, 3, 6], [1, 4, 7], [2, 5, 8]] # Verical
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

# ----- #

class GameController(object):
	def get_next_move(self, state):
		assert state.game_result is None


class RandomGameController(GameController):
	def get_next_move(self, state):
		super(RandomGameController, self).get_next_move(state)
		return choice(tuple(state.get_moves()))

# ----- #

class MCTSNode(object):
	def __init__(self, state, parent=None, move=None):
		self.parent = parent
		self.move = move
		self.state = state

		self.plays = 0
		self.score = 0

		self.pending_moves = state.get_moves()
		self.children = []

	def select_child_ucb(self):
		# Note that each node's plays count is equal
		# to the sum of its children's plays
		def ucb(child):
			win_ratio = child.score / child.plays \
			    + math.sqrt(2 * math.log(self.plays) / child.plays)

		return max(self.children, key=ucb)

	def expand_move(self, move):
		self.pending_moves.remove(move) # raises KeyError

		child_state = deepcopy(self.state)
		child_state.play_move(move)

		child = MCTSNode(state=child_state, parent=self, move=move)
		self.children.append(child)
		return child

	def get_score(self, result):
		if result == 0.5:
			return result

		if self.state.next_turn_player == result:
			return 0.0
		else:
			return 1.0

	def __repr__(self):
		s = 'ROOT\n' if self.parent is None else ''

		children_moves = [c.move for c in self.children]

		s += """Score ratio: {score} / {plays}
Pending moves: {pending_moves}
Children's moves: {children_moves}
State:
{state}\n""".format(children_moves=children_moves, **self.__dict__)

		return s


class MCTSGameController(GameController):
	def select(self):
		node = self.root_node

		# Descend until we find a node that has pending moves, or is terminal
		while node.pending_moves == set() and node.children != []:
			node = node.select_child_ucb()

		return node
	
	def expand(self, node):
		assert node.pending_moves != set()

		move = choice(tuple(node.pending_moves))
		return node.expand_move(move)

	def simulate(self, state, max_iterations=1000):
		state = deepcopy(state)

		move = state.get_random_move()
		while move is not None:
			state.play_move(move)
			move = state.get_random_move()

			max_iterations -= 1
			if max_iterations <= 0:
				return 0.5 # raise exception? (game too deep to simulate)

		return state.game_result
		
	def update(self, node, result):
		while node is not None:
			node.plays += 1
			node.score += node.get_score(result)
			node = node.parent

	# ----- #
	
	def get_next_move(self, state, time_allowed=1.0):
		super(MCTSGameController, self).get_next_move(state)

		# Create new tree (TODO: Preserve some state for better performance?)
		self.root_node = MCTSNode(state)

		iterations = 0

		# Repeat while there is time
		start_time = clock()
		while clock() < start_time + time_allowed:
			# Select based on UCB
			node = self.select()

			# Expand a child at random
			if node.pending_moves != set():
				node = self.expand(node)

			# Simulate until we reach a terminal state
			result = self.simulate(node.state)

			# Update (propagate results up the tree)
			self.update(node, result)

			iterations += 1

		# Return most visited node's move
		return max(self.root_node.children, key=lambda n: n.plays).move

# ----- #

def test_play():
	players = (MCTSGameController(), RandomGameController())

	results = defaultdict(int)
	for game_number in xrange(1, 101):
		ttts = TicTacToeState()

		while ttts.game_result is None:
			next_move = players[ttts.next_turn_player].get_next_move(ttts)
			ttts.play_move(next_move)

		print game_number, ttts.game_result
		results[ttts.game_result] += 1

	print results


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
	test_play()


if __name__ == '__main__':
	main()

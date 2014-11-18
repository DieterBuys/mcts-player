from collections import defaultdict

from game_states import GameState, TicTacToeState
from game_controllers import RandomGameController, MCTSGameController, MCTSNode

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

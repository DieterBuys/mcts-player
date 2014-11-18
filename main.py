import argparse
from collections import defaultdict

from game_states import GameState, TicTacToeState
from game_controllers import RandomGameController, MCTSGameController, MCTSNode


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

def test_play(trials=100):
    players = (MCTSGameController(), RandomGameController())

    results = defaultdict(int)
    for game_number in xrange(1, trials+1):
        ttts = TicTacToeState()

        while ttts.game_result is None:
            next_move = players[ttts.next_turn_player].get_next_move(ttts)
            ttts.play_move(next_move)

        print game_number, ttts.game_result
        results[ttts.game_result] += 1

    print results

def main():
    parser = argparse.ArgumentParser(description='Monte-Carlo Tree Search AI Player')
    parser.add_argument('trials', type=int, help='The number of trials to conduct.')
    parser.add_argument('turn_limit', type=float, help='The time allowed for the AI to take each turn, in seconds.')

    # TODO: Play according to the parameters from the command line
    # args = parser.parse_args()
    test_play(5)


if __name__ == '__main__':
    main()
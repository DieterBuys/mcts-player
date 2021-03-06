# Monte Carlo Tree Search

## About
This is a pure-Python implementation of the Monte Carlo Tree Search algorithm for two-player turn-based games. It can play arbitrary games, as long as the valid moves and win conditions are specified.

Currently it can play Tic Tac Toe. 

## Usage

```
[~]> python main.py
```

## References
This work is based on the UCT variant of the [Monte Carlo Tree Search](http://en.wikipedia.org/wiki/Monte_Carlo_tree_search) algorithm. MCTS was popularized in 2006 by [this seminal paper](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.81.6817) by R. Coulom entitled "Efficient Selectivity and backup operators in Monte-Carlo tree search". The UCT algorithm, which involves deploying the "bandit" UCB1 selection strategy in combination with MCTS is due to [this paper](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.102.1296) by L. Kocsis and C. Szepesvári.

## License
This code is distributed under the MIT license.
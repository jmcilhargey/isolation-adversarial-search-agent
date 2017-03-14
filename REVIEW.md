### AlphaGo by the DeepMind Team

[Mastering the game of Go with deep neural networks and tree search](https://storage.googleapis.com/deepmind-media/alphago/AlphaGoNaturePaper.pdf)

### Overview

Developing a functional AI for the game of Go has posed a significant challenge due to the number of moves and difficulty of evaluating positions. Prior efforts have only been able to develop rudimentary AI capable of playing at a novice level. In this seminal paper, the AlphaGo team at Google Deepmind were able to achieve a significant breakthrough in game playing intelligence. Using a combination of deep neural networks and tree searching algorithms, they create an AI agent capable of playing Go at a professional skill level and beat the European Go champion 5 games to 0.

Go is a game played on a 19 by 19 board where the objective is to fully surround a larger area of the board than the opponent. The size of the board and the number of pieces on it creates an astronomically large search space of 250^150. With the number of moves far exceeding the atoms in the universe, traditional methods to exhaustively search the board are impossible. The AlphaGo team used a combination of methods to dramatically reduce the search space. First, they were able to truncate certain game subtrees with an approximation function. Second, they were able to reduce the breadth of the search tree by selecting specific actions according to a policy, which is a probability distribution of all actions for the current game state.

### Monto Carlo Tree Method

A key method described in the paper is Monte Carlo tree search (MCTS). In MCTS, a potential move is chosen at random and then that action is played out to the final game result. Based on the result, the nodes touched during the MCTS rollout have their probability updated, making them more or less likely to be picked for the next MCTS selection. Because of the built-in randomness of a Monte Carlo approach, the game tree will expand as more rounds are sampled, while at the same time building up preference for moves that lead to a positive result for the AI.

### Neural Network and Training

Another hallmark of the team’s approach is use of neural networks for speed and performance improvements in evaluating positions. This is done with a convolutional neural network that represents the board position as a 19 by 19 image that contains the representation of a board position. The neural network is trained through several stages of machine learning. The team begins by conducting supervised training using moves played by human experts to developer a supervised learning (SL) policy. They also train a fast policy that’s necessary for the MCTS rollouts. Then they train a reinforcement learning (RL) policy that builds on the SL policy by having the AI play games against itself and optimizing routes that lead to victory. Finally a value network is trained which predicts the winner of games where the RL network plays against itself. The completed program combines the policy and value networks with the MCTS technique.

### Search Algorithm

The paper goes into great detail about the methods and mathematical models used to approach the problem. Here is a short overview of the core search algorithm. The search algorithm stores statistics for each edge that contains prior probability, Monte Carlo estimates, leaf evaluations, and rollout rewards. Actions are selected using a variation of the PUCT algorithm. When a leaf node is added to a queue for evaluation, the simulation starts at the leaf and continues until the game end and the outcome is computed from the final game score. As the simulation proceeds, the rollout statistics are updated so that the program doesn’t sample identical game variations. When the visit count for a node exceeds a defined threshold, the state is initialized using a tree policy to provide prior probabilities and the position is inserted into a queue for further evaluation. The algorithm itself is run on an architechture where a single master machine executes the main search, remote CPUs execute the async rollouts, and remote worker GPUs execute policy and value network operations.

### Recap

The game of Go and the achievements of AlphaGo outlined in this paper show the progress of AI in areas of decision making with large intractable search spaces when finding an optimal solution seems infeasible. Breakthroughs in MCTS, partial and classical planning, scheduling, constraint satisfaction and other areas enabled the team to combine tree search policy and value networks to achieve a professional level performance in Go.

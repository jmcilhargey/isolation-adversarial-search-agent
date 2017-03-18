
## Intro

After implementing the minimax algorithm with alpha-beta pruning and iterative deepening, the next task is to find an effective evaluation function. Because minimax picks the least or greatest score each round, we’re looking for a scoring heuristic that calculates a win condition for our player.

We want to maximize our player's moves and minimize the opponent’s moves so we start with a basic formula for the evaluation function, taking the difference of player and opponent moves. With this as our baseline, we implement three other functions and compare their performance.

Note that time spent in the evaluation function reduces time that can be spent exploring the game tree. For this reason, it’s generally considered to keep the evaluation function simple and within linear or constant time.

## Methods

One method is to count the number of open spaces on the board as a measure of the game’s progress and use this in the evaluation function. If the board is open, we can play aggressively and when we reach the endgame, our player can become more defensive. This relationship is represented in the `calc_move_diff_with_spaces` function.

Another approach is to consider a move’s distance from the center. We know that the further a move is from the center, the fewer available moves there are around it. For instance, the center of the board has 8 possible moves, while the corners have 2 possible moves. This method is implemented in `calc_move_diff_from_center`.

A third strategy is to change the mathematical relationship between the number of opponent and player moves. Instead of taking the difference of player and opponent moves, the ratio of the moves is taken. This heuristic favors moves with larger differences between player and opponent moves and is implemented in the `calc_ratio_of_moves` method.

## Evaluation Function Data

The test script `tournament.py` was used to measure the performance of the three evaluation functions against the baseline function. In the tables below, the total percentage of games won against opponents is used as a measure of the evaluation function performance. The first set of games is played using the baseline function and the second with the alternate heuristic.

#### calc_move_diff_with_spaces

| Opponent  | Baseline W to L | Implemented W to L |
| ------------- | :---: | :---: |
| Random | 18 to 2 | 17 to 3 |
| MM_Null | 17 to 3 | 18 to 2 |
| MM_Open | 10 to 10 | 12 to 8 |
| MM_Improved | 10 to 10 | 14 to 6 |
| AB_Null | 9 to 11 | 19 to 1 |
| AB_Open | 10 to 10 | 15 to 5 |
| AB_Improved | 14 to 6 | 14 to 6 |

Baseline _**62.86%**_, Implemented _**77.14%**_

#### calc_ratio_of_moves

| Opponent  | Baseline W to L | Implemented W to L |
| ------------- | :---: | :---: |
| Random | 16 to 4 | 18 to 2 |
| MM_Null | 17 to 3 | 11 to 9 |
| MM_Open | 5 to 15 | 13 to 7 |
| MM_Improved | 12 to 8 | 12 to 8 |
| AB_Null | 16 to 4 | 14 to 6 |
| AB_Open | 11 to 9 | 13 to 7 |
| AB_Improved | 11 to 9 | 16 to 4 |

Baseline _**62.86%**_, Implemented _**69.29%**_

#### calc_move_diff_from_center

| Opponent  | Baseline W to L | Implemented W to L |
| ------------- | :---: | :---: |
| Random | 18 to 2 | 18 to 2 |
| MM_Null | 13 to 7 | 18 to 2 |
| MM_Open | 7 to 13 | 10 to 10|
| MM_Improved | 15 to 5  | 9 to 11 |
| AB_Null | 12 to 8 | 15 to 5 |
| AB_Open | 9 to 11 | 12 to 8 |
| AB_Improved | 13 to 7 | 12 to 8 |

Baseline _**62.14%**_, Implemented _**67.14%**_

## Discussion

With the baseline as a control, we see that the heuristic using board spaces has the highest success rate overall. Using this custom heuristic results in a roughly 15% improvement from the baseline. 

The results demonstrate that across different types of scoring methods, `calc_move_diff_with_spaces` consistently achieves a higher win rate. For example, the MM (minimax) and AB(alpha-beta) opponents using the baseline heuristic won less games than `calc_move_diff_with_spaces`, by an average of ~3 games per every 20 played. 

If we monitor the search on a move-by-move basis, we see the iterative search depth for `calc_move_diff_with_spaces` is on average greater than the others. Because less processing is done within the function, there is more time available to search deeply in the tree, which in turn leads to better win rate overall.

For the reasons discussed, `calc_move_diff_with_spaces` is the most effective heuristic developed in the project.

Further experimentation could be done by changing the constant values on the scoring variables and adding an opening book of moves. Some basic testing was done by altering the leading constants in the heuristic. For example, a 2 : 1 ratio for the player constant with respect to the opponent constant leads to a slight improvement ~5% in the win rate for `calc_move_diff_with_spaces`.

Additional efforts could also focus on combine the techniques from each of the heuristics to see if there is an improvement in win rate when a combination of factors are used.

Isolation is an excellent model for exploring the challenges presented by artifical intelligence. Because of the large search space, effective solutions must make use of techniques like minimax, alpha-beta pruning, and iterative deepening to find optimal moves and play intelligently. In this project an efficient and effective program was developed to play the game at human-level performance. 

# Connect-4 AI Agent

## Introduction
Connect 4 is a zero-sum and decision-making game, a fundamental approach to solving this type of game is a game-tree search. We are going to implement the AI agent using minimax algorithm, which is a game-tree search algorithm, to tackle the game of connect 4. We are also going to show how adding alpha-beta pruning to the normal minimax algorithm can improve the efficiency of computation without chaning the value of minimax algorithm's result.

## State Representation
- The board state is represented as a 64-bit number.
- Each column takes 9 bits as follows:
-- 3 bits show the index of first empty row (000 indicate full column, while 110 indicate empty column).
-- 6 bits show the board discs (0 is for AI, 1 for human).

- An empty state would be represented as follows:
0 110000000 110000000 110000000 110000000 110000000 110000000 110000000

## Helper Functions
### Count Consecutive Pieces
#### Checking for vertical pieces:
The algorithm checks for N-consecutive pieces in all columns. An N-consecutive pieces is valid in two cases (as illustrated in the following image and explained below):
- N is 4, so no extra plays are required to connect 4 discs.
- The 4-N cells above the N-consecutive pieces are empty, so possible moves can lead to a 4-consecutive pieces.

<center><img src="img/Vertical-Checks.png?raw=true" alt="Vertical Check" width="150"/></center>

#### Checking for horizontal pieces:
The algorithm checks for all permutations of size 4 containing N pieces and 4-N empty cells. Refer to the following image for an example of different permutations of N=3.
<center><img src="img/Horizontal-Checks.png?raw=true" alt="Horizontal Check" width="150"/></center>



#### Checking for diagonal pieces:
The algorithm finds all different 24 diagonals of the 6x7 board game. It follows a similar approach like the horizontal pieces checker to give score to diagonals that contain 4-connected discs or have possible move(s) that can lead to a 4-connected discs.


## Evaluation Function
We designed a heuristic function that evaluates the state of a game and returns a number indicating whether the computer is near to win or lose and truncate the game tree after K levels evaluating the states using the heuristic function.

The evaluation function depends on the following key factors:
##### Attacking
- Number of 4-consecutive discs placed by AI (Score: 100)
- Number of 3-consecutive discs placed by AI (Score: 10)
- Number of 2-consecutive discs placed by AI (Score: 5)
##### Defending
- Number of 4-consecutive discs placed by Human (Score: 100)
- Number of 3-consecutive discs placed by Human (Score: 30)
- Number of 2-consecutive discs placed by Human (Score: 10)

The evaluation function result is the difference between Human score and AI score.

## Notes
- For simplicity, we performed all development and tests using a board with dimension of seven columns and six rows.
- The complete game tree for Connect Four has over 4.5 trillion different boards.
- Alpha-beta pruning does not change the value of the minimax algorithm's result; it only changes the efficiency of the computation.

## References
- [OEIS - The Online Encyclopedia for Integer Sequences](https://oeis.org/A212693)
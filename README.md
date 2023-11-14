# Connect4 AI Agent
Using Minimax Algorithm to Make Connect 4 AI Agent

## State Representation
- The board state is represented as a 64-bit number.
- Each column takes 9 bits as follows:
-- 3 bits show the index of first empty row (000 indicate full column, while 110 indicate empty column).
-- 6 bits show the board discs (0 is for AI, 1 for human).

- An empty state would be represented as follows:
0 110000000 110000000 110000000 110000000 110000000 110000000 110000000

## Evaluation Function
The evaluation function depends on the following key factors:
- Number of 4-consecutive discs placed by AI (Score: 10)
- Number of 3-consecutive discs placed by AI (Score: 10)
- Number of 2-consecutive discs placed by AI (Score: 10)
- Number of 4-consecutive discs placed by Human (Score: 10)
- Number of 3-consecutive discs placed by Human (Score: 2)
- Number of 2-consecutive discs placed by Human (Score: 1)

The score is calculated as: ai_score - human_score
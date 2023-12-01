import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from algorithms.minimax_ab_pruning import MinimaxAlphaBeta
from algorithms.minimax import Minimax
from utils import *
import random
from heuristics import count_consecutive_pieces
import time

if __name__ == '__main__':
    TEST_GAMES = 10
    DEPTH = 2
    DEPTH_2 = 4
    DEBUG = False
    ALGORITHM = 0 # 0: Minimax, 1: Minimax with Alpha-Beta Pruning
    games = []
    times_taken = []
    total_nodes = []
    for i in range(TEST_GAMES):
        start_time = time.time()
        bitboard = 0b0110000000110000000110000000110000000110000000110000000110000000  # Empty Board

        for j in range(21):
            if ALGORITHM == 0:
                solver = Minimax(bitboard, DEPTH, True)
            else:
                solver = MinimaxAlphaBeta(bitboard, DEPTH, True)
            changed_root, root, number_of_nodes_expanded = solver.solve()
            total_nodes.append(number_of_nodes_expanded)
            bitboard = MAKE_MOVE(bitboard, changed_root, 0)
            DEBUG and print(j, 'BEST MOVE', changed_root, root.score)
            # Random Play:
            move = random.choice(GET_POSSIBLE_MOVES(bitboard))
            bitboard = MAKE_MOVE(bitboard, move, 1)
            DEBUG and print(f'RANDOM MOVE: {move}')
        
        end_time = time.time()
        DEBUG and print_board(bitboard)
        ai_score = count_consecutive_pieces(bitboard, 'AI', 4)
        human_score = count_consecutive_pieces(bitboard, 'Human', 4)
        ai_score_sum = ai_score['vertical'] + ai_score['horizontal'][0] + ai_score['horizontal'][1] + ai_score['diagonal'][0] + ai_score['diagonal'][1]
        human_score_sum = human_score['vertical'] + human_score['horizontal'][0] + human_score['horizontal'][1] + human_score['diagonal'][0] + human_score['diagonal'][1]
        games.append(['AA' if ai_score_sum > human_score_sum else 'RR' if ai_score_sum < human_score_sum else 'TT', ai_score_sum, human_score_sum, sum(total_nodes) / len(total_nodes)])
        times_taken.append(end_time - start_time)
        print(f'Game {i+1} completed in {end_time - start_time} seconds', 'AA' if ai_score_sum > human_score_sum else 'RR' if ai_score_sum > human_score_sum else 'TT', ai_score_sum, human_score_sum, sum(total_nodes) / len(total_nodes))

    AA_wins = len([game for game in games if game[0] == 'AA'])
    RR_wins = len([game for game in games if game[0] == 'RR'])
    TT_wins = len([game for game in games if game[0] == 'TT'])
    print(f'{AA_wins} : {RR_wins} : {TT_wins}')
    print('W/L', AA_wins / RR_wins) if RR_wins != 0 else print('W/L', AA_wins)
    print('Average Nodes Expanded:', round(sum([game[3] for game in games]) / len(games), 2))
    if [game for game in games if game[0] == 'TT']:
        print('W/T Ratio:', len([game for game in games if game[0] == 'AA']) / len([game for game in games if game[0] == 'TT']))
    print('Average Time Taken:', round(sum(times_taken) / len(times_taken), 5))
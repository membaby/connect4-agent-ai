from algorithms.minimax_ab_pruning import MinimaxAlphaBeta
from algorithms.minimax import Minimax
from utils import *
import random
from heuristics import count_consecutive_pieces
import time

if __name__ == '__main__':
    TEST_GAMES = 20
    DEPTH = 3
    DEPTH_2 = 4
    DEBUG = False
    ALGORITHM = 1 # 0: Minimax, 1: Minimax with Alpha-Beta Pruning
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
            changed_root, root, path, number_of_nodes_expanded = solver.solve()
            total_nodes.append(number_of_nodes_expanded)
            bitboard = MAKE_MOVE(bitboard, changed_root, 0)
            DEBUG and print(j, 'BEST MOVE', changed_root, root.score)
            # Random Play:
            move = random.choice(GET_POSSIBLE_MOVES(bitboard))
            bitboard = MAKE_MOVE(bitboard, move, 1)
            DEBUG and print(f'RANDOM MOVE: {move}')
            # solver = MinimaxAlphaBeta(bitboard, DEPTH_2, True)
            # changed_root, root_, path_, number_of_nodes_expanded_ = solver.solve()
            # bitboard = MAKE_MOVE(bitboard, changed_root, 1)
        
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

# TEST CERTAIN MOVE

    # bitboard = 0b0110000000110000000110000000110000000110000000110000000110000000 # Empty Board
    # bitboard = MAKE_MOVE(bitboard, 0, 1)
    # bitboard = MAKE_MOVE(bitboard, 0, 1)
    # bitboard = MAKE_MOVE(bitboard, 0, 1)
    # bitboard = MAKE_MOVE(bitboard, 1, 1)
    # bitboard = MAKE_MOVE(bitboard, 2, 1)
    # bitboard = MAKE_MOVE(bitboard, 3, 1)
    # # bitboard = MAKE_MOVE(bitboard, 1, 1)
    # # bitboard = MAKE_MOVE(bitboard, 2, 1)
    # # bitboard = MAKE_MOVE(bitboard, 3, 1)
    # # bitboard = MAKE_MOVE(bitboard, 4, 1)
    # # bitboard = MAKE_MOVE(bitboard, 5, 1)
    # # bitboard = MAKE_MOVE(bitboard, 6, 1)
    # print_board(bitboard, True)
    
    # start_time = time.time()
    # solver = MinimaxAlphaBeta(bitboard, 5, True)
    # changed_root, root, path = solver.solve()
    # end_time = time.time()
    # print(changed_root, root.score)
    # start_time = time.time()
    # solver = Minimax(bitboard, 5, True)
    # changed_root, root, path = solver.solve()
    # end_time = time.time()
    # print(changed_root, root.score)
    # # bitboard = MAKE_MOVE(bitboard, changed_root, 0)
    # # print_board(bitboard, True)
    # # print('Time Taken:', end_time - start_time)
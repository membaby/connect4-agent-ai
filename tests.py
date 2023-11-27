from algorithms.minimax_ab_pruning import MinimaxAlphaBeta
from algorithms.minimax import Minimax
from utils import *
import random
from heuristics import count_consecutive_pieces
import time

if __name__ == '__main__':
    TEST_GAMES = 100
    DEPTH = 3
    DEBUG = False
    ALGORITHM = 0 # 0: Minimax, 1: Minimax with Alpha-Beta Pruning
    games = []
    times_taken = []
    for i in range(TEST_GAMES):
        start_time = time.time()
        bitboard = 0b0110000000110000000110000000110000000110000000110000000110000000  # Empty Board

        for i in range(21):
            if ALGORITHM == 0:
                solver = Minimax(bitboard, DEPTH, True)
            else:
                solver = MinimaxAlphaBeta(bitboard, DEPTH, True)
            changed_root, root, path = solver.solve()
            bitboard = MAKE_MOVE(bitboard, changed_root, 0)
            DEBUG and print(i, 'BEST MOVE', changed_root, root.score)
            # Random Play:
            move = random.choice(GET_POSSIBLE_MOVES(bitboard))
            bitboard = MAKE_MOVE(bitboard, move, 1)
            DEBUG and print(f'RANDOM MOVE: {move}')
        
        end_time = time.time()
        DEBUG and print_board(bitboard)
        ai_score = count_consecutive_pieces(bitboard, 'AI', 4)
        human_score = count_consecutive_pieces(bitboard, 'Human', 4)
        games.append(['AA' if ai_score > human_score else 'RR' if ai_score > human_score else 'TT', ai_score, human_score])
        times_taken.append(end_time - start_time)

    print('AA wins', len([game for game in games if game[0] == 'AA']))
    print('RR wins', len([game for game in games if game[0] == 'RR']))
    print('TT wins', len([game for game in games if game[0] == 'TT']))
    if [game for game in games if game[0] == 'TT']:
        print('W/T Ratio:', len([game for game in games if game[0] == 'AA']) / len([game for game in games if game[0] == 'TT']))
    print('Average Time Taken:', sum(times_taken) / len(times_taken))

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
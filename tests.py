from algorithms.minimax_ab_pruning import MinimaxAlphaBeta
from algorithms.minimax import Minimax
from utils import *
import random
from heuristics import count_consecutive_pieces

if __name__ == '__main__':
    TEST_GAMES = 100
    DEPTH = 3
    DEBUG = False
    ALGORITHM = 1 # 0: Minimax, 1: Minimax with Alpha-Beta Pruning
    games = []
    for i in range(TEST_GAMES):
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
            
        DEBUG and print_board(bitboard)
        ai_score = count_consecutive_pieces(bitboard, 'AI', 4)
        human_score = count_consecutive_pieces(bitboard, 'Human', 4)
        games.append(['AA' if ai_score > human_score else 'RR' if ai_score > human_score else 'TT', ai_score, human_score])

    print('AA wins', len([game for game in games if game[0] == 'AA']))
    print('RR wins', len([game for game in games if game[0] == 'RR']))
    print('TT wins', len([game for game in games if game[0] == 'TT']))
    if [game for game in games if game[0] == 'TT']:
        print('W/T Ratio:', len([game for game in games if game[0] == 'AA']) / len([game for game in games if game[0] == 'TT']))
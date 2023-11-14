import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import *
from tree_node import TreeNode
from heuristics import heuristic_evaluation

# # Minimax algorithm
class Minimax:
    def __init__(self, bitboard, max_depth, maximizing_player):
        self.current_bitboard = bitboard
        self.max_depth = max_depth
        self.maximizing_player = maximizing_player
        self.path = {bitboard}
    
    def generate_minimax_tree(self, depth, bitboard, maximizing_player):
        if depth == 0 or IS_GAME_OVER(bitboard): # BASE CASE
            return TreeNode(bitboard, depth, maximizing_player, heuristic_evaluation(bitboard))

        node = TreeNode(bitboard, depth, maximizing_player)

        if maximizing_player:
            max_eval = float('-inf')
            for col in GET_POSSIBLE_MOVES(bitboard):
                new_board = MAKE_MOVE(bitboard, col, self.maximizing_player)
                child_node = self.generate_minimax_tree(depth-1, new_board, False)
                node.children.append(child_node)
                max_eval = max(max_eval, child_node.score)
                self.path.add(new_board)
            node.score = max_eval
            return node

        else:
            min_eval = float('inf')
            for col in GET_POSSIBLE_MOVES(bitboard):
                new_board = MAKE_MOVE(bitboard, col, not self.maximizing_player)
                child_node = self.generate_minimax_tree(depth-1, new_board, True)
                node.children.append(child_node)
                min_eval = min(min_eval, child_node.score)
                self.path.add(new_board)
            node.score = min_eval
            return node
        
    def solve(self):
        root = self.generate_minimax_tree(self.max_depth, self.current_bitboard, self.maximizing_player)
        return root, self.path
    

if __name__ == '__main__':
    bitboard = 0b0110000000110000000110000000110000000110000000110000000110000000  # Empty Board

    bitboard = MAKE_MOVE(bitboard, 0, 1)
    bitboard = MAKE_MOVE(bitboard, 1, 0)
    bitboard = MAKE_MOVE(bitboard, 1, 1)
    bitboard = MAKE_MOVE(bitboard, 2, 0)
    bitboard = MAKE_MOVE(bitboard, 2, 1)
    bitboard = MAKE_MOVE(bitboard, 2, 0)
    bitboard = MAKE_MOVE(bitboard, 2, 1)
    bitboard = MAKE_MOVE(bitboard, 3, 0)
    bitboard = MAKE_MOVE(bitboard, 3, 1)
    bitboard = MAKE_MOVE(bitboard, 3, 0)
    bitboard = MAKE_MOVE(bitboard, 3, 1)
    bitboard = MAKE_MOVE(bitboard, 4, 0)
    bitboard = MAKE_MOVE(bitboard, 4, 1)
    bitboard = MAKE_MOVE(bitboard, 4, 0)
    bitboard = MAKE_MOVE(bitboard, 4, 1)
    bitboard = MAKE_MOVE(bitboard, 4, 0)
    bitboard = MAKE_MOVE(bitboard, 5, 1)
    bitboard = MAKE_MOVE(bitboard, 5, 0)
    bitboard = MAKE_MOVE(bitboard, 5, 1)
    bitboard = MAKE_MOVE(bitboard, 5, 0)
    bitboard = MAKE_MOVE(bitboard, 5, 1)
    bitboard = MAKE_MOVE(bitboard, 5, 0)

    print('(MOVE: N) (SCORE: 000) CUR BOARD:', bin(bitboard))

    best_move_score = float("-inf")
    worst_move_score = float("inf")
    best_move_node = None
    worst_move_node = None

    for move in GET_POSSIBLE_MOVES(bitboard):
        new_bitboard = MAKE_MOVE(bitboard, move, 1)
        MinimaxAlpha = Minimax(new_bitboard, 5, True)
        root, path = MinimaxAlpha.solve()
        best_move_score = max(best_move_score, root.score)
        best_move_node = root if best_move_score == root.score else best_move_node
        worst_move_score = min(worst_move_score, root.score)
        worst_move_node = root if worst_move_score == root.score else worst_move_node
        print(f'(MOVE: {move}) (SCORE: {root.score}) NEW BOARD:', bin(new_bitboard))
    print('BEST MOVE SCORE:', best_move_score)
    print('WORST MOVE SCORE:', worst_move_score)
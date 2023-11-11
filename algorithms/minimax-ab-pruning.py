from utils import *
from more_utils import TreeNode, IS_GAME_OVER, CAN_MAKE_MOVE, MAKE_MOVE
from heuristics import heuristic_evaluation

class MinimaxAlphaBeta:
    def __init__(self, bitboard, max_depth, maximizing_player):
        self.current_bitboard = bitboard
        self.max_depth = max_depth
        self.maximizing_player = maximizing_player
        self.path = {bitboard}
        self.alpha = float("-inf")
        self.beta = float("inf")

    def generate_minimax_tree(self, depth, bitboard, alpha, beta, maximizing_player):
        if depth == 0 or IS_GAME_OVER(bitboard): # BASE CASE
            return TreeNode(bitboard, depth, heuristic_evaluation(bitboard))
        
        node = TreeNode(bitboard, depth)

        if maximizing_player:
            max_score = float("-inf")
            for column in range(7):
                if CAN_MAKE_MOVE(bitboard, column):
                    new_bitboard = MAKE_MOVE(bitboard, column, self.player)
                    child_node = self.generate_minimax_tree(depth-1, new_bitboard, alpha, beta, False)
                    node.children.append(child_node)
                    max_score = max(max_score, child_node.score)
                    self.alpha = max(alpha, child_node.score)
                    if (self.beta <= self.alpha):
                        break
            node.score = max_score
            return node
        else:
            min_score = float("inf")
            for column in range(7):
                if CAN_MAKE_MOVE(bitboard, column):
                    new_bitboard = MAKE_MOVE(bitboard, column, not self.player)
                    child_node = self.generate_minimax_tree(depth-1, new_bitboard, alpha, beta, True)
                    node.children.append(child_node)
                    min_score = min(min_score, child_node.score)
                    self.beta = min(beta, child_node.score)
                    if (self.beta <= self.alpha):
                        break
            node.score = min_score
            return node
        
    def solve(self):
        root = self.generate_minimax_tree(self.max_depth, self.current_bitboard, self.alpha, self.beta, self.maximizing_player)
        return root
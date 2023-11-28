from utils import *
from tree_node import TreeNode
from heuristics import heuristic_evaluation

class MinimaxAlphaBeta:
    def __init__(self, bitboard, max_depth, maximizing_player):
        self.current_bitboard = bitboard
        self.max_depth = max_depth
        self.maximizing_player = maximizing_player
        self.path = {bitboard}
        self.alpha = float("-inf")
        self.beta = float("inf")
        self.expanded_nodes = 0

    def generate_minimax_tree(self, depth, bitboard, alpha, beta, maximizing_player, parent):
        if depth == 0 or IS_GAME_OVER(bitboard):  # BASE CASE
            return TreeNode(bitboard, depth, heuristic_evaluation(bitboard), maximizing_player, parent)

        node = TreeNode(bitboard, depth, None, maximizing_player, parent)
        self.expanded_nodes += 1

        if maximizing_player:
            max_score = float("-inf")
            for column in GET_POSSIBLE_MOVES(bitboard):
                new_bitboard = MAKE_MOVE(bitboard, column, 0)
                child_node = self.generate_minimax_tree(depth-1, new_bitboard, alpha, beta, False, node)
                node.children.append(child_node)
                max_score = max(max_score, child_node.score)
                alpha = max(alpha, max_score)
                self.path.add(new_bitboard)
                if beta <= alpha:
                    break
            node.score = max_score
            return node
        else:
            min_score = float("inf")
            for column in GET_POSSIBLE_MOVES(bitboard):
                new_bitboard = MAKE_MOVE(bitboard, column, 1)
                child_node = self.generate_minimax_tree(depth-1, new_bitboard, alpha, beta, True, node)
                node.children.append(child_node)
                min_score = min(min_score, child_node.score)
                beta = min(beta, min_score)
                self.path.add(new_bitboard)
                if beta <= alpha:
                    break
            node.score = min_score
            return node

    def solve(self):
        root = self.generate_minimax_tree(self.max_depth, self.current_bitboard, self.alpha, self.beta, self.maximizing_player, None)
        max_child = root.children[0]
        for child in root.children:
            if child.score > max_child.score:
                max_child = child
        changed_column = GET_CHANGED_COLUMN(root.bitboard, max_child.bitboard)
        return changed_column, root, self.path, self.expanded_nodes
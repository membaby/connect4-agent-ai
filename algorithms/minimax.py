from utils import *
from tree_node import TreeNode
from heuristics import heuristic_evaluation

class Minimax:
    def __init__(self, bitboard, max_depth, maximizing_player):
        self.current_bitboard = bitboard
        self.max_depth = max_depth
        self.maximizing_player = maximizing_player
        self.path = {bitboard}

    def generate_minimax_tree(self, depth, bitboard, maximizing_player, parent):
        if depth == 0 or IS_GAME_OVER(bitboard):  # BASE CASE
            return TreeNode(bitboard, depth, heuristic_evaluation(bitboard), maximizing_player, parent)

        node = TreeNode(bitboard, depth, None, maximizing_player, parent)

        if maximizing_player:
            max_eval = float('-inf')
            for col in GET_POSSIBLE_MOVES(bitboard):
                new_board = MAKE_MOVE(bitboard, col, 0)
                ##problem
                child_node = self.generate_minimax_tree(depth - 1, new_board, False, node)
                node.children.append(child_node)
                max_eval = max(max_eval, child_node.score)
                # if max_eval==eval:
                # what happens if max_eval==eval ?!?!?!?!?!?!?!?
                ###problem
                self.path.add(new_board)
            node.score = max_eval
            return node

        else:
            min_eval = float('inf')
            for col in GET_POSSIBLE_MOVES(bitboard):
                new_board = MAKE_MOVE(bitboard, col, 1)
                ##problem
                child_node = self.generate_minimax_tree(depth - 1, new_board, True, node)
                node.children.append(child_node)
                min_eval = min(min_eval, child_node.score)
                # if min_eval==eval:
                # what happens if min_eval==eval ?!?!?!?!?!?!?!?
                ##problem
                self.path.add(new_board)
            node.score = min_eval
            return node

    def solve(self):
        root = self.generate_minimax_tree(self.max_depth, self.current_bitboard, self.maximizing_player, None)
        max_child = root.children[0]
        for child in root.children:
            if child.score >= max_child.score:
                max_child = child
        changed_column = GET_CHANGED_COLUMN(root.bitboard, max_child.bitboard)
        return changed_column, root, self.path
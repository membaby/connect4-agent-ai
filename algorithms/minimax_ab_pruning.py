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

    def generate_minimax_tree(self, depth, bitboard, alpha, beta, maximizing_player, parent):
        if depth == 0 or IS_GAME_OVER(bitboard):  # BASE CASE
            return TreeNode(bitboard, depth, heuristic_evaluation(bitboard), maximizing_player, parent)

        node = TreeNode(bitboard, depth, heuristic_evaluation(bitboard), maximizing_player, parent)

        if maximizing_player:
            max_score = float("-inf")
            for column in range(7):
                if CAN_MAKE_MOVE(bitboard, column):
                    new_bitboard = MAKE_MOVE(bitboard, column, self.maximizing_player)
                    child_node = self.generate_minimax_tree(depth - 1, new_bitboard, alpha, beta, False, bitboard)
                    node.children.append(child_node)
                    max_score = max(max_score, child_node.score)
                    self.alpha = max(alpha, child_node.score)
                    self.path.add(new_bitboard)
                    if self.beta <= self.alpha:
                        break
            node.score = max_score
            return node
        else:
            min_score = float("inf")
            for column in range(7):
                if CAN_MAKE_MOVE(bitboard, column):
                    new_bitboard = MAKE_MOVE(bitboard, column, not self.maximizing_player)
                    child_node = self.generate_minimax_tree(depth - 1, new_bitboard, alpha, beta, True, bitboard)
                    node.children.append(child_node)
                    min_score = min(min_score, child_node.score)
                    self.beta = min(beta, child_node.score)
                    self.path.add(new_bitboard)
                    if self.beta <= self.alpha:
                        break
            node.score = min_score
            return node

    def solve(self):
        root = self.generate_minimax_tree(self.max_depth, self.current_bitboard, self.alpha, self.beta, self.maximizing_player, None)
        max_child = root.children[0]
        for child in root.children:
            if child.score >= max_child.score:
                max_child = child
        changed_column = GET_CHANGED_COLUMN(root.bitboard, max_child.bitboard)
        return changed_column, root, self.path

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
        MinimaxAlpha = MinimaxAlphaBeta(new_bitboard, 7, True)
        root, path = MinimaxAlpha.solve()
        best_move_score = max(best_move_score, root.score)
        best_move_node = root if best_move_score == root.score else best_move_node
        worst_move_score = min(worst_move_score, root.score)
        worst_move_node = root if worst_move_score == root.score else worst_move_node
        print(f'(MOVE: {move}) (SCORE: {root.score}) NEW BOARD:', bin(new_bitboard))
    print('BEST MOVE SCORE:', best_move_score)
    print('WORST MOVE SCORE:', worst_move_score)
import graphviz

class TreeNode:
    def __init__(self, bitboard, depth, score, is_maximizing_player, parent):
        self.data = None
        self.bitboard = bitboard
        self.depth = depth
        self.is_maximizing_player = is_maximizing_player
        self.children = []
        self.score = score
        self.parent = parent

    def visualize_tree(self, node, graph=None):
        if graph is None:
            graph = graphviz.Digraph(comment='Minimax Tree')

        graph.node(str(id(node)), label=str(node.bitboard)+', '+str(node.score))

        for child in node.children:
            graph.edge(str(id(node)), str(id(child)))
            self.visualize_tree(child, graph)

        return graph
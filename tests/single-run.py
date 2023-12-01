import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from algorithms.minimax_ab_pruning import MinimaxAlphaBeta
from algorithms.minimax import Minimax
from utils import *
import time

DEPTH = 2
ALGORITHM = 1       # 0 for Minimax, 1 for Minimax with Alpha-Beta Pruning
INITIAL_BOARD = [   # 0 for AI, 1 for Human, 2 for Empty
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2],
]
bitboard = array_to_bitboard(INITIAL_BOARD)

if ALGORITHM == 0: solver = Minimax(bitboard, DEPTH, True)
else: solver = MinimaxAlphaBeta(bitboard, DEPTH, True)

start_time = time.time()
changed_root, root, nodes_expanded = solver.solve()
end_time = time.time()

print()
print('Initial Board:', bin(bitboard))
print(f'[+] Method: {"Minimax" if ALGORITHM == 0 else "Minimax with Alpha-Beta Pruning"}')
print(f"[+] Time taken: {end_time - start_time}")
print(f"[+] Nodes expanded: {nodes_expanded}")
print(f'[+] Best Play: column #{changed_root}')
print(f'[+] Best Score: {root.score}')
d = root.visualize_tree(root)
d.render('minimax_tree', format='pdf', cleanup=True)
print('[+] Minimax Tree visualization saved to minimax_tree.pdf')
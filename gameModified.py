import pygame
import sys
import random
import math
import time
import utils
import tree_node
from algorithms.minimax import Minimax
from algorithms.minimax_ab_pruning import MinimaxAlphaBeta

# Constants
ROWS = 6
COLS = 7
PLAYER_TURN = 0
AI_TURN = 1
PLAYER_PIECE = 1
AI_PIECE = 2

BLUE = (0, 0, 255)
GRAY = (233, 233, 233)
DARK_BLUE = (51, 54, 82)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

SQUARESIZE = 100
SIDEBAR_WIDTH = 390
WIDTH = COLS * SQUARESIZE + SIDEBAR_WIDTH
HEIGHT = (ROWS + 1) * SQUARESIZE
CIRCLE_RADIUS = int(SQUARESIZE / 2 - 5)
SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SIZE)
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 40

# Global variables
player_score = 0
ai_score = 0
other_data = 0
K = 0
METHOD = None

class GameTree:
    def __init__(self, screen, node_radius=20):
        self.screen = screen
        self.node_radius = node_radius
        self.font = pygame.font.SysFont(None, 30)
        self.node_color = DARK_BLUE
        self.hovered_node = None
        self.node_positions = {}  # Store positions of all nodes
        self.edge_color = (255, 255, 255)
        self.last_click_time = 0
        self.double_click_delay = 200  # Adjust this value as needed (in milliseconds)
        self.state_rendered = False
        self.rendered_node = None
        self.root_node = None
        self.main_game = MainGame()  # TODO call method (get_board(bitboard))

    def draw_tree(self, root_node, root_position, spacing):
        if not root_node:
            print("No nodes provided.")
            return
        self.root_node = root_node
        node_positions = {}
        root_position[0] = root_position[0] + 40
        self._draw_node(root_position, root_node)
        root_position[0] = root_position[0] - 40
        node_positions[root_node] = root_position
        self._draw_child_nodes(root_position, root_node.children, spacing, 1)
        self.draw_options(root_position, root_node.is_maximizing_player)
        if self.rendered_node:
            self.render_state(self.rendered_node)

    def draw_options(self, root_position, is_min):
        min_max_text_position = (root_position[0] + 75, root_position[1] - 20)
        min_max_text = None
        if is_min:
            min_max_text = self.font.render("MIN NODE", True, RED)
        else:
            min_max_text = self.font.render("MAX NODE", True, DARK_BLUE)

        self.screen.blit(min_max_text, min_max_text_position)

    def render_state(self, node):
        position = ((COLS + 0.5) * SQUARESIZE, (ROWS - 2) * SQUARESIZE + 25)
        text = self.font.render(f"State: {node.bitboard}", True, DARK_BLUE)
        self.screen.blit(text, position)

    def _draw_node(self, position, node):
        x, y = position
        pygame.draw.circle(self.screen, self.node_color, (x, y), self.node_radius * 1.25)

        text = self.font.render(str(node.score), True, (255, 255, 255))
        text_width, text_height = self.font.size(str(node.score))
        text_position = (x - text_width // 2, y - text_height // 2)
        self.screen.blit(text, text_position)

    def _draw_child_nodes(self, parent_position, nodes, spacing, level):
        if not nodes:
            return

        current_x = parent_position[0] - spacing[0] / 2 * (len(nodes) - 1) / 1.5

        for node in nodes:
            x = current_x
            y = parent_position[1] + level * spacing[1] * 1.5

            self._draw_node((int(x), int(y)), node)
            self.node_positions[node] = (x, y)

            # Draw an edge to the parent node
            line_position = (parent_position[0] + 40, parent_position[1] + 25)
            pygame.draw.line(self.screen, self.edge_color, line_position, (x, y - 25))

            current_x += spacing[0]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if x < 700 and y < 230:
                    return
                for node, position in self.node_positions.items():
                    dx = x - position[0]
                    dy = y - position[1]
                    distance = (dx ** 2 + dy ** 2) ** 0.5
                    if distance < self.node_radius * 1.25:
                        self.hovered_node = node
                        # TODO convert bitboard into 2D board
                        #  self.main_game.draw_board(board)
                        break
                else:
                    self.hovered_node = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered_node:
                    if event.button == 1:  # Left mouse button (single-click)
                        self.rendered_node = self.hovered_node
                        self.state_rendered = True
                        current_time = pygame.time.get_ticks()
                        if current_time - self.last_click_time < self.double_click_delay:
                            # Double-click event
                            self.last_click_time = 0
                            print(f"Double-clicked on {self.hovered_node.score}")
                            spacing = (55, 55)
                            root_position = [COLS * SQUARESIZE + SIDEBAR_WIDTH / 2 - 50, 3 * SQUARESIZE]
                            self.draw_tree(self.hovered_node, root_position, spacing)
                        else:
                            # Single-click event
                            self.last_click_time = current_time


class Button:
    def __init__(self, font, text, x, y, width, height):
        self.font = font
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, color):
        # Draw the rounded rectangle
        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        # Calculate text position to center it within the button
        text_render = self.font.render(self.text, 1, WHITE)
        text_width, text_height = text_render.get_size()
        text_position = (
            self.rect.x + (self.rect.width - text_width) // 2,
            self.rect.y + (self.rect.height - text_height) // 2
        )

        # Draw the text
        screen.blit(text_render, text_position)


class Sidebar:
    def __init__(self, font):
        self.font = font
        self.tree_button = Button(font, "Show Game Tree", COLS * SQUARESIZE + 10,
                                  150, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.reset_button = Button(font, "Reset", (COLS + 2.47) * SQUARESIZE, 150, BUTTON_WIDTH/1.5, BUTTON_HEIGHT)
        self.my_font = pygame.font.SysFont("monospace", 25, bold=True)
        self.data_font = pygame.font.SysFont("monospace", 20, bold=True)
        self.graph_shown = False
        self.game_tree = GameTree(SCREEN)
        self.tree = None  # TODO get from miniMax

    def draw(self):
        player_score_text = self.my_font.render(f"Player Score: {player_score}", 1, DARK_BLUE)
        ai_score_text = self.my_font.render(f"AI Score: {ai_score}", 1, DARK_BLUE)
        nodes_expanded = self.data_font.render(f"Nodes Expanded: {other_data}", 1, DARK_BLUE)
        time = self.data_font.render(f"Time: {other_data}", 1, DARK_BLUE)

        # Sidebar rectangle
        pygame.draw.rect(SCREEN, GRAY, (COLS * SQUARESIZE, 0, SIDEBAR_WIDTH, HEIGHT))

        SCREEN.blit(player_score_text, (COLS * SQUARESIZE + 10, 50))
        SCREEN.blit(nodes_expanded, (COLS * SQUARESIZE + 20, 630))
        SCREEN.blit(time, (COLS * SQUARESIZE + 20, 660))
        SCREEN.blit(ai_score_text, (COLS * SQUARESIZE + 10, 100))

        self.tree_button.draw(SCREEN, DARK_BLUE)
        self.reset_button.draw(SCREEN, RED)
        if self.graph_shown:
            spacing = (55, 55)
            root_position = [COLS * SQUARESIZE + SIDEBAR_WIDTH / 2 - 50, 3 * SQUARESIZE]
            self.game_tree.draw_tree(self.tree, root_position, spacing)
            x, y = pygame.mouse.get_pos()
            if x > 700 and y > 230:
                self.game_tree.handle_events()
            # self.tree = self.game_tree.root_node

class MainGame:
    def __init__(self):
        utils.initialize_board()
        self.board = utils.current_numboard
        self.game_over = False
        self.not_over = True
        self.turn = random.randint(PLAYER_TURN, AI_TURN)
        self.my_font = pygame.font.SysFont("monospace", 20, bold=True)
        # Draw initial GUI
        self.draw_board(self.board)
        pygame.display.update()
        self.bitboard = utils.current_bitboard
        self.miniMax = Minimax(self.bitboard, K, True)
        self.miniMaxAlphaBeta = MinimaxAlphaBeta(self.bitboard, K, True)

    def reset_data(self):
        K = 0
        ai_score = 0
        player_score = 0
        other_data = 0
        METHOD = None
        K = input(".:Enter K: ")
        METHOD = input(".:Enter Method\n1. Without Alpha Beta\n2. With Alpha Beta\n")
        K = int(K)
        METHOD = int(METHOD)
        utils.initialize_board()
        self.board = utils.current_numboard
        self.draw_board(self.board)

    # TODO convert board into our state
    def draw_board(self, board):
        for c in range(COLS):
            for r in range(ROWS):
                pygame.draw.rect(SCREEN, DARK_BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                if board[r][c] == utils.EMPTY:
                    pygame.draw.circle(SCREEN, GRAY, (
                        int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                       CIRCLE_RADIUS)
                elif board[r][c] == utils.HUMAN:
                    pygame.draw.circle(SCREEN, RED, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                                     int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), CIRCLE_RADIUS)
                else:
                    pygame.draw.circle(SCREEN, YELLOW, (
                        int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                       CIRCLE_RADIUS)

        pygame.display.update()

    def run(self):
        while not self.game_over:
            sidebar.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # Clicks on the sidebar
                if event.type == pygame.MOUSEBUTTONDOWN and K > 0:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if sidebar.tree_button.rect.collidepoint(mouse_x, mouse_y):
                        sidebar.graph_shown = True
                    elif sidebar.reset_button.rect.collidepoint(mouse_x, mouse_y):
                        self.reset_data()
                        break

                # Show the moving part
                if event.type == pygame.MOUSEMOTION and not self.game_over:
                    pygame.draw.rect(SCREEN, GRAY, (0, 0, WIDTH - SIDEBAR_WIDTH, SQUARESIZE))
                    xpos = pygame.mouse.get_pos()[0]
                    if self.turn == PLAYER_TURN and xpos < (COLS - 0.5) * SQUARESIZE:
                        pygame.draw.circle(SCREEN, RED, (xpos, int(SQUARESIZE / 2)), CIRCLE_RADIUS)

                # Add Piece
                xpos = pygame.mouse.get_pos()[0]
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over and xpos < COLS * SQUARESIZE and K > 0:
                    pygame.draw.rect(SCREEN, GRAY, (0, 0, WIDTH - SIDEBAR_WIDTH, SQUARESIZE))
                    if self.turn == PLAYER_TURN:
                        xpos = event.pos[0]
                        col = int(math.floor(xpos / SQUARESIZE))

                        if utils.is_valid_move(col):
                            utils.make_move(col, utils.HUMAN)

                        self.board = utils.current_numboard
                        self.draw_board(self.board)
                        self.turn += 1
                        self.turn = self.turn % 2

                if utils.is_game_over():
                    self.game_over = True

            if self.turn == AI_TURN and not self.game_over:
                # tree = None
                # path = None
                # if METHOD == 1:
                #     tree, path = self.miniMax.solve()
                # else:
                #     tree, path = self.miniMaxAlphaBeta.solve()
                #
                # #  TODO get the column where the new piece ia added

                col = 1
                if utils.is_valid_move(col):
                    pygame.time.wait(500)
                    utils.make_move(col, utils.COMPUTER)

                self.board = utils.current_numboard
                self.draw_board(self.board)
                self.turn += 1
                self.turn = self.turn % 2

                if utils.is_game_over():
                    self.game_over = True

            pygame.display.update()


K = input(".:Enter K: ")
K = int(K)
METHOD = input(".:Enter Method\n1. Without Alpha Beta\n2. With Alpha Beta\n")
METHOD = int(METHOD)
# Initialize pygame
pygame.init()

# Create instances
main_game = MainGame()
sidebar = Sidebar(main_game.my_font)

# Main game loop
main_game.run()
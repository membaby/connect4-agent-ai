import sys
import utils
import random
from PyQt5.QtWidgets import *

EMPTY_COLOR = "#e0e0e0"
HUMAN_COLOR = "#0000ff"
COMPUTER_COLOR = "#ff0000"


class Connect4Game(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.board = utils.initialize_board()
        self.grid_layout = QGridLayout()
        self.combo_box = QComboBox()
        self.player_label = QLabel()
        self.init_ui()
        self.current_player = utils.HUMAN

    def init_ui(self):
        self.setWindowTitle('Connect 4 Game')
        self.setGeometry(200, 200, 400, 450)

        main_layout = QVBoxLayout()

        # Title label for "Connect 4"
        title_label = QLabel("Connect 4 Game")

        title_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px; text-align: ""center;")
        main_layout.addWidget(title_label)

        for row in range(utils.ROWS):
            row_buttons = []
            for col in range(utils.COLS):
                button = QPushButton()
                button.setFixedSize(50, 50)
                button.setStyleSheet(f"background-color: {EMPTY_COLOR};")
                button.clicked.connect(lambda state, col=col: self.button_clicked(col))
                row_buttons.append(button)
                self.grid_layout.addWidget(button, row, col)
            self.buttons.append(row_buttons)

        # Add the board background to the main layout
        main_layout.addLayout(self.grid_layout)

        # Horizontal layout for the player's turn label and the dropdown
        hbox = QHBoxLayout()

        self.player_label.setText("Human's Turn")
        self.player_label.setStyleSheet("color: blue; font-size: 18px;")
        hbox.addWidget(self.player_label)

        self.combo_box.setStyleSheet(
            "QComboBox { background-color: #FFFFFF; border: 2px solid #555555; color: #000000; min-width: 200px; }"
            "QComboBox::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 15px; "
            "border-left: 1px solid #555555; background-color: #E0E0E0; }"
            "QComboBox::down-arrow { image: url(drop_arrow.png); width: 15px; height: 15px; }"
        )
        self.combo_box.addItems(["MiniMax without alpha-beta", "MiniMax with alpha-beta"])
        self.combo_box.currentIndexChanged.connect(self.combo_box_changed)  # TODO

        font = self.combo_box.font()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.combo_box.setFont(font)
        hbox.addWidget(self.combo_box)

        main_layout.addLayout(hbox)

        self.setLayout(main_layout)
        self.show()

    def button_clicked(self, col):
        if self.current_player == utils.COMPUTER:
            return

        if utils.is_valid_move(self.board, col):
            row = self.drop_disc(col)
            self.buttons[row][col].setStyleSheet(f"background-color: {HUMAN_COLOR};")
            self.board[row][col] = utils.HUMAN

            self.player_label.setText("Computer's Turn")
            self.player_label.setStyleSheet("color: 'red'; font-size: 18px;")
            self.current_player = utils.COMPUTER
            self.computer_agent()

            self.player_label.setText("Human's Turn")
            self.player_label.setStyleSheet("color: 'blue'; font-size: 18px;")
            self.current_player = utils.HUMAN

            if utils.is_board_full(self.board):
                result, color = utils.finalize_game(self.board)
                self.player_label.setText(result)
                self.player_label.setStyleSheet(f"color: {color}; font-size: 18px;")

    def combo_box_changed(self, index):  # TODO
        # Modify the dropdown list content
        pass

    def drop_disc(self, col):
        for row in range(5, -1, -1):
            if self.buttons[row][col].palette().button().color().name() == EMPTY_COLOR:
                return row
        return None

    def computer_agent(self):
        while True:
            col = random.randint(0, utils.COLS - 1)
            if utils.is_valid_move(self.board, col):
                break

        row = self.drop_disc(col)
        self.buttons[row][col].setStyleSheet(f"background-color: {COMPUTER_COLOR};")
        self.board[row][col] = utils.COMPUTER


def main():
    app = QApplication(sys.argv)
    Connect4Game()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

# REQUIREMENT 2.1
# You are required to provide a full game with GUI with only one mode human vs. computer
# We choose whether to use alpha-beta pruning or not in AI agent then play against the agent till the board is full.
# The game dimensions are as follows (width≥7, length≥6).
# You can fix any acceptable dimensions.
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel, QComboBox
from PyQt5.QtGui import QColor, QFont
import random

class Connect4Game(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_player = 1

    def init_ui(self):
        self.setWindowTitle('Connect 4 Game')
        self.setGeometry(200, 200, 400, 450)

        main_layout = QVBoxLayout()

        # Title label for "Connect 4"
        title_label = QLabel("Connect 4 Game")

        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px; text-align: "
                                  "center;")
        main_layout.addWidget(title_label)

        # Create the board background
        self.grid_layout = QGridLayout()
        self.buttons = []

        for row in range(6):
            row_buttons = []
            for col in range(7):
                button = QPushButton()
                button.setFixedSize(50, 50)
                button.setStyleSheet("background-color: #E0E0E0;")
                button.clicked.connect(lambda state, col=col: self.button_clicked(col))
                row_buttons.append(button)
                self.grid_layout.addWidget(button, row, col)
            self.buttons.append(row_buttons)

        # Add the board background to the main layout
        main_layout.addLayout(self.grid_layout)

        # Horizontal layout for the player's turn label and the dropdown
        hbox = QHBoxLayout()

        self.player_label = QLabel("Human's turn")
        self.player_label.setStyleSheet("color: blue; font-size: 18px;")
        hbox.addWidget(self.player_label)

        self.combo_box = QComboBox()
        self.combo_box.setStyleSheet(
            "QComboBox { background-color: #FFFFFF; border: 2px solid #555555; color: #000000; min-width: 200px; }"
            "QComboBox::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 15px; "
            "border-left: 1px solid #555555; background-color: #E0E0E0; }"
            "QComboBox::down-arrow { image: url(drop_arrow.png); width: 15px; height: 15px; }"
        )
        self.combo_box.addItems(
            ["MiniMax without alpha-beta", "MiniMax with alpha-beta"])  # Initial items in the dropdown
        self.combo_box.currentIndexChanged.connect(self.combo_box_changed)

        font = self.combo_box.font()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.combo_box.setFont(font)
        hbox.addWidget(self.combo_box)

        main_layout.addLayout(hbox)

        self.setLayout(main_layout)
        self.show()

    def button_clicked(self, col):
        row = self.drop_disc(col)
        if row is not None:
            player_color = QColor("blue")
            self.buttons[row][col].setStyleSheet(f"background-color: {player_color.name()};")
            self.current_player = 2 if self.current_player == 1 else 1
            self.computer_agent()
            self.player_label.setStyleSheet(f"color: {'blue' if self.current_player == 1 else 'red'}; font-size: 18px;")
            self.player_label.setText(f"Human's Turn")
            self.current_player = 2 if self.current_player == 1 else 1
            self.player_label.setStyleSheet(f"color: {'blue' if self.current_player == 1 else 'red'}; font-size: 18px;")

    def combo_box_changed(self, index):
        # Modify the dropdown list content
        self.current_player = 1
        self.player_label.setText("Human's Turn")
        self.player_label.setStyleSheet("color: blue; font-size: 18px;")

    def drop_disc(self, col):
        for row in range(5, -1, -1):
            if self.buttons[row][col].palette().button().color().name() == "#e0e0e0":
                return row
        return None

    def computer_agent(self):
        available_cols = [col for col in range(7) if
                          self.buttons[0][col].palette().button().color().name() == "#e0e0e0"]
        if available_cols:
            selected_col = random.choice(available_cols)
            for row in range(5, -1, -1):
                if self.buttons[row][selected_col].palette().button().color().name() == "#e0e0e0":
                    player_color = QColor("red")
                    self.buttons[row][selected_col].setStyleSheet(f"background-color: {player_color.name()};")
                    break

def main():
    app = QApplication(sys.argv)
    game = Connect4Game()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

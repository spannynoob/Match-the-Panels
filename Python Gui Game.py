import sys
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout)
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QFont, QIcon, QResizeEvent

class MemoryGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Emoji Game ~ spannynoob")
        self.setMinimumSize(450, 560)
        self.resize(600, 725)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(8)
        main_layout.setContentsMargin(25, 25, 25, 25)
        
        top_layout = QVBoxLayout()
        
        self.new_game_button = QPushButton ("🔄 Restart")
        self.new_game_button.setProperty("class", "new_game_button")
        self.new_game_button.clicked.connect(self.start_new_game)
        self.new_game_button.setFixedHeight(38)
        top_layout.addWidget(self.new_game_button)
        
        self.info_label = QLabel("Attempts: 0")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setFont(QFont("Arial", 18))
        self.info_label.setStyleSheet("color: #472c50; margin: 10px")
        top_layout.addWidget(self.info_label)
        
        main_layout.addLayout(top_layout)
        
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(8)
        main_layout.addWidget(self.grid_container)
        
        self.buttons = []
        self.first_card = None
        self.can_click = True
        self.attempts = 0
        self.matches = 0
        
        self.Emojis = ['🏀', '🚁', '🏎', '🛸', '⚡', '📂', '🚇', '🦼']
        self.Emojis *= 2
        random.shuffle(self.Emojis)
        
        self.create_buttons()
        
        self.load_styles()
        
    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.adjust_button_sizes()
        
        
    def adjust_button_sizes(self):
        container_width = self.grid_container.width()
        container_height = self.grid_container.height()
        
        spacing = self.grid_layout.spacing()
        available_width = container_width - (3 * spacing)
        available_height = container_height - (3 * spacing)
        
        button_size = min(available_width // 4, available_height // 4)
        
        font_size = max(int(button_size * 0.4), 12)
        
        for button in self.buttons:
            button.setFixedSize (button_size, button_size)
            font = button.font()
            font.setPointSize(font_size)
            button.setFont(font)
            
    def create_buttons(self):
        for i in range(4):
            for j in range(4):
                button = QPushButton()
                button.setFont(QFont("Arial", 45))
                button.setProperty("class", "card")
                button.clicked.connect(lambda checked=False, r=i, c=j:
self.button_clicked(r, c))
                self.grid_layout.addWidget(button, i, j)
                self.buttons.append(button)
                
    def load_styles(self):
        try:
            with open("Python Gui Game/Panel.qss", "r") as f:
                self.setStyleSheet(f.read())
        except:
            self.setStyleSheet("""
                QPushButton.card {
                    background-color: #9e34db;
                    border-radius: 8px
                    border: none
                }
                QPushButton.card:hover {
                    background-color: #a44ad9;
                }
                QPushButton[matched="true"] {
                    background-color: #2eaacc;
                    border-radius: 10px
                }
            """)
            
    def button_clicked(self, row, col):
        if not self.can_click:
            return
        
        button = self.grid_layout.itemAtPosition(row, col).widget()
        index = row * 4 + col
        
        if button.text() or button.property("matched"):
            return
        
        button.setText(self.Emojis[index])
        
        if self.first_card is None:
            self.first_card = (button, index)
        else:
            first_button, first_index = self.first_card
            if button == first_button:
                return
            
            self.attempts += 1
            self.info_label.setText(f"attempts: {self.attempts}")
            if self.Emojis[index] == self.Emojis[first_index]:
                button.setProperty("matched", True)
                first_button.setProperty("matched", True)
                
                button.style().unpolish(button)
                button.style().polish(button)
                first_button.style().unpolish(first_button)
                first_button.style().polish(first_button)
                
                self.matches += 1
                
                if self.matches == 8:
                    self.info_label.setText(f"Congratulations! You win after {self.attempts} attempts!!")
            else:
                self.can_click = False
                QTimer.singleShot(1000, lambda: self.hide_cards(button, first_button))
            
            self.first_card = None
    def hide_cards(self, button1, button2):
        button1.setText("")
        button2.setText("")
        self.can_click = True
   
    def start_new_game(self):
        random.shuffle(self.Emojis)
        
        self.first_card = None
        self.can_click = True
        self.attempts = 0
        self.matches = 0
        
        self.info_label.setText("attempts: 0")
        
        for button in self.buttons:
            button.setText("")
            button.setProperty("matched", False)
            
            button.style().unpolish(button)
            button.style().polish(button)
        
        self.load_styles()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = MemoryGame()
    game.show()
    sys.exit(app.exec())
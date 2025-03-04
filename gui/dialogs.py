from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton

from utils.players import TeamMember


class DelPlayerDialog(QDialog):
    def __init__(self, parent=None, players: list[TeamMember]=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("Delete a Task Type")
        self.players = players

        self.label_player_name = QLabel("Choose the Player to delete:")
        self.comBox_player_name = QComboBox(self)
        self.comBox_player_name.addItems(["Select..."])
        self.comBox_player_name.addItems(player.last_name for player in self.players)

        self.delete_button = QPushButton("Delete", self)
        self.delete_button.clicked.connect(self.del_player)

        layout.addWidget(self.label_player_name)
        layout.addWidget(self.comBox_player_name)
        layout.addWidget(self.delete_button)

        self.return_comBox_index = None

    def del_player(self):
        if not self.comBox_player_name.currentIndex() == 0:
            self.return_comBox_index = self.comBox_player_name.currentIndex()
        self.accept()
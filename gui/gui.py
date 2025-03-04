from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextBrowser, QComboBox, QMessageBox

from gui.dialogs import DelPlayerDialog
from utils.players import TeamMember
from utils import csv_manager as csv_manager


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.players = csv_manager.read_players()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Football Team Manager')
        self.setGeometry(100, 100, 550, 300)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel('Insert player data:')
        self.label_position = QLabel('Position:')
        self.label_shirt_number = QLabel('Shirt number:')
        self.label_last_name = QLabel('Last Name:')
        self.label_goals = QLabel('Scored goals (only for field players):')
        self.label_time_played = QLabel('Time played (minutes):')
        self.label_goals.setEnabled(False)

        self.input_shirt_number = QLineEdit()
        self.input_last_name = QLineEdit()
        self.input_goals = QLineEdit()
        self.input_time_played = QLineEdit()
        self.input_goals.setEnabled(False)

        self.combo_position = QComboBox()
        self.combo_position.addItems(["GoalKeeper", "Defense", "MidField", "Attack"])
        self.combo_position.currentIndexChanged.connect(self.toggle_goal_input)

        self.button_save = QPushButton('Save Player')
        self.button_query = QPushButton('Query')
        self.button_delete = QPushButton('Delete Player')
        self.button_save.clicked.connect(self.save_player)
        self.button_query.clicked.connect(self.query)
        self.button_delete.clicked.connect(self.del_player)

        self.text_result = QTextBrowser()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label_shirt_number)
        self.layout.addWidget(self.input_shirt_number)
        self.layout.addWidget(self.label_last_name)
        self.layout.addWidget(self.input_last_name)
        self.layout.addWidget(self.label_position)
        self.layout.addWidget(self.combo_position)
        self.layout.addWidget(self.label_goals)
        self.layout.addWidget(self.input_goals)
        self.layout.addWidget(self.label_time_played)
        self.layout.addWidget(self.input_time_played)
        self.layout.addWidget(self.button_save)
        self.layout.addWidget(self.button_query)
        self.layout.addWidget(self.text_result)
        self.layout.addWidget(self.button_delete)

    def save_player(self):
        shirt_number = self.input_shirt_number.text()
        last_name = self.input_last_name.text()
        position = self.combo_position.currentText()
        time_played = self.input_time_played.text()
        scored_goals = self.input_goals.text()

        player = TeamMember(shirt_number, last_name, position, time_played, scored_goals)
        if self.validate_data(player):
            if position == "GoalKeeper": player.scored_goals = "No goals"

            if csv_manager.write_player(player):
                self.players.append(player)
                QMessageBox.information(self, "Success", "Player added successfully")
                self.clear_inputs()

    def validate_data(self, player: TeamMember) -> bool:
        errors = []

        if not player.shirt_number:
            errors.append("Missing shirt number")
        else:
            try:
                shirt_number = int(player.shirt_number)
                if shirt_number < 1 or shirt_number > 99:
                    errors.append("Shirt's number must be between 1 a 99")
                elif any(curr_player.shirt_number == shirt_number for curr_player in self.players):
                    errors.append("Shirt's number is already asigned")
            except ValueError:
                errors.append("Invalid value for shirt's number")

        if not player.last_name:
            errors.append("Missing last name")

        if not player.time_played:
            errors.append("Missing time played")
        else:
            try:
                if int(player.time_played) < 1:
                    errors.append("Time played must be bigger than 0")
            except ValueError:
                errors.append("Invalid missing time")

        if player.position != "GoalKeeper":
            if not player.scored_goals:
                errors.append("Missing amount of scored goals")
            elif not player.scored_goals.isdigit():
                errors.append("Invalid scored goals")

        error_message = "Errors:"
        if len(errors) > 0:
            for error in errors:
                error_message += f"\n {error}"

            QMessageBox.warning(self, "Error", f"{error_message}")
            return False
        else:
            return True

    def del_player(self):
        dialog = DelPlayerDialog(self, self.players)
        if dialog.exec_() and dialog.return_comBox_index:
            dialog.return_comBox_index -= 1 # To adjust for the "Select... option"
            del self.players[dialog.return_comBox_index]
            csv_manager.rewrite_players(self.players)

    def query(self):
        result = ""
        for player in self.players:
            if isinstance(player, TeamMember):
                result += f'--Player: {player.last_name:<12}   --Position: {player.position:<12}   --Number: {player.shirt_number:<4}   --Goals: {player.scored_goals:<4}   --Time played: {player.time_played:<6}\n'

        self.text_result.setText(result)

    def clear_inputs(self):
        self.input_shirt_number.clear()
        self.input_last_name.clear()
        self.input_goals.clear()
        self.combo_position.setCurrentIndex(0)
        self.input_time_played.clear()

    def toggle_goal_input(self):
        position = self.combo_position.currentText()
        if position == "GoalKeeper":
            self.label_goals.setEnabled(False)
            self.input_goals.setEnabled(False)
        else:
            self.label_goals.setEnabled(True)
            self.input_goals.setEnabled(True)
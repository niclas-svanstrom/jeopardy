import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog, QProgressBar
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

class JeopardyGame(QWidget):
    def __init__(self):
        super().__init__()

        self.categories = ['Gaming', 'Årtal', 'Kända personer', 'Musik', 'Film', 'Övrigt']
        self.questions = {
            'Gaming': {100: 'Vilket är den mest sålda spelkonsolen?',
                    200: 'Vilket var det första spelet som spelades i rymden?', 
                    300: 'I Kingdom hearts så åker man mellan planeter som representerar olika filmer, \ni första spelet vilken är den första planeten man kan åka till?', 
                    400: 'Vad hette kvinnan som Mario försökte rädda i första Donkey Kong spelet?', 
                    500: 'Vad heter språket i The sims?'},
            'Årtal': {100: 'Vilket år föddes Nelson?', 
                      200: 'Vad hände år 0?', 
                      300: 'Vilket år sjönk titanic?', 
                      400: 'När såg vi Super Mario för första gången?', 
                      500: 'När grundades Facebook som då hette TheFacebook?'},
            'Kända personer': {100: 'Vad hette den första hunden att skickas upp i rymden?', 
                               200: 'North, Saint, Chicago och Psalm är namnen på vad?', 
                               300: 'Vad hette Super Mario när vi fick se honom första gången?',
                                 400: 'Bill Gates grundade Microsoft med vilken barndomsvän?', 
                                 500: 'Vad hette Oprah Winfrey i förnamn innan hon ändrade det till Oprah?'},
            'Musik': {100: 'Vilken artist hade låten "video games"?', 
                      200: 'Vilken är den mest streamade artisten på spotify under 2023?', 
                      300: 'År 2017, vilken singel toppade listorna i 47 länder samtidigt?', 
                      400: 'Vilket band tjänade mer pengar från guitar hero royalties än ett eget album?', 
                      500: 'Vilket är det/den första och enda benadet/artisten som har spelat på samtliga '},
            'Film': {100: 'I vilket land utspelar sig djungelboken?', 
                     200: 'I star wars, vem byggde C-3PO?', 
                     300: 'hur många trappor finns på hogwarts +-10?', 
                     400: 'Vilket företag jobbade huvudpersonen i Cast Away på?', 
                     500: 'Vilken artist är domare under en modevisning i zoolander?'},
            'Övrigt': {100: 'Vilket land uppfann te?', 
                       200: 'Vilket land har flest öar?', 
                       300: 'År 2006 slutade Pluto betecknas som en planet, numera betecknas den som en?', 
                       400: 'Vad kallas ett ensamt strå med spaghetti?', 
                       500: 'Vad kallas en grupp pandor?'},
        }

        self.player_points = {'Q': 0, 'Z': 0, 'P': 0, 'M': 0}
        self.current_question_points = 0
        self.fastest_player = None
        self.current_player = None

        self.player_labels = []

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        title_label = QLabel('Jeopardy')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 72, QFont.Bold))
        title_label.setStyleSheet("QLabel { color: gold; } background-color: black; }")
        main_layout.addWidget(title_label)

        palette = QPalette()
        palette.setColor(QPalette.Button, QColor(255, 200, 0))

        category_layout = QHBoxLayout()

        for category in self.categories:
            category_label = QLabel(category)
            category_label.setAlignment(Qt.AlignCenter)
            category_label.setFont(QFont('Arial', 34))
            category_label.setStyleSheet("QLabel { color: white; }")
            category_layout.addWidget(category_label)

        main_layout.addLayout(category_layout)

        question_layout = QVBoxLayout()

        for amount in [100, 200, 300, 400, 500]:
            amount_layout = QHBoxLayout()
            for category in self.categories:
                button = QPushButton(f'{amount}')
                button.clicked.connect(lambda _, cat=category, amt=amount: self.show_question(cat, amt, button))
                button.setFont(QFont('Arial', 16))
                button.setFixedHeight(100)
                button.setStyleSheet("QPushButton { background-color: darkblue; color: gold; }")  # Ändra färgerna här
                amount_layout.addWidget(button)

            question_layout.addLayout(amount_layout)

        main_layout.addLayout(question_layout)

        self.label = QLabel()
        main_layout.addWidget(self.label)

        score_layout = QHBoxLayout()
        for player in self.player_points:
            player_label = QLabel(f'Lag {player}: {self.player_points[player]} poäng')
            player_label.setFont(QFont('Arial', 16))
            player_label.setAlignment(Qt.AlignCenter)
            player_label.setStyleSheet("QLabel { color: white; }")
            score_layout.addWidget(player_label)

            self.player_labels.append(player_label)

        main_layout.addLayout(score_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Jeopardy Game')
        self.setStyleSheet("background-color: black;")
        self.showMaximized()

    def show_question(self, category, amount, sender_button):
        self.current_question_points = amount

        if self.questions[category][amount] is not None:
            question_dialog = QuestionDialog(self.questions[category][amount], self)
            result = question_dialog.exec_()
            self.fastest_player = question_dialog.fastest_player
            self.fastest_players = question_dialog.fastest_players
            if result == QDialog.Accepted:
                self.player_points[self.fastest_player] += amount
                for p in self.fastest_players:
                    if p == None:
                        continue
                    self.player_points[p] -= amount
                    if self.player_points[p] < 0:
                        self.player_points[p] = 0
            if result == QDialog.Rejected:
                if len(self.fastest_players) > 0:
                    for p in self.fastest_players:
                        if p == None:
                            continue
                        self.player_points[p] -= amount
                        if self.player_points[p] < 0:
                            self.player_points[p] = 0
            self.questions[category][amount] = None
            self.update_score_labels()
            sender_button = self.sender()
            sender_button.setEnabled(False)
            sender_button.setStyleSheet("QPushButton { background-color: gray; color: gold; }")  # Ändra färgerna här

    def update_score_labels(self):
        for i, player in enumerate(self.player_points):
            label = self.player_labels[i]
            label.setText(f'Player {player}: {self.player_points[player]} poäng')

class QuestionDialog(QDialog):
    player_answered_correctly = pyqtSignal(str)

    def __init__(self, question, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Question')
        self.resize(1400, 900)

        screen_geometry = QApplication.desktop().screenGeometry()

        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        self.move(x, y)

        self.fastest_player = None
        self.fastest_players = set()
        self.qtimer = None
        self.ztimer = None
        self.ptimer = None
        self.mtimer = None

        layout = QVBoxLayout()

        question_label = QLabel(question)
        question_label.setAlignment(Qt.AlignCenter)
        question_label.setWordWrap(True)
        question_label.setFont(QFont('Arial', 40))
        question_label.setStyleSheet("QLabel { color: white; }")
        layout.addWidget(question_label)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.timer = QTimer(self)
        self.time_left = 4000
        self.progress_step = 40

        self.fastest_player_label = QLabel()
        self.fastest_player_label.setAlignment(Qt.AlignCenter)
        self.fastest_player_label.setFont(QFont('Arial', 20))
        self.fastest_player_label.setStyleSheet("QLabel { color: white; }")
        layout.addWidget(self.fastest_player_label)

        button_layout = QHBoxLayout()

        self.correct_button = QPushButton('Rätt')
        self.correct_button.clicked.connect(self.correct_answer)
        self.correct_button.setStyleSheet("QPushButton { background-color: darkblue; color: gold; }")
        self.correct_button.setFixedHeight(100)
        self.correct_button.setVisible(False)
        button_layout.addWidget(self.correct_button)

        self.wrong_button = QPushButton('Fel')
        self.wrong_button.clicked.connect(self.wrong_answer)
        self.wrong_button.setStyleSheet("QPushButton { background-color: darkblue; color: gold; }")
        self.wrong_button.setFixedHeight(100)
        self.wrong_button.setVisible(False)
        button_layout.addWidget(self.wrong_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.timer.start(40)

    def update_progress(self):
        self.time_left -= self.progress_step
        progress_bar_value = int((self.time_left / 4000) * 100)
        self.progress_bar.setValue(progress_bar_value)

        if progress_bar_value <= 0:
            self.timer.stop()

    def show_fastest_player(self, player):
        self.fastest_player_label.setText(f'Fastest player: {player}')
        self.fastest_player_label.setVisible(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.timer.timeout.connect(self.update_progress)
            return
        if self.time_left > 0:
            pressed_key = event.key()
            if pressed_key == Qt.Key_Q:
                if self.qtimer is None:
                    self.qtimer = QTimer(self)
                    self.qtimer.timeout.connect(lambda: self.timeout_function(self.qtimer))
                    self.qtimer.start(500)
                    print(self.qtimer)
            elif pressed_key == Qt.Key_Z:
                if self.ztimer is None:
                    self.ztimer = QTimer(self)
                    self.ztimer.timeout.connect(lambda: self.timeout_function(self.ztimer))
                    self.ztimer.start(500)
            elif pressed_key == Qt.Key_P:
                if self.ptimer is None:
                    self.ptimer = QTimer(self)
                    self.ptimer.timeout.connect(lambda: self.timeout_function(self.ptimer))
                    self.ptimer.start(500)
            elif pressed_key == Qt.Key_M:
                if self.mtimer is None:
                    self.mtimer = QTimer(self)
                    self.mtimer.timeout.connect(lambda: self.timeout_function(self.mtimer))
                    self.mtimer.start(500)
        pressed_key = event.key()
        if not self.fastest_player:
            if pressed_key == Qt.Key_Q and not self.qtimer:
                self.show_fastest_player('Q')
                self.set_fastest_player('Q')
                self.show_answer_buttons()
            elif pressed_key == Qt.Key_Z and not self.ztimer:
                self.show_fastest_player('Z')
                self.set_fastest_player('Z')
                self.show_answer_buttons()
            elif pressed_key == Qt.Key_P and not self.ptimer:
                self.show_fastest_player('P')
                self.set_fastest_player('P')
                self.show_answer_buttons()
            elif pressed_key == Qt.Key_M and not self.mtimer:
                self.show_fastest_player('M')
                self.set_fastest_player('M')
                self.show_answer_buttons()

    def timeout_function(self, timer):
        if timer is not None:
            if timer == self.qtimer:
                self.qtimer.stop()
                self.qtimer = None
            elif timer == self.ztimer:
                self.ztimer.stop()
                self.ztimer = None
            elif timer == self.ptimer:
                self.ptimer.stop()
                self.ptimer = None
            elif timer == self.mtimer:
                self.mtimer.stop()
                self.mtimer = None
    
    def show_answer_buttons(self):
        self.correct_button.setVisible(True)
        self.wrong_button.setVisible(True)

    def correct_answer(self):
        self.accept()
    
    def closeEvent(self, event):
        self.reject()
    
    def wrong_answer(self):
        self.time_left = 4000
        self.timer.start(40)
        self.fastest_players.add(self.fastest_player)
        self.fastest_player = None
        self.fastest_player_label.setVisible(False)
        self.correct_button.setVisible(False)
        self.wrong_button.setVisible(False)
    
    def set_fastest_player(self, player):
        self.fastest_player = player

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = JeopardyGame()
    sys.exit(app.exec_())

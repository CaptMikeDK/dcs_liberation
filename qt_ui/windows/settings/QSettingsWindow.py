from PySide2.QtCore import QSize, Qt, QItemSelectionModel, QPoint
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QLabel, QDialog, QGridLayout, QListView, QStackedLayout, QComboBox, QWidget, \
    QAbstractItemView, QPushButton, QGroupBox, QCheckBox

import qt_ui.uiconstants as CONST
from game.game import Game
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal


class QSettingsWindow(QDialog):

    def __init__(self, game: Game):
        super(QSettingsWindow, self).__init__()

        self.game = game

        self.setModal(True)
        self.setWindowTitle("Settings")
        self.setWindowIcon(CONST.ICONS["Settings"])
        self.setMinimumSize(600, 250)

        self.initUi()

    def initUi(self):
        self.layout = QGridLayout()

        self.categoryList = QListView()
        self.right_layout = QStackedLayout()

        self.categoryList.setMaximumWidth(175)

        self.categoryModel = QStandardItemModel(self.categoryList)

        difficulty = QStandardItem("Difficulty")
        difficulty.setIcon(CONST.ICONS["Missile"])
        difficulty.setEditable(False)
        difficulty.setSelectable(True)

        generator = QStandardItem("Mission Generator")
        generator.setIcon(CONST.ICONS["Generator"])
        generator.setEditable(False)
        generator.setSelectable(True)

        cheat = QStandardItem("Cheat Menu")
        cheat.setIcon(CONST.ICONS["Cheat"])
        cheat.setEditable(False)
        cheat.setSelectable(True)

        self.categoryList.setIconSize(QSize(32, 32))
        self.categoryModel.appendRow(difficulty)
        self.categoryModel.appendRow(generator)
        self.categoryModel.appendRow(cheat)

        self.categoryList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.categoryList.setModel(self.categoryModel)
        self.categoryList.selectionModel().setCurrentIndex(self.categoryList.indexAt(QPoint(1,1)), QItemSelectionModel.Select)
        self.categoryList.selectionModel().selectionChanged.connect(self.onSelectionChanged)

        self.initDifficultyLayout()
        self.initGeneratorLayout()
        self.initCheatLayout()

        self.right_layout.addWidget(self.difficultyPage)
        self.right_layout.addWidget(self.generatorPage)
        self.right_layout.addWidget(self.cheatPage)

        self.layout.addWidget(self.categoryList, 0, 0, 1, 1)
        self.layout.addLayout(self.right_layout, 0, 1, 5, 1)

        self.setLayout(self.layout)

    def init(self):
        pass

    def initDifficultyLayout(self):

        self.difficultyPage = QWidget()
        self.difficultyLayout = QGridLayout()
        self.difficultyLayout.setAlignment(Qt.AlignTop)
        self.difficultyPage.setLayout(self.difficultyLayout)

        self.playerCoalitionSkill = QComboBox()
        self.enemyCoalitionSkill = QComboBox()
        self.enemyAASkill = QComboBox()
        for skill in CONST.SKILL_OPTIONS:
            self.playerCoalitionSkill.addItem(skill)
            self.enemyCoalitionSkill.addItem(skill)
            self.enemyAASkill.addItem(skill)

        self.playerCoalitionSkill.setCurrentIndex(CONST.SKILL_OPTIONS.index(self.game.settings.player_skill))
        self.enemyCoalitionSkill.setCurrentIndex(CONST.SKILL_OPTIONS.index(self.game.settings.enemy_skill))
        self.enemyAASkill.setCurrentIndex(CONST.SKILL_OPTIONS.index(self.game.settings.enemy_vehicle_skill))

        self.playerCoalitionSkill.currentIndexChanged.connect(self.applySettings)
        self.enemyCoalitionSkill.currentIndexChanged.connect(self.applySettings)
        self.enemyAASkill.currentIndexChanged.connect(self.applySettings)

        self.difficultyLayout.addWidget(QLabel("Player coalition skill"), 0, 0)
        self.difficultyLayout.addWidget(self.playerCoalitionSkill, 0, 1)
        self.difficultyLayout.addWidget(QLabel("Enemy skill"), 1, 0)
        self.difficultyLayout.addWidget(self.enemyCoalitionSkill, 1, 1)
        self.difficultyLayout.addWidget(QLabel("Enemy AA and vehicles skill"), 2, 0)
        self.difficultyLayout.addWidget(self.enemyAASkill, 2, 1)

        self.difficultyLabel = QComboBox()
        [self.difficultyLabel.addItem(t) for t in CONST.LABELS_OPTIONS]
        self.difficultyLabel.setCurrentIndex(CONST.LABELS_OPTIONS.index(self.game.settings.labels))
        self.difficultyLabel.currentIndexChanged.connect(self.applySettings)

        self.difficultyLayout.addWidget(QLabel("In Game Labels"), 3, 0)
        self.difficultyLayout.addWidget(self.difficultyLabel, 3, 1)

        self.noNightMission = QCheckBox()
        self.noNightMission.setChecked(self.game.settings.night_disabled)
        self.noNightMission.toggled.connect(self.applySettings)
        self.difficultyLayout.addWidget(QLabel("No night missions"), 4, 0)
        self.difficultyLayout.addWidget(self.noNightMission, 4, 1)


    def initGeneratorLayout(self):
        self.generatorPage = QWidget()
        self.generatorLayout = QGridLayout()
        self.generatorLayout.setAlignment(Qt.AlignTop)
        self.generatorPage.setLayout(self.generatorLayout)

        self.coldStart = QCheckBox()
        self.coldStart.setChecked(self.game.settings.cold_start)
        self.coldStart.toggled.connect(self.applySettings)
        self.takeOffOnlyForPlayerGroup = QCheckBox()
        self.takeOffOnlyForPlayerGroup.setChecked(self.game.settings.only_player_takeoff)
        self.takeOffOnlyForPlayerGroup.toggled.connect(self.applySettings)

        self.generatorLayout.addWidget(QLabel("Aircraft cold start"), 0, 0)
        self.generatorLayout.addWidget(self.coldStart, 0, 1)
        self.generatorLayout.addWidget(QLabel("Takeoff only for player group"), 1, 0)
        self.generatorLayout.addWidget(self.takeOffOnlyForPlayerGroup, 1, 1)


    def initCheatLayout(self):

        self.cheatPage = QWidget()
        self.cheatLayout = QGridLayout()
        self.cheatPage.setLayout(self.cheatLayout)

        self.moneyCheatBox = QGroupBox("Money Cheat")
        self.moneyCheatBox.setAlignment(Qt.AlignTop)
        self.moneyCheatBoxLayout = QGridLayout()
        self.moneyCheatBox.setLayout(self.moneyCheatBoxLayout)

        self.cheat25M = QPushButton("Cheat +25M")
        self.cheat50M = QPushButton("Cheat +50M")
        self.cheat100M = QPushButton("Cheat +100M")
        self.cheat200M = QPushButton("Cheat +200M")

        self.cheat25M.clicked.connect(lambda: self.cheatMoney(25))
        self.cheat50M.clicked.connect(lambda: self.cheatMoney(50))
        self.cheat100M.clicked.connect(lambda: self.cheatMoney(100))
        self.cheat200M.clicked.connect(lambda: self.cheatMoney(200))

        self.moneyCheatBoxLayout.addWidget(self.cheat25M, 0, 0)
        self.moneyCheatBoxLayout.addWidget(self.cheat50M, 0, 1)
        self.moneyCheatBoxLayout.addWidget(self.cheat100M, 1, 0)
        self.moneyCheatBoxLayout.addWidget(self.cheat200M, 1, 1)

        self.cheatLayout.addWidget(self.moneyCheatBox, 0, 0)

    def cheatMoney(self, amount):
        self.game.budget += amount
        GameUpdateSignal.get_instance().updateGame(self.game)

    def applySettings(self):
        self.game.settings.player_skill = CONST.SKILL_OPTIONS[self.playerCoalitionSkill.currentIndex()]
        self.game.settings.enemy_skill = CONST.SKILL_OPTIONS[self.enemyCoalitionSkill.currentIndex()]
        self.game.settings.enemy_vehicle_skill = CONST.SKILL_OPTIONS[self.enemyAASkill.currentIndex()]
        self.game.settings.labels = CONST.LABELS_OPTIONS[self.difficultyLabel.currentIndex()]
        self.game.settings.night_disabled = self.noNightMission.isChecked()
        self.game.settings.only_player_takeoff = self.takeOffOnlyForPlayerGroup.isChecked()
        self.game.settings.cold_start = self.coldStart.isChecked()

        GameUpdateSignal.get_instance().updateGame(self.game)

    def onSelectionChanged(self):
        index = self.categoryList.selectionModel().currentIndex().row()
        self.right_layout.setCurrentIndex(index)
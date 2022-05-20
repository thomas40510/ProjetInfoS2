from Tarot_Africain import *
from IHM import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *


class Jeu_Tarot(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


class DialogWelcome(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Bienvenue !")
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)

        QTxt = QInputDialog()

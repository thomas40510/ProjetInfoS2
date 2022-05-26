from Tarot_Africain import *
from IHM import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *


class Jeu_Tarot(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.playerName = self.dialogName
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        tarot = Tarot([[self.playerName, 'humain']] + [['Bot1', 'bot']] + [['Bot2', 'bot']] + [['Bot3', 'bot']],
                      nbPoints=10,
                      aff=False)
        tarot.exe()  # TODO : remove all console inputs to make it work w/ GUI
        i = 0
        for element in (self.ui.pVies, self.ui.b1Vies, self.ui.b2Vies, self.ui.b3Vies):
            element.setText(str(tarot.vies[i]))
            i += 1

    @property
    def dialogName(self):
        text, ok = QInputDialog.getText(self, 'Nom', 'Entrez votre nom:')
        if ok:
            return str(text)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Jeu_Tarot()
    window.show()
    sys.exit(app.exec_())

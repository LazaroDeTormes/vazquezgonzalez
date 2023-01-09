from PyQt6 import QtWidgets
from views import Ui_dlgSalir


class DialogoSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogoSalir, self).__init__()
        self.ui = Ui_dlgSalir()
        self.ui.setupUi(self)
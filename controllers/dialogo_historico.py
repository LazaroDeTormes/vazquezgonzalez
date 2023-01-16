from PyQt6 import QtWidgets
from views import Ui_dlgHistorico


class DialogoHistorico(QtWidgets.QDialog):
    def __init__(self):
        super(DialogoHistorico, self).__init__()
        self.ui = Ui_dlgHistorico()
        self.ui.setupUi(self)
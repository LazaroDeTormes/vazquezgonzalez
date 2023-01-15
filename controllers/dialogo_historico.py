from PyQt6 import QtWidgets, QtCore
from views import Ui_dlgCalendar
from datetime import datetime


class DialogoHistorico(QtWidgets.QDialog):
    def __init__(self):
        super(DialogoHistorico, self).__init__()
        self.ui = Ui_dlgHistorico()
        self.ui.setupUi(self)


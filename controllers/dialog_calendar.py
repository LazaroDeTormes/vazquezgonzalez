from PyQt6 import QtWidgets, QtCore
from views import Ui_dlgCalendar
from datetime import datetime


class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar, self).__init__()
        self.ui = Ui_dlgCalendar()
        self.ui.setupUi(self)
        dia = datetime.now().day
        mes = datetime.now().month
        anho = datetime.now().year
        self.ui.calendario.setSelectedDate(QtCore.QDate(anho, mes, dia))




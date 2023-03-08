from PyQt6 import QtWidgets, QtSql
from views import Ui_dlgHistorico


class DialogoHistorico(QtWidgets.QDialog):
    def __init__(self):
        super(DialogoHistorico, self).__init__()
        self.ui = Ui_dlgHistorico()
        self.ui.setupUi(self)

    def cargarTabHistorico(self):
        """

        Carga los coches dados de baja

        """
        try:
            tabla = self.ui.tabBajas

            indice = 0
            query = QtSql.QSqlQuery()
            query.prepare('select matricula, dniCli, marca, modelo, motor, fecha '
                          '     from historicoches')

            if query.exec():
                while query.next():
                    tabla.setRowCount(indice + 1)

                    tabla.setItem(indice, 0, QtWidgets.QTableWidgetItem(str(query.value(1))))
                    tabla.setItem(indice, 1, QtWidgets.QTableWidgetItem(str(query.value(0))))
                    tabla.setItem(indice, 2, QtWidgets.QTableWidgetItem(str(query.value(2))))
                    tabla.setItem(indice, 3, QtWidgets.QTableWidgetItem(str(query.value(3))))
                    tabla.setItem(indice, 4, QtWidgets.QTableWidgetItem(str(query.value(4))))
                    tabla.setItem(indice, 5, QtWidgets.QTableWidgetItem(str(query.value(5))))

                    indice = indice + 1

        except Exception as error:
            print("Error al cargar el histórico: " + str(error))

    def alinearTablaHistorico(self):
        """

        Ajusta el tamaño del histórico.

        """
        try:
            header = self.ui.tabBajas.horizontalHeader()
            for i in range(header.model().columnCount()):
                header.setSectionResizeMode(i,QtWidgets.QHeaderView.ResizeMode.Stretch)
                if i ==0:
                    header.setSectionResizeMode(i,QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        except Exception as error:
            print(error)
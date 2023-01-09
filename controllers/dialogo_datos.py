from PyQt6 import QtWidgets, QtSql
from views import Ui_dlgDatos

from datetime import datetime

import xlwt


class DialogoDatos(QtWidgets.QDialog):
    def __init__(self):
        super(DialogoDatos, self).__init__()
        self.ui = Ui_dlgDatos()
        self.ui.setupUi(self)

        self.ui.btnAceptar.clicked.connect(self.exportacion)

    def exportacion(self):

        if self.ui.chbCliente.isChecked():

            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            file = (str(fecha) + '_Clientes.xls')
            directorio, filename = QtWidgets.QFileDialog().getSaveFileName(None, 'Guardar Datos', file, '.xls')
            wb = xlwt.Workbook()
            sheet1 = wb.add_sheet('Clientes')
            sheet1.write(0, 0, 'DNI')
            sheet1.write(0, 1, 'Nombre')
            sheet1.write(0, 2, 'Fecha Alta')
            sheet1.write(0, 3, 'Dirección')
            sheet1.write(0, 4, 'Provincia')
            sheet1.write(0, 5, 'Municipio')
            sheet1.write(0, 6, 'Forma de pago')

            fila = 1
            query = QtSql.QSqlQuery()
            query.prepare('select * from clientes order by dni;')

            if query.exec():

                while query.next():

                    for i in range(0, 7):
                        sheet1.write(fila, i, str(query.value(i)))

                    fila += 1

            wb.save(directorio)
            msg = QtWidgets.QMessageBox()
            msg.setModal(True)
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText('Exportación de datos realizada con éxito')
            msg.exec()

        if self.ui.chbCoche.isChecked():

            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            file = (str(fecha) + '_Coches.xls')
            directorio, filename = QtWidgets.QFileDialog.getSaveFileName(None, 'Guardar Datos', file, '.xls')
            wb = xlwt.Workbook()
            sheet1 = wb.add_sheet('Coches')
            sheet1.write(0, 0, 'Matrícula')
            sheet1.write(0, 1, 'DNI')
            sheet1.write(0, 2, 'Marca')
            sheet1.write(0, 3, 'Modelo')
            sheet1.write(0, 4, 'Motor')

            fila = 1
            query = QtSql.QSqlQuery()
            query.prepare('select * from coches order by dniCli;')

            if query.exec():

                while query.next():
                    for i in range(0, 5):
                        sheet1.write(fila, i, str(query.value(i)))

                    fila += 1

            wb.save(directorio)
            msg = QtWidgets.QMessageBox()
            msg.setModal(True)
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText('Exportación de datos realizada con éxito')
            msg.exec()

        self.close()

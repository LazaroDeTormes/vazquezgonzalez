# Form implementation generated from reading ui file 'C:/Users/a21alejandrovg/PycharmProjects/vazquezgonzalez/views/dlgHistorico.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dlgHistorico(object):
    def setupUi(self, dlgHistorico):
        dlgHistorico.setObjectName("dlgHistorico")
        dlgHistorico.resize(820, 460)
        self.tabBajas = QtWidgets.QTableWidget(dlgHistorico)
        self.tabBajas.setEnabled(True)
        self.tabBajas.setGeometry(QtCore.QRect(20, 160, 780, 290))
        self.tabBajas.setMinimumSize(QtCore.QSize(780, 290))
        self.tabBajas.setMaximumSize(QtCore.QSize(780, 290))
        self.tabBajas.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabBajas.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabBajas.setObjectName("tabBajas")
        self.tabBajas.setColumnCount(6)
        self.tabBajas.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tabBajas.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabBajas.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabBajas.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabBajas.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabBajas.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabBajas.setHorizontalHeaderItem(5, item)
        self.label = QtWidgets.QLabel(dlgHistorico)
        self.label.setGeometry(QtCore.QRect(0, 0, 821, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 209, 8);\n"
"background-color: rgb(58, 58, 58);")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(dlgHistorico)
        self.label_2.setGeometry(QtCore.QRect(50, 50, 241, 101))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("C:/Users/a21alejandrovg/PycharmProjects/vazquezgonzalez/views\\../../../OneDrive/Documentos/CLASE/vazquezgonzalez/img/decoraciones/coche.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(dlgHistorico)
        self.label_3.setGeometry(QtCore.QRect(336, 60, 171, 91))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("C:/Users/a21alejandrovg/PycharmProjects/vazquezgonzalez/views\\../../../OneDrive/Documentos/CLASE/vazquezgonzalez/img/decoraciones/calavera.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(dlgHistorico)
        self.label_4.setGeometry(QtCore.QRect(550, 60, 221, 91))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("C:/Users/a21alejandrovg/PycharmProjects/vazquezgonzalez/views\\../../../OneDrive/Documentos/CLASE/vazquezgonzalez/img/decoraciones/cocheLlamas.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(dlgHistorico)
        QtCore.QMetaObject.connectSlotsByName(dlgHistorico)

    def retranslateUi(self, dlgHistorico):
        _translate = QtCore.QCoreApplication.translate
        dlgHistorico.setWindowTitle(_translate("dlgHistorico", "Dialog"))
        item = self.tabBajas.horizontalHeaderItem(0)
        item.setText(_translate("dlgHistorico", "DNI"))
        item = self.tabBajas.horizontalHeaderItem(1)
        item.setText(_translate("dlgHistorico", "MATRÍCULA"))
        item = self.tabBajas.horizontalHeaderItem(2)
        item.setText(_translate("dlgHistorico", "MARCA"))
        item = self.tabBajas.horizontalHeaderItem(3)
        item.setText(_translate("dlgHistorico", "MODELO"))
        item = self.tabBajas.horizontalHeaderItem(4)
        item.setText(_translate("dlgHistorico", "MOTOR"))
        item = self.tabBajas.horizontalHeaderItem(5)
        item.setText(_translate("dlgHistorico", "FECHA DE BAJA"))
        self.label.setText(_translate("dlgHistorico", "HISTÓRICO DE BAJAS"))
import calendar

import xlrd as xlrd
import xlwt
from PyQt6 import QtWidgets, QtSql
from PyQt6.uic.properties import QtCore
from reportlab.pdfgen import canvas

from views import Ui_venMain
from controllers import DialogoSalir, DialogoDatos, DialogCalendar
import sys
from datetime import datetime
import zipfile
import shutil
import os


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        self.ui = Ui_venMain()
        self.ui.setupUi(self)
        self.avisosalir = DialogoSalir()
        self.dlgcalendar = DialogCalendar()
        self.avisoDatos = DialogoDatos()
        self.dlgHistorico = DialogoHistorico()

        '''
        Eventos de la barra de iconos
        '''
        self.ui.SalirBarra.triggered.connect(self.salir)                        # === sale del programa === #

        self.ui.actionCrearBU2.triggered.connect(self.creaBackup)               # === guarda los datos === #

        self.ui.actionRestaurarBU2.triggered.connect(self.restauraBackup)       # === restaura los datos === #

        self.ui.actionExportar.triggered.connect(self.exportarDatos)            # === exporta los datos === #

        '''
        Eventos de la barra de herramientas
        '''
        self.ui.actionSalir.triggered.connect(self.salir)                               # === sale del programa === #

        self.ui.actionCrear_Copia_Seguridad.triggered.connect(self.creaBackup)          # === guarda los datos === #

        self.ui.actionRestaurar_Copia_Seguridad.triggered.connect(self.restauraBackup)  # === restaura los datos === #

        self.ui.actionImportar.triggered.connect(self.importarDatos)                    # === importa los datos === #

        '''
        Eventos de botones variados
        '''
        self.ui.btnFechaCli.clicked.connect(self.abrirCalendario)               # === abre el calendario === #

        self.ui.btnLimpiar.clicked.connect(self.limpiaCli)                      # === limpia el formulario === #

        self.ui.btnGuardarCli.clicked.connect(self.guardarCli)                  # === guarda un cliente === #

        self.ui.btnBorraCli.clicked.connect(self.eliminarCliente)               # === borra un cliente === #

        self.ui.tabCli.clicked.connect(self.cargaCliente)                       # === carga un cliente === #

        self.ui.btnModifCli.clicked.connect(self.modifCliente)                  # === modifica un cliente === #

        self.ui.btnHist.clicked.connect(self.abrirHistorico)                    # === abre el histórico === #

        '''
        Listado de eventos de cajas del formulario
        '''
        self.ui.txtDniCli.editingFinished.connect(self.mostrarValidezDNI)       # === comprueba el DNI ===#

        self.ui.txtNombreCli.editingFinished.connect(self.letrasCapital)        # === pone las mayúsculas ===#

        self.ui.txtDirCli.editingFinished.connect(self.letrasCapital)           # === pone las mayúsculas ===#

        self.ui.txtMatr.editingFinished.connect(self.letrasCapital)             # === pone las mayúsculas ===#

        self.ui.txtModelo.editingFinished.connect(self.letrasCapital)           # === pone las mayúsculas ===#

        '''
        Llamadas a funciones varias
        '''
        self.selMotor()                                                         # === asegura el motor ===#

        self.conexion()                                                         # === conexión con la base ===#

        self.cargarProvincia()                                                  # === llena las provincias ===#

        self.mostrarTabCocheCli()                                               # === muestra la tabla de coches ===#

        self.mostrarTabProductos()                                              # === muestra la tabla productos === #

        self.restructuracionTablaCocheCli()                                     # === reestructura la tabla coches ===#

        self.ui.cmbProCli.currentIndexChanged.connect(self.cargarMunicipio)     # === llena los municipios ===#

        '''
        Llamadas a funciones de productos (examen)
        '''
        self.ui.btnBorrarProd.clicked.connect(self.eliminarProducto)            # === borra un producto === #

        self.ui.tabProd.clicked.connect(self.cargaProducto)                     # === carga un producto === #

        self.ui.btnModificarProd.clicked.connect(self.modificarProducto)        # === modifica un producto === #

        self.ui.btnAnhadirProd.clicked.connect(self.creaProd)                   # === crea un producto === #

        self.ui.btnExportarProd.clicked.connect(self.exportaProd)               # === exporta los productos === #

        '''
        Llamadas a funciones de informes
        '''
        self.ui.actionInforme_Clientes.triggered.connect(self.crearInformeCli)      # === crea informe de clientes === #
        
        self.ui.actionInforme_Coches.triggered.connect(self.crearInformeAuto)       # === crea informe de coches === #
    '''
    ========================================================================================================================
    
                                                    M  É  T  O  D  O  S
    
    ========================================================================================================================
    '''

    def salir(self):
        try:
            self.avisosalir.show()
            if self.avisosalir.exec():
                sys.exit()
            else:
                self.avisosalir.hide()

        except Exception as error:
            print(error)

    def abrirCalendario(self):
        try:
            self.dlgcalendar.show()
            self.cargarFecha()
        except Exception as error:
            print(error)

    def letrasCapital(self):
        try:
            self.ui.txtNombreCli.setText(self.ui.txtNombreCli.text().title())
            self.ui.txtDniCli.setText(self.ui.txtDniCli.text().title())
            self.ui.txtMatr.setText(self.ui.txtMatr.text().upper())
            self.ui.txtModelo.setText(self.ui.txtModelo.text().title())
            self.ui.txtMarca.setText(self.ui.txtMarca.text().title())
            self.ui.txtDirCli.setText(self.ui.txtDirCli.text().title())
        except Exception as error:
            print(error)

    def restructuracionTablaCocheCli(self):
        try:
            header = self.ui.tabCli.horizontalHeader()
            for i in range(5):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                if i == 0 or i == 1:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        except Exception as error:
            print(error)

    def creaBackup(self):
        try:
            pantalla = QtWidgets.QFileDialog()

            fecha = datetime.today()
            fecha = fecha.strftime("%Y.%m.%d.%H.%M.%S")
            copia = (str(fecha) + '_backup.zip')

            directorio, filename = pantalla.getSaveFileName(None, 'Guardar copia', copia, '.zip')

            if pantalla.accept and filename != '':
                fichzip = zipfile.ZipFile(copia, 'w')
                fichzip.write(self.bbdd, os.path.basename(self.bbdd), zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(str(copia), str(directorio))
                msg = QtWidgets.QMessageBox()
                msg.setModal(True)
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Copia creada con éxito.')
                msg.exec()

        except Exception as error:
            print(error)

    def restauraBackup(self):
        try:
            pantalla = QtWidgets.QFileDialog()

            filename = pantalla.getOpenFileName(None, 'Restaurar copia de seguridad', '',
                                                '*.zip;;All Files (*)')

            if pantalla.accept and filename != '':
                file = filename[0]
                with zipfile.ZipFile(str(file), 'r') as bbdd:
                    bbdd.extractall(pwd=None)
                    bbdd.close()

            self.conexion()
            self.mostrarTabCocheCli()

            msg = QtWidgets.QMessageBox()
            msg.setModal(True)
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText('Copia de seguridad restaurada')
            msg.exec()


        except Exception as error:
            print(error)

    def exportarDatos(self):
        try:

            ventana = self.avisoDatos

            ventana.show()



        except Exception as error:
            print("Error exportar datos", error)

    def validarDNI(self, dni):
        '''
        Módulo para la validación de DNI
        :return: boolean
        '''

        try:
            numeros = "1234567890"
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {"X": "0", "Y": "1", "Z": "2"}
            dni = dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext)
                return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control
            return False
        except Exception as error:
            print("Error validez DNI: ", error)

    def mostrarValidezDNI(self):
        try:
            dniCaja = self.ui.txtDniCli
            dni = dniCaja.text()
            verificacion = self.ui.lblValidarDni

            if self.validarDNI(dni):

                verificacion.setStyleSheet("color: green")
                verificacion.setText("V")
                dniCaja.setText(dni.upper())

            else:

                verificacion.setStyleSheet("color: red")
                verificacion.setText("X")
                dniCaja.setText(dni.upper())

        except Exception as error:
            print(error)

    def selMotor(self):
        try:
            self.motor = (self.ui.rbtGas, self.ui.rbtDie, self.ui.rbtHib, self.ui.rbtEle)
            for i in self.motor:
                i.toggled.connect(self.cheMotor)
        except Exception as error:
            print(error)

    def cheMotor(self):
        try:
            if self.ui.rbtGas.isChecked():
                motor = "Gasolina"
            elif self.ui.rbtDie.isChecked():
                motor = "Diésel"
            elif self.ui.rbtHib.isChecked():
                motor = "Híbrido"
            elif self.ui.rbtEle.isChecked():
                motor = "Eléctrico"
            else:
                pass
            return motor
        except Exception as error:
            print(error)

    def guardarCli(self):
        try:
            desplePro = self.ui.cmbProCli
            despleMun = self.ui.cmbMunCli

            newcli = []
            cliente = [self.ui.txtDniCli, self.ui.txtNombreCli, self.ui.txtFechaCli, self.ui.txtDirCli]
            for i in cliente:
                newcli.append(i.text())

            prov = desplePro.currentText()
            newcli.append(prov)

            muni = despleMun.currentText()
            newcli.append(muni)
            pagos = []

            if self.ui.ckbTarjeta.isChecked():

                pagos.append('tarjeta')

            elif self.ui.ckbEfectivo.isChecked():

                pagos.append('efectivo')

            elif self.ui.ckbTransferencia.isChecked():

                pagos.append('transferencia')

            pagos = set(pagos)
            newcli.append(';'.join(pagos))

            motor = self.cheMotor()
            newcli.append(motor)

            print(newcli)

            newcar = []
            coche = [self.ui.txtMatr, self.ui.txtMarca, self.ui.txtModelo]
            for i in coche:
                newcar.append(i.text())

            motor = self.cheMotor()
            newcar.append(motor)

            self.altaCli(newcli, newcar)

        except Exception as error:
            print(error)

    def limpiaCli(self):
        try:
            botonesPago = self.ui.btnGrupoPagos
            despleMun = self.ui.cmbMunCli
            desplePro = self.ui.cmbProCli

            cliente = [self.ui.txtDniCli, self.ui.txtNombreCli, self.ui.txtDirCli, self.ui.txtFechaCli, self.ui.txtMatr,
                       self.ui.txtMarca, self.ui.txtModelo]

            for i in cliente:
                i.setText("")

            for i in botonesPago.buttons():
                i.setChecked(False)

            checks = [self.ui.ckbEfectivo, self.ui.ckbTarjeta, self.ui.ckbTransferencia]

            for i in checks:
                i.setChecked(False)

            despleMun.setCurrentText('')
            desplePro.setCurrentText('')
        except Exception as error:
            print(error)

    def cargaCliente(self):

        try:
            despleMun = self.ui.cmbMunCli
            desplePro = self.ui.cmbProCli
            self.limpiaCli()
            fila = self.ui.tabCli.selectedItems()
            datos = [self.ui.txtDniCli, self.ui.txtMatr, self.ui.txtMarca, self.ui.txtModelo]
            row = [dato.text() for dato in fila]

            for i, dato in enumerate(datos):
                dato.setText(row[i])

            if row[4] == 'Diésel':
                self.ui.rbtDie.setChecked(True)
            elif row[4] == 'Gasolina':
                self.ui.rbtGas.setChecked(True)
            elif row[4] == 'Híbrido':
                self.ui.rbtHib.setChecked(True)
            elif row[4] == 'Eléctrico':
                self.ui.rbtEle.setChecked(True)

            registro = self.consultaDni(row[0])
            print(registro)

            self.ui.txtNombreCli.setText(registro[0])

            self.ui.txtDirCli.setText(registro[1])

            self.ui.txtFechaCli.setText(registro[2])

            desplePro.setCurrentText(registro[3])

            despleMun.setCurrentText(registro[4])

            if 'efectivo' in registro[5]:
                self.ui.ckbEfectivo.setChecked(True)
            if 'tarjeta' in registro[5]:
                self.ui.ckbTarjeta.setChecked(True)
            if 'transferencia' in registro[5]:
                self.ui.ckbTransferencia.setChecked(True)


        except Exception as error:
            print(error)

    def cargarFecha(self, qDate):

        try:

            calendario = self.dlgcalendar
            if calendario.ui.calendario.clicked:

                data = ("{0}/{1}/{2}".format(qDate.day(), qDate.month(), qDate.year()))

                self.ui.txtFechaCli.setText(str(data))
                calendario.hide()
            else:
                pass

        except Exception as error:
            print("Error de calendario: " + str(error))

    def conexion(self):

        filedb = 'bases/bbdd.sqlite'
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(filedb)
        self.bbdd = 'bbdd.sqlite'

        if not db.open():
            QtWidgets.QMessageBox.critical(None, "No se ha podido abrir la base. Conexión no establecida.\n",
                                           "Haga click para cerrar.", QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

        else:
            print("Conexión establecida.")
            return True

    def cargarProvincia(self):
        try:
            desplePro = self.ui.cmbProCli

            desplePro.clear()
            query = QtSql.QSqlQuery()
            query.prepare("select provincia from provincias")
            if query.exec():
                desplePro.addItem("")
                while query.next():
                    desplePro.addItem(query.value(0))

        except Exception as error:
            print(error)

    def cargarMunicipio(self):
        try:
            despleMun = self.ui.cmbMunCli
            desplePro = self.ui.cmbProCli

            despleMun.clear()

            query2 = QtSql.QSqlQuery()
            query2.prepare("select municipio "
                           "    from municipios as m inner join provincias as p "
                           "        on p.id = m.provincia_id "
                           "    where p.provincia = :nombre")
            query2.bindValue(":nombre", desplePro.currentText())

            if query2.exec():
                despleMun.addItem("")
                while query2.next():
                    despleMun.addItem(query2.value(0))


        except Exception as error:
            print(error)

    def altaCli(self, newcli, newcar):
        try:
            query0 = QtSql.QSqlQuery()
            query0.prepare("")

            query = QtSql.QSqlQuery()
            query.prepare(
                'insert into clientes (dni, nombre, alta, direccion, provincia, municipio, pago) values (:dni, :nombre, :alta, :direccion, :provincia, :municipio, :pago)')
            query.bindValue(":dni", str(newcli[0]))
            query.bindValue(":nombre", str(newcli[1]))
            query.bindValue(":alta", str(newcli[2]))
            query.bindValue(":direccion", str(newcli[3]))
            query.bindValue(":provincia", str(newcli[4]))
            query.bindValue(":municipio", str(newcli[5]))
            query.bindValue(":pago", str(newcli[6]))

            if query.exec():
                pass

            query2 = QtSql.QSqlQuery()
            query2.prepare(
                'insert into coches (matricula, dniCli, modelo, marca, motor) '
                '   values (:matricula, :dniCli, :modelo, :marca, :motor)')
            query2.bindValue(":matricula", str(newcar[0]))
            query2.bindValue(":dniCli", str(newcli[0]))
            query2.bindValue(":modelo", str(newcar[1]))
            query2.bindValue(":marca", str(newcar[2]))
            query2.bindValue(":motor", str(newcar[3]))

            if query2.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Aviso")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText("Cliente - Coche dado de alta")
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Aviso")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query2.lastError().text())
                msg.exec()

            self.mostrarTabCocheCli()

        except Exception as error:
            print(error)

    def mostrarTabCocheCli(self):
        try:
            tabla = self.ui.tabCli

            indice = 0
            query = QtSql.QSqlQuery()
            query.prepare('select matricula, dniCli, marca, modelo, motor '
                          '     from coches '
                          '     order by marca, modelo;')


            if query.exec():
                while query.next():


                    tabla.setRowCount(indice + 1)

                    tabla.setItem( indice, 0, QtWidgets.QTableWidgetItem(str(query.value(1))))
                    tabla.setItem( indice, 1, QtWidgets.QTableWidgetItem(str(query.value(0))))
                    tabla.setItem( indice, 2, QtWidgets.QTableWidgetItem(str(query.value(2))))
                    tabla.setItem( indice, 3, QtWidgets.QTableWidgetItem(str(query.value(3))))
                    tabla.setItem( indice, 4, QtWidgets.QTableWidgetItem(str(query.value(4))))

                    indice = indice + 1

        except Exception as error:
            print("Hola " + str(error))

    def consultaDni(self, dni):
        try:
            print(str(dni))
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare('select nombre, direccion, alta, provincia, municipio, pago '
                          '     from clientes '
                          '     where dni = :dni')
            query.bindValue(':dni', str(dni))

            query.exec()
            if query.next():
                for i in range(6):
                    registro.append(str(query.value(i)))

            return registro

        except Exception as error:
            print(error)

    def eliminarCliente(self):
        try:

            query3 = QtSql.QSqlQuery()
            query3.prepare('select * from coches where dniCli = :dni')
            query3.bindValue(':dni', str(self.ui.txtDniCli.text()))

            query1 = QtSql.QSqlQuery()
            query1.prepare('delete from coches where dniCli = :dni')
            query1.bindValue(':dni', str(self.ui.txtDniCli.text()))

            query2 = QtSql.QSqlQuery()
            query2.prepare('delete from clientes where dni = :dni')
            query2.bindValue(':dni', str(self.ui.txtDniCli.text()))




            if query3.exec() != "":
                query1.exec()

            query1.exec()
            query2.exec()
            if query2.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('ALERTA')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Baja completada')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("ALERTA")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query2.lastError().text())
                msg.exec()

            self.mostrarTabCocheCli()



        except Exception as error:
            print(error)

    def importarDatos(self):
        try:
            filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Importar datos', '', '*.xls;;All Files (*)')
            if DialogoDatos.accept and filename != '':
                file = filename[0]
                documento = xlrd.open_workbook(file)
                datos = documento.sheet_by_index(0)
                filas = datos.nrows
                print(filas)
                columnas = datos.ncols
                print(columnas)
                for i in range(filas):
                    if i == 0:
                        pass
                    else:

                        newCar = []
                        for j in range(columnas):
                            newCar.append(str(datos.cell_value(i, j)))


                        print(newCar)
                        if self.validarDNI(str(newCar[1])):
                            self.altaCli(newCar)
                self.mostrarTabCocheCli()
                msg = QtWidgets.QMessageBox()
                msg.setModal(True)
                msg.setWindowTitle("Aviso")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Importacion de datos Realizada')
                msg.exec()
        except Exception as error:
            print('Error importar datos: ', error)

    def modifCliente(self):

        try:
            modcar = []
            modclient = []
            cliente = [self.ui.txtDniCli, self.ui.txtNombreCli, self.ui.txtFechaCli, self.ui.txtDirCli]
            for i in cliente:
                modclient.append(i.text())
            prov = self.ui.cmbProCli.currentText()
            modclient.append(prov)
            municipio = self.ui.cmbMunCli.currentText()
            modclient.append(municipio)
            pagos = []
            if self.ui.ckbTarjeta.isChecked():
                pagos.append('Tarjeta')
            if self.ui.ckbEfectivo.isChecked():
                pagos.append('Efectivo')
            if self.ui.ckbTransferencia.isChecked():
                pagos.append('Transferencia')
            pagos = set(pagos)
            modclient.append('; '.join(pagos))
            car = [self.ui.txtMatr, self.ui.txtMarca, self.ui.txtModelo]
            for i in car:
                modcar.append(i.text())
            motor = self.cheMotor()
            modcar.append(motor)
            self.modificarCliente(modclient, modcar)
            self.mostrarTabCocheCli()

        except Exception as error:
            print('Error cambiando cliente', error)

    def modificarCliente(self, modClient, modCar):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'update clientes set nombre = :nombre, alta = :alta, direccion = :direccion, provincia = :provincia, municipio = :municipio, pago = :pago where dni = :dni')
            query.bindValue(':dni', str(modClient[0]))
            query.bindValue(':nombre', str(modClient[1]))
            query.bindValue(':alta', str(modClient[2]))
            query.bindValue(':direccion', str(modClient[3]))
            query.bindValue(':provincia', str(modClient[4]))
            query.bindValue(':municipio', str(modClient[5]))
            query.bindValue(':pago', str(modClient[6]))
            if query.exec():
                pass
            query1 = QtSql.QSqlQuery()
            query1.prepare(
                'update coches set dniCli = :dni, marca = :marca, modelo = :modelo, motor = :motor where matricula = :matricula')
            query1.bindValue(':dni', str(modClient[0]))
            query1.bindValue(':matricula', str(modCar[0]))
            query1.bindValue(':marca', str(modCar[1]))
            query1.bindValue(':modelo', str(modCar[2]))
            query1.bindValue(':motor', str(modCar[3]))
            if query1.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Datos modificados de cliente')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Error')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query1.lastError().text())
                msg.exec()
                print(query1.lastError().text())
        except Exception as error:
            print('Error modificando', error)

    def mostrarTabProductos(self):
        try:
            tabla = self.ui.tabProd

            indice = 0
            query = QtSql.QSqlQuery()
            query.prepare('select servicio, precio '
                          '     from servicios '
                          '     order by id;')

            if query.exec():
                while query.next():
                    tabla.setRowCount(indice + 1)

                    tabla.setItem(indice, 0, QtWidgets.QTableWidgetItem(str(indice+1)))
                    tabla.setItem(indice, 1, QtWidgets.QTableWidgetItem(str(query.value(0))))
                    tabla.setItem(indice, 2, QtWidgets.QTableWidgetItem(str(query.value(1))))

                    indice = indice + 1

        except Exception as error:
            print("Hola " + str(error))

    def eliminarProducto(self):
        try:



            query1 = QtSql.QSqlQuery()
            query1.prepare('delete from servicios where servicio = :concepto')
            query1.bindValue(':concepto', str(self.ui.txtConcepto.text().lower()))




            if query1.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('ALERTA')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Producto eliminado')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("ALERTA")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query1.lastError().text())
                msg.exec()

            self.mostrarTabProductos()



        except Exception as error:
            print(error)

    def cargaProducto(self):

        try:


            fila = self.ui.tabProd.selectedItems()
            datos = [self.ui.txtConcepto, self.ui.txtPrecio]
            row = [dato.text() for dato in fila]

            for i, dato in enumerate(datos):
                dato.setText(row[i])





            self.ui.txtConcepto.setText(row[1].title())

            self.ui.txtPrecio.setText(row[2])





        except Exception as error:
            print(error)

    def modificarProducto(self):
        try:

            modProd = []
            producto = [self.ui.txtConcepto, self.ui.txtPrecio]
            for i in producto:
                modProd.append(i.text())


            query = QtSql.QSqlQuery()
            query.prepare(
                'update servicios set servicio = :concepto, precio = :precio where servicio = :concepto')
            query.bindValue(':concepto', str(modProd[0]))
            query.bindValue(':precio', str(modProd[1]))

            if query.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Datos modificados del producto')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Error')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()
                print(query.lastError().text())

            self.mostrarTabProductos()
        except Exception as error:
            print('Error modificando', error)

    def creaProd(self):
        try:


            newprod = []
            producto = [self.ui.txtConcepto, self.ui.txtPrecio.text()]
            for i in producto:
                newprod.append(i.text())


            query = QtSql.QSqlQuery()
            query.prepare(
                'insert into servicios (servicio, precio) values (:concepto, :precio)')
            query.bindValue(":concepto", str(newprod[0].title()))
            query.bindValue(":precio", str(newprod[1]))


            if query.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Aviso")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText("Producto añadido")
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Aviso")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()


            self.mostrarTabProductos()

        except Exception as error:
            print(error)

    def exportaProd(self):

        fecha = datetime.datetime.today()
        fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
        file = (str(fecha) + '_Servicios.xls')
        directorio, filename = QtWidgets.QFileDialog().getSaveFileName(None, 'Guardar Datos', file, '.xls')
        wb = xlwt.Workbook()
        sheet1 = wb.add_sheet('Servicios')
        sheet1.write(0, 0, 'ID')
        sheet1.write(0, 1, 'Concepto')
        sheet1.write(0, 2, 'Precio')


        fila = 1
        query = QtSql.QSqlQuery()
        query.prepare('select * from servicios order by id;')

        if query.exec():

            while query.next():

                for i in range(0, 3):
                    sheet1.write(fila, i, str(query.value(i)))

                fila += 1

        wb.save(directorio)
        msg = QtWidgets.QMessageBox()
        msg.setModal(True)
        msg.setWindowTitle('Aviso')
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setText('Exportación de datos realizada con éxito')
        msg.exec()

    def crearInformeCli(self):

            try:
                self.titulo = 'LISTA DE CLIENTES'

                dir, file = QtWidgets.QFileDialog().getSaveFileName(None, 'Guardar Datos', "Listado", '.pdf')
                self.report = canvas.Canvas(dir+file)

                self.report.drawString(230,700, 'LISTA DE CLIENTES')
                items = ['DNI', 'Nombre', 'Dirección', 'Provincia', 'Municipio']
                self.report.line(50, 660, 525, 660)
                self.report.setFont('Helvetica-Bold', size=10)
                self.report.drawString(60, 650, items[0])
                self.report.drawString(120, 650, items[1])
                self.report.drawString(270, 650, items[2])
                self.report.drawString(360, 650, items[3])
                self.report.drawString(460, 650, items[4])
                self.report.line(50, 645, 525, 645)
                self.cuerpoInformeCliente()
                self.pieInforme()
                self.topInforme()
                self.report.save()




                #rootPath = '.\\informes'
                #os.startfile('%s\%s' % (rootPath, 'listadoClientes.pdf'))
            except Exception as error:
                print('Error informes estado clientes: '+ str(error))
            
    def crearInformeAuto(self):
        try:
            self.titulo = 'LISTA DE VEHÍCULOS'
            dir, file = QtWidgets.QFileDialog().getSaveFileName(None, 'Guardar Datos', "Listado", '.pdf')
            self.report = canvas.Canvas(dir + file)
            self.report.drawString(230, 700, 'LISTA DE VEHÍCULOS')
            items = ['DNI', 'Matrícula', 'Marca', 'Modelo', 'Motor']
            self.report.line(50, 660, 525, 660)
            self.report.setFont('Helvetica-Bold', size=10)
            self.report.drawString(60, 650, items[0])
            self.report.drawString(120, 650, items[1])
            self.report.drawString(270, 650, items[2])
            self.report.drawString(360, 650, items[3])
            self.report.drawString(460, 650, items[4])
            self.report.line(50, 645, 525, 645)
            self.cuerpoInformeCoche()
            self.pieInforme()
            self.topInforme()
            self.report.save()
            
        except Exception as error:
            print('Error informes estado clientes: ' + str(error))

    def pieInforme(self):
        try:
            self.report.line(50,50,525,50)
            fecha = datetime.datetime.today()
            fecha = fecha.strftime('%d.%m.%Y %H:%M:%S')
            self.report.setFont('Helvetica-Oblique', size=7)
            self.report.drawString(50,40, str(fecha))
            self.report.drawString(250, 40, str(self.titulo))
            self.report.drawString(475, 40, 'Página {}'.format(self.report.getPageNumber()))
        except Exception as error:
            print('Error pie de informe de cualquier tipo: '+str(error))

    def topInforme(self):
        try:

            logo = '.\img\logo.jpg'
            self.report.line(50, 800, 525, 800)
            self.report.line(50, 720, 525, 720)
            self.report.setFont('Helvetica-Bold', size=14)
            self.report.drawImage(logo, 15, 680, width=120, height=150)
            self.report.drawString(230, 815, 'Taller Mecánico Teis')
            self.report.drawImage(logo, 460, 680, width=120, height=150)

            self.report.setFont('Helvetica', size=9)
            self.report.drawString(150, 785, 'CIF: A12345678')
            self.report.drawString(350, 785, 'Avda. Galicia - 101')
            self.report.drawString(350, 775, 'Vigo - 36216 - España')
            self.report.drawString(150, 775, 'Correo: mitaller@mail.com')
            self.report.drawString(150, 765, 'Teléfono: 987654321')



        except Exception as error:
            print('Error de cabecera: '+str(error))

    def cuerpoInformeCliente(self):
        items = ['DNI', 'Nombre', 'Dirección', 'Provincia', 'Municipio']

        query = QtSql.QSqlQuery()
        query.prepare('select dni, nombre, direccion, provincia, municipio '
                      'from clientes order by nombre')



        self.report.setFont('Helvetica', size=8)

        if query.exec():
            i = 60
            j = 630
            while query.next():
                if j <= 80:
                    self.report.drawString(460, 90, 'Página siguiente...')
                    self.report.showPage()
                    self.topInforme()
                    self.pieInforme()
                    self.report.line(50, 660, 525, 660)
                    self.report.setFont('Helvetica-Bold', size=10)
                    self.report.drawString(60, 650, items[0])
                    self.report.drawString(120, 650, items[1])
                    self.report.drawString(270, 650, items[2])
                    self.report.drawString(360, 650, items[3])
                    self.report.drawString(460, 650, items[4])
                    self.report.line(50, 645, 525, 645)

                self.report.setFont('Helvetica', size=8)
                censura = ""
                dni = query.value(0)
                for x in range(9):
                    if x < 5:
                        censura = censura + '*'
                    elif ((x >= 5) and (x < 8)):
                        censura = censura + dni[x]
                    elif x == 8:
                        censura = censura + '*'

                self.report.drawString(i, j, str(censura))
                self.report.drawString(i + 60, j, str(query.value(1)))
                self.report.drawString(i + 210, j, str(query.value(2)))
                self.report.drawString(i + 300, j, str(query.value(3)))
                self.report.drawString(i + 400, j, str(query.value(4)))
                j = j - 20

    def cuerpoInformeCoche(self):
        items = ['DNI', 'Matrícula', 'Marca', 'Modelo', 'Motor']

        query = QtSql.QSqlQuery()
        query.prepare('select dniCli, matricula, marca, modelo, motor '
                      'from coches order by marca')

        self.report.setFont('Helvetica', size=8)

        if query.exec():
            i = 60
            j = 630
            while query.next():
                if j <= 80:
                    self.report.drawString(460, 90, 'Página siguiente...')
                    self.report.showPage()
                    self.topInforme()
                    self.pieInforme()
                    self.report.line(50, 660, 525, 660)
                    self.report.setFont('Helvetica-Bold', size=10)
                    self.report.drawString(60, 650, items[0])
                    self.report.drawString(120, 650, items[1])
                    self.report.drawString(270, 650, items[2])
                    self.report.drawString(360, 650, items[3])
                    self.report.drawString(460, 650, items[4])
                    self.report.line(50, 645, 525, 645)

                self.report.setFont('Helvetica', size=8)

                censura = ""
                dni = query.value(0)
                for x in range(9):
                    if x < 5:
                        censura = censura + '*'

                    if ((x >= 5) and (x < 8)):
                        censura = censura + dni[x]


                    if x == 8:
                        censura = censura + '*'



                self.report.drawString(i, j, str(censura))
                self.report.drawString(i + 60, j, str(query.value(1)))
                self.report.drawString(i + 210, j, str(query.value(2)))
                self.report.drawString(i + 300, j, str(query.value(3)))
                self.report.drawString(i + 400, j, str(query.value(4)))
                j = j - 20



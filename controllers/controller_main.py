import calendar

import xlrd as xlrd
import xlwt
from PyQt6 import QtWidgets, QtSql, QtCore
from PyQt6.QtGui import QIcon
from reportlab.pdfgen import canvas

from views import Ui_venMain
from controllers import DialogoSalir, DialogoDatos, DialogCalendar, DialogoHistorico
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
        indice = 0

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

        self.ui.btnHist.clicked.connect(self.abrirHistorico)                    # === abre el hist??rico === #

        self.ui.btnFacturar.clicked.connect(self.facturar)                      # === a??ade una factura === #

        self.ui.btnImprimirFac.clicked.connect(self.factura)                    # === imprime la factura === #

        self.ui.btnBorrarFac.clicked.connect(self.borrarFactura)                # === borra la factura === #

        self.ui.btnBusqFac.clicked.connect(self.buscarFacturaPorDNI)            # === busca la factura === #

        self.ui.btnRecargaFac.clicked.connect(self.limpiarCasillasFactura)      # === limpia las casillas factura === #



        '''
        Listado de eventos de cajas del formulario
        '''
        self.ui.txtDniCli.editingFinished.connect(self.mostrarValidezDNI)       # === comprueba el DNI === #

        self.ui.txtNombreCli.editingFinished.connect(self.letrasCapital)        # === pone las may??sculas === #

        self.ui.txtDirCli.editingFinished.connect(self.letrasCapital)           # === pone las may??sculas === #

        self.ui.txtMatr.editingFinished.connect(self.letrasCapital)             # === pone las may??sculas === #

        self.ui.txtModelo.editingFinished.connect(self.letrasCapital)           # === pone las may??sculas === #

        '''
        Llamadas a funciones varias
        '''
        self.selMotor()                                                         # === asegura el motor === #

        self.conexion()                                                         # === conexi??n con la base === #

        self.cargarProvincia()                                                  # === llena las provincias === #

        self.mostrarTabCocheCli()                                               # === muestra la tabla de coches === #

        self.mostrarTabProductos()                                              # === muestra la tabla productos === #

        #self.cargarTabHistorico()                                               # === muestra la tabla hist??rico === #

        self.restructuracionTablaCocheCli()                                     # === reestructura la tabla coches === #

        self.ui.cmbProCli.currentIndexChanged.connect(self.cargarMunicipio)     # === llena los municipios ===#

        self.mostrarTabFacturas()                                               # === muestra la tabla de facturas === #

        self.ui.tabFac.clicked.connect(self.cargarFactura)                      # === carga los datos de facturas === #

        self.ui.tabCli.clicked.connect(self.cargarClienteEnFactura)             # === carga los datos de facturas === #

        self.alinearTablaVentas()                                               # === alinea la tabla de ventas === #

        self.alinearTablaFacturas()                                             # === alinea la tabla de facturas === #

        self.alinearTablaServicios()                                            # === alinea la tabla de servicios === #

        self.ui.tabFac.clicked.connect(self.cargarVentas)                       # === carga las ventas del cliente === #

        self.ui.btnImprimirFac.clicked.connect(self.factura)

        '''
        Llamadas a funciones de servicios (examen)
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
    
                                                    M  ??  T  O  D  O  S
    
    ========================================================================================================================
    '''

    def salir(self):
        """

        Sale del programa.

        """
        try:
            self.avisosalir.show()
            if self.avisosalir.exec():
                sys.exit()
            else:
                self.avisosalir.hide()

        except Exception as error:
            print(error)

    def abrirCalendario(self):
        """

        Abre el calendario.

        """
        try:
            self.dlgcalendar.show()
            self.dlgcalendar.ui.calendario.clicked.connect(self.cargarFecha)
        except Exception as error:
            print(error)

    def letrasCapital(self):
        """

        Pone la primera letra en may??scula de los datos del cliente.

        """
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
        """

        Reestructura el tama??o de la tabla de coches.

        """
        try:
            header = self.ui.tabCli.horizontalHeader()
            for i in range(5):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                if i == 0 or i == 1:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        except Exception as error:
            print(error)

    def creaBackup(self):
        """

        Crea un Backup.

        """
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
                msg.setText('Copia creada con ??xito.')
                msg.exec()

        except Exception as error:
            print(error)

    def restauraBackup(self):
        """

        Restaura un Backup.

        """
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
        """

        Exporta los datos.

        """
        try:

            ventana = self.avisoDatos

            ventana.show()



        except Exception as error:
            print("Error exportar datos", error)

    def validarDNI(self, dni):
        '''
        M??dulo para la validaci??n de DNI

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
        """

        Muestra al lado de la caja del dni si ??ste es v??lido o no.

        """
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
        """

        Selecciona el motor y pasa la selecci??n a la funci??n cheMotor.

        """
        try:
            self.motor = (self.ui.rbtGas, self.ui.rbtDie, self.ui.rbtHib, self.ui.rbtEle)
            for i in self.motor:
                i.toggled.connect(self.cheMotor)
        except Exception as error:
            print(error)

    def cheMotor(self):
        """

        Iguala cada selecci??n a un motor y lo devuelve.

        :return: motor
        """
        try:
            if self.ui.rbtGas.isChecked():
                motor = "Gasolina"
            elif self.ui.rbtDie.isChecked():
                motor = "Di??sel"
            elif self.ui.rbtHib.isChecked():
                motor = "H??brido"
            elif self.ui.rbtEle.isChecked():
                motor = "El??ctrico"
            else:
                pass
            return motor
        except Exception as error:
            print(error)

    def guardarCli(self):
        """

        Guarda un cliente en la base de datos.

        """
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
        """

        Limpia las cajas de informaci??n del cliente.

        """
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
        """

        Carga la informaci??n de un cliente de la base de datos.

        """
        try:
            despleMun = self.ui.cmbMunCli
            desplePro = self.ui.cmbProCli
            self.limpiaCli()
            fila = self.ui.tabCli.selectedItems()
            datos = [self.ui.txtDniCli, self.ui.txtMatr, self.ui.txtMarca, self.ui.txtModelo]
            row = [dato.text() for dato in fila]

            for i, dato in enumerate(datos):
                dato.setText(row[i])

            if row[4] == 'Di??sel':
                self.ui.rbtDie.setChecked(True)
            elif row[4] == 'Gasolina':
                self.ui.rbtGas.setChecked(True)
            elif row[4] == 'H??brido':
                self.ui.rbtHib.setChecked(True)
            elif row[4] == 'El??ctrico':
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
        """

        Carga la fecha seleccionada en el calendario.

        """
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
        """

        Crea la conexi??n con la base de datos.

        :return: booleano
        """
        filedb = 'bases/bbdd.sqlite'
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(filedb)
        self.bbdd = 'bbdd.sqlite'

        if not db.open():
            QtWidgets.QMessageBox.critical(None, "No se ha podido abrir la base. Conexi??n no establecida.\n",
                                           "Haga click para cerrar.", QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

        else:
            print("Conexi??n establecida.")
            return True

    def cargarProvincia(self):
        """

        Carga las provincias en el desplegable.

        """
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
        """

        Carga los municipios en el desplegable.

        """
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
        """

        Da de alta a un cliente.

        :param newcli: El nuevo cliente.
        :param newcar: El nuevo coche.
        """
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
                'insert into coches (matricula, dniCli, marca, modelo, motor) '
                '   values (:matricula, :dniCli, :marca, :modelo, :motor)')
            query2.bindValue(":matricula", str(newcar[0]))
            query2.bindValue(":dniCli", str(newcli[0]))
            query2.bindValue(":marca", str(newcar[1]))
            query2.bindValue(":modelo", str(newcar[2]))
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
        """

        Carga los datos en la tabla de coches.

        """
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
        """

        Realiza una consulta por dni.

        :param dni: el dni.
        :return: una lista con la informaci??n.
        """
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
        """

        Borra a un cliente de la base de datos.

        """
        try:



            query1 = QtSql.QSqlQuery()
            query1.prepare('delete from coches where matricula = :matr')
            query1.bindValue(':matr', str(self.ui.txtMatr.text()))

            query2 = QtSql.QSqlQuery()
            query2.prepare('select * from coches where matricula = :matr')
            query2.bindValue(':matr', str(self.ui.txtMatr.text()))



            tabla = self.dlgHistorico.ui.tabBajas
            indice = 0

            if query2.exec():
                while query2.next():
                    tabla.setRowCount(indice + 1)
                    tabla.setItem(0, 0, QtWidgets.QTableWidgetItem(str(query2.value(1))))
                    tabla.setItem(0, 1, QtWidgets.QTableWidgetItem(str(query2.value(0))))
                    tabla.setItem(0, 2, QtWidgets.QTableWidgetItem(str(query2.value(2))))
                    tabla.setItem(0, 3, QtWidgets.QTableWidgetItem(str(query2.value(3))))
                    tabla.setItem(0, 4, QtWidgets.QTableWidgetItem(str(query2.value(4))))
                    tabla.setItem(0, 5, QtWidgets.QTableWidgetItem(str(datetime.today())))
                    indice = indice + 1

                    query3 = QtSql.QSqlQuery()
                    query3.prepare('insert into historicoches (matricula, dniCli, marca, modelo, motor, fecha) '
                                   '   values (:matricula, :dniCli, :marca, :modelo, :motor, :fecha)')
                    query3.bindValue(":matricula", str(query2.value(1)))
                    query3.bindValue(":dniCli", str(query2.value(0)))
                    query3.bindValue(":marca", str(query2.value(2)))
                    query3.bindValue(":modelo", str(query2.value(3)))
                    query3.bindValue(":motor", str(query2.value(4)))
                    query3.bindValue(":fecha", str(datetime.today()))
                query3.exec()
                query1.exec()



            if query1.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('ALERTA')
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText('Baja completada')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("ALERTA")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query1.lastError().text())
                msg.exec()

            self.mostrarTabCocheCli()



        except Exception as error:
            print(error)

    def importarDatos(self):
        """

        Importa los datos.

        """
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
        """

        Modifica un cliente de la base de datos llamando al m??todo que hace las consultas.

        """
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
        """

        Realiza las consultas para modificar el cliente.

        :param modClient: cliente a modificar.
        :param modCar: coche a modificar.
        """
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

    def abrirHistorico(self):
        """

        Abre la ventana del hist??rico.

        """
        try:
            self.dlgHistorico.show()
            self.dlgHistorico.cargarTabHistorico()
            self.dlgHistorico.alinearTablaHistorico()

        except Exception as error:
            print(error)

    def mostrarTabProductos(self):
        """

        Carga los productos en la tabla.

        """
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
        """

        Elimina un producto de la base de datos.

        """
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
        """

        Carga los datos de un producto de la base de datos en las casillas de informaci??n.

        """
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
        """

        Modifica un producto de la base de datos.

        """
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
        """

        Crea un producto en la base de datos.

        """
        try:


            newprod = []
            producto = [self.ui.txtConcepto, self.ui.txtPrecio]
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
                msg.setText("Producto a??adido")
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Aviso")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()


            self.mostrarTabProductos()
            self.cmbServicio.addItem(str(newprod[0]))

        except Exception as error:
            print(error)

    def exportaProd(self):
        """

        Exporta un producto de la base de datos.

        """
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
        msg.setText('Exportaci??n de datos realizada con ??xito')
        msg.exec()

    def crearInformeCli(self):
            """

            Crea el informe del cliente.

            """
            try:
                self.titulo = 'LISTA DE CLIENTES'

                dir, file = QtWidgets.QFileDialog().getSaveFileName(None, 'Guardar Datos', "Listado", '.pdf')
                self.report = canvas.Canvas(dir+file)

                self.report.drawString(230,700, 'LISTA DE CLIENTES')
                items = ['DNI', 'Nombre', 'Direcci??n', 'Provincia', 'Municipio']
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


            except Exception as error:
                print('Error informes estado clientes: '+ str(error))
            
    def crearInformeAuto(self):
        """

        Crea el informe del coche.

        """
        try:
            self.titulo = 'LISTA DE VEH??CULOS'
            dir, file = QtWidgets.QFileDialog().getSaveFileName(None, 'Guardar Datos', "Listado", '.pdf')
            self.report = canvas.Canvas(dir + file)
            self.report.drawString(230, 700, 'LISTA DE VEH??CULOS')
            items = ['DNI', 'Matr??cula', 'Marca', 'Modelo', 'Motor']
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
        """

        Crea el pie de los informes.

        """
        try:
            self.report.line(50,50,525,50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d.%m.%Y %H:%M:%S')
            self.report.setFont('Helvetica-Oblique', size=7)
            self.report.drawString(50,40, str(fecha))
            self.report.drawString(250, 40, str(self.titulo))
            self.report.drawString(475, 40, 'P??gina {}'.format(self.report.getPageNumber()))
        except Exception as error:
            print('Error pie de informe de cualquier tipo: '+str(error))

    def topInforme(self):
        """

        Crea la cabecera de los informes.

        """
        try:

            logo = '.\img\logo.jpg'
            self.report.line(50, 800, 525, 800)
            self.report.line(50, 720, 525, 720)
            self.report.setFont('Helvetica-Bold', size=14)
            self.report.drawImage(logo, 15, 680, width=120, height=150)
            self.report.drawString(230, 815, 'Taller Mec??nico Teis')
            self.report.drawImage(logo, 460, 680, width=120, height=150)

            self.report.setFont('Helvetica', size=9)
            self.report.drawString(150, 785, 'CIF: A12345678')
            self.report.drawString(350, 785, 'Avda. Galicia - 101')
            self.report.drawString(350, 775, 'Vigo - 36216 - Espa??a')
            self.report.drawString(150, 775, 'Correo: mitaller@mail.com')
            self.report.drawString(150, 765, 'Tel??fono: 987654321')



        except Exception as error:
            print('Error de cabecera: '+str(error))

    def cuerpoInformeCliente(self):
        """

        Crea el cuerpo del informe del cliente.

        """
        items = ['DNI', 'Nombre', 'Direcci??n', 'Provincia', 'Municipio']

        query = QtSql.QSqlQuery()
        query.prepare('select dni, nombre, direccion, provincia, municipio '
                      'from clientes order by nombre')



        self.report.setFont('Helvetica', size=8)

        if query.exec():
            i = 60
            j = 630
            while query.next():
                if j <= 80:
                    self.report.drawString(460, 90, 'P??gina siguiente...')
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
        """

        Crea el cuerpo del informe del coche.

        """
        items = ['DNI', 'Matr??cula', 'Marca', 'Modelo', 'Motor']

        query = QtSql.QSqlQuery()
        query.prepare('select dniCli, matricula, marca, modelo, motor '
                      'from coches order by marca')

        self.report.setFont('Helvetica', size=8)

        if query.exec():
            i = 60
            j = 630
            while query.next():
                if j <= 80:
                    self.report.drawString(460, 90, 'P??gina siguiente...')
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
        items = ['DNI', 'Nombre', 'Direcci??n', 'Provincia', 'Municipio']

        query = QtSql.QSqlQuery()
        query.prepare('select dniCli, matricula, marca, modelo, motor '
                      'from coches order by marca')



        self.report.setFont('Helvetica', size=8)

        if query.exec():
            i = 60
            j = 630
            while query.next():
                if j <= 80:
                    self.report.drawString(460, 90, 'P??gina siguiente...')
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

    def mostrarTabFacturas(self):
        """

        Carga en la tabla de facturas las facturas de la base de datos.

        """
        tabla = self.ui.tabFac
        indice = 0

        query = QtSql.QSqlQuery()
        query.prepare("select id_factura, matrAuto from facturas")

        if query.exec():
            while query.next():
                tabla.setRowCount(indice + 1)

                tabla.setItem(indice, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
                tabla.setItem(indice, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))


                indice = indice + 1

    def cargarClienteEnFactura(self):
        """

        Carga un cliente en una factura.

        """
        try:
            fila = self.ui.tabCli.selectedItems()
            row = [dato.text() for dato in fila]



            self.ui.txtMatrFac.setText(str(row[1]))
            self.ui.textBoxDniCliFac.setText(str(row[0]))
            data = datetime.today()
            self.ui.txtFechaCliFac.setText(str(data))

        except Exception as error:
            print(error)

    def cargarFactura(self):
        """

        Carga los datos de una factura en las casillas de informaci??n.

        """
        try:
            fila = self.ui.tabFac.selectedItems()
            row = [dato.text() for dato in fila]



            self.ui.txtMatrFac.setText(str(row[1]))
            self.ui.txtNumFac.setText(str(row[0]))
            query = QtSql.QSqlQuery()
            query.prepare('select dniCli, fechaFac from facturas where id_factura = :num')
            query.bindValue(':num', str(row[0]))
            print(query.value(0))



            if query.exec():
                while query.next():
                    self.ui.textBoxDniCliFac.setText(str(query.value(0)))
                    self.ui.txtFechaCliFac.setText(str(query.value(1)))
        except Exception as error:
            print(error)

    def facturar(self):
        """

        Crea una nueva factura en la base de datos.

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'insert into facturas (dniCli, matrAuto, fechaFac) values (:dni, :matr, :fecha)')
            query.bindValue(":dni", str(self.ui.textBoxDniCliFac.text()))
            query.bindValue(":matr", str(self.ui.txtMatrFac.text()))
            query.bindValue(":fecha", str(self.ui.txtFechaCliFac.text()))

            if query.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Aviso")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText("Factura impuesta")
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Aviso")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

            self.mostrarTabFacturas()

        except Exception as error:
            print(error)

    def borrarFactura(self):
        """

        Borra una factura de la base de datos.

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'delete from facturas where id_factura = :num')
            query.bindValue(":num", int(self.ui.txtNumFac.text()))

            if query.exec():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Aviso")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText("Factura borrada")
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Aviso")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

            self.mostrarTabFacturas()
        except Exception as error:
            print(error)

    def cargaLineaVenta(self, index):
        """

        Carga las l??neas de venta en la tabla de facturas.

        :param index: ??ndice est??tico.
        """
        try:
            self.cmbServicio = QtWidgets.QComboBox()
            self.cmbServicio.setFixedSize(172, 30)
            self.txtUnidades = QtWidgets.QLineEdit()
            self.txtUnidades.setFixedSize(100,30)
            self.txtUnidades.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.txtPrecio = QtWidgets.QLineEdit()
            self.txtPrecio.setFixedSize(100, 30)
            self.txtPrecio.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.txtPrecio.setReadOnly(True)
            self.txtTotal = QtWidgets.QLineEdit()
            self.txtTotal.setFixedSize(100, 30)
            self.txtTotal.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.txtTotal.setReadOnly(True)
            self.ui.tabVentas.setRowCount(index+1)

            self.ui.tabVentas.setCellWidget(index,1, self.cmbServicio)
            self.ui.tabVentas.setCellWidget(index,2, self.txtPrecio)
            self.ui.tabVentas.setCellWidget(index,3, self.txtUnidades)
            self.ui.tabVentas.setCellWidget(index, 4, self.txtTotal)
            self.cargaComboVentas()
            self.cmbServicio.currentIndexChanged.connect(self.cargarPrecioVentas)
            self.txtUnidades.editingFinished.connect(self.totalLineaVenta)
            self.ui.tabVentas.resizeColumnsToContents()
        except Exception as error:
            print('Hay un error en las l??neas: '+str(error))

    def cargaComboVentas(self):
        """

        Carga los productos en el desplegable de las l??neas de ventas.

        """
        try:
            self.cmbServicio.clear()
            query = QtSql.QSqlQuery()
            query.prepare('select servicio from servicios order by servicio')
            if query.exec():
                while query.next():
                    self.cmbServicio.addItem(str(query.value(0)))
        except Exception as error:
            print(error)

    def cargarPrecioVentas(self):
        """

        Carga el precio de cada producto en la tabla de facturas.

        """
        try:
            tabla = self.ui.tabVentas
            row = self.ui.tabVentas.currentRow()
            print(row)
            servicio = self.cmbServicio.currentText()
            precio = self.obtenerPrecio(servicio)
            precio = precio.replace('.',',')
            precio = precio + '???'
            self.txtPrecio.setText(precio)
            self.txtPrecio.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        except Exception as error:
            print("precio: "+str(error))

    def totalLineaVenta(self):
        """

        Carga el precio total a pagar por los productos de un mismo tipo.

        """
        try:
            row = self.ui.tabVentas.currentRow()
            precio = self.txtPrecio.text().replace(',', '.')
            precio = precio.replace('???', '0')
            print(precio)
            cantidad = self.txtUnidades.text()
            print(cantidad)
            total = float(precio)*float(cantidad)
            total = str(total).replace('.', ',')+'???'
            self.txtTotal.setText(total)
            self.txtTotal.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            venta = []
            venta.append(int(self.ui.txtNumFac.text()))

            query = QtSql.QSqlQuery()
            query.prepare('select id from servicios where servicio = :nombre')
            query.bindValue(":nombre", str(self.cmbServicio.currentText()))
            if query.exec():
                while query.next():
                    venta.append(int(query.value(0)))
            venta.append(float(self.txtUnidades.text()))
            venta.append(float(self.txtPrecio.text().replace(',','.').replace('???','0')))

            self.registrarVenta(venta)
            self.cargarVentas()


        except Exception as error:
            print("total: "+str(error))

    def registrarVenta(self, venta):
        """

        Registra cada venta en la base de datos.

        :param venta: lista con los datos de la venta.
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into ventas (facturaId, servicioId, cantidad, precio) VALUES (:codFac, :codSer, :canti, :precio)')
            query.bindValue(":codFac", int(venta[0]))
            query.bindValue(":codSer", int(venta[1]))
            query.bindValue(":canti", int(venta[2]))
            query.bindValue(":precio", int(venta[3]))

            if query.exec():
                print('L??nea de venta realizada')
        except Exception as error:
            print('reigistro: '+str(error))

    def obtenerPrecio(self, servicio):
        """

        Obtiene el precio de cada servicio.

        :param servicio:
        :return:
        """
        try:
            precio = ""
            query = QtSql.QSqlQuery()
            query.prepare('select precio from servicios where servicio = :servicio')
            query.bindValue(':servicio', str(servicio))
            if query.exec():
                while query.next():
                    precio = str(query.value(0))
            return precio
        except Exception as error:
            print('obtenci??n de precio: '+str(error))

    def alinearTablaVentas(self):
        """

        Ajusta el tama??o de la tabla de ventas.

        """
        try:
            header = self.ui.tabVentas.horizontalHeader()
            for i in range(header.model().columnCount()):
                header.setSectionResizeMode(i,QtWidgets.QHeaderView.ResizeMode.Stretch)
                if i ==0:
                    header.setSectionResizeMode(i,QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        except Exception as error:
            print(error)

    def alinearTablaFacturas(self):
        """

        Ajusta el tama??o de la tabla de facturas.

        """
        try:
            header = self.ui.tabFac.horizontalHeader()
            for i in range(header.model().columnCount()):
                header.setSectionResizeMode(i,QtWidgets.QHeaderView.ResizeMode.Stretch)
                if i ==0:
                    header.setSectionResizeMode(i,QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        except Exception as error:
            print(error)

    def cargarVentas(self):
        """

        Carga las ventas en cada factura.

        """
        try:
            tabla_ventas = self.ui.tabVentas
            self.limpiaTabla(tabla_ventas)
            self.ui.txtPrecioTotal.setText('')
            self.cargaLineaVenta(0)
            indice = 1
            suma = 0
            total = 0
            query = QtSql.QSqlQuery()
            query.prepare('select idVentas, servicioId, precio, cantidad from ventas where facturaId = :numFac')
            query.bindValue(':numFac', int(self.ui.txtNumFac.text()))
            if query.exec():
                while query.next():
                    id = str(query.value(0))
                    precio = str('{:.2f}'.format(round(query.value(2),2)))+' ???'
                    cantidad = str('{:.2f}'.format(round(query.value(3),2)))
                    servicio = self.buscarServicio(round(query.value(1)))
                    suma = str('{:.2f}'.format(round(query.value(2)*query.value(3), 2)))
                    total = total + float(suma)
                    self.btnBorrarLinea = QtWidgets.QPushButton()
                    self.btnBorrarLinea.setFixedSize(30, 30)
                    self.btnBorrarLinea.clicked.connect(self.borrarLineaVenta)
                    tabla_ventas.setRowCount(indice+1)
                    tabla_ventas.setItem(indice, 0, QtWidgets.QTableWidgetItem(str(id)))
                    tabla_ventas.item(indice, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    tabla_ventas.setItem(indice, 1, QtWidgets.QTableWidgetItem(str(servicio)))
                    tabla_ventas.item(indice, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    tabla_ventas.setItem(indice, 2, QtWidgets.QTableWidgetItem(str(precio).replace('.',',')))
                    tabla_ventas.item(indice, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    tabla_ventas.setItem(indice, 3, QtWidgets.QTableWidgetItem(str(cantidad).replace('.',',')))
                    tabla_ventas.item(indice, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    tabla_ventas.setItem(indice, 4, QtWidgets.QTableWidgetItem(str(suma) + ' ???'))
                    tabla_ventas.item(indice, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    tabla_ventas.setCellWidget(indice, 5, self.btnBorrarLinea)
                    self.btnBorrarLinea.setIcon(QIcon("img\decoraciones\papelera.png"))

                    self.ui.txtPrecioTotal.setText(str('{:.2f}'.format(round(total)))+' ???')
                    indice = indice + 1
                    tabla_ventas.resizeColumnsToContents()



        except Exception as error:
            print("cargar l??nea: "+str(error))

    def borrarLineaVenta(self):
        """

        Elimina una l??nea de venta.

        """
        try:
            fila = self.ui.tabVentas.selectedItems()
            row = [dato.text() for dato in fila]
            print(row)
            id = str(row[0])
            print(id)
            query = QtSql.QSqlQuery()
            query.prepare('delete from ventas where idVentas = :id')
            query.bindValue(":id", str(id))

            if query.exec():

                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Aviso")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.setText("Factura borrada")
                msg.exec()
                self.cargarVentas()

        except Exception as error:
            print("Error en borrado de ventas: "+str(error))

    def buscarServicio(self, num):
        """

        Busca los servicios.

        :param num: id del servicio
        :return: devuelve el servicio
        """
        try:
            servicio = ""
            query = QtSql.QSqlQuery()
            query.prepare('select servicio from servicios where id = :numSer')
            query.bindValue(":numSer", int(num))
            if query.exec():
                while query.next():
                    servicio = query.value(0)
            return servicio
        except Exception as error:
            print(error)

    def limpiarCasillasFactura(self):
        """

        Limpia las casillas de informaci??n de las facturas.

        """
        try:
            self.ui.txtFechaCliFac.setText("")
            self.ui.txtMatrFac.setText("")
            self.ui.textBoxDniCliFac.setText("")
            self.ui.txtNumFac.setText("")
            self.limpiaTabla(self.ui.tabVentas)
        except Exception as error:
            print(error)

    def buscarFacturaPorDNI(self):
        """

        Busca las facturas por el dni.

        """
        try:
            tabla = self.ui.tabFac
            indice = 0
            dni = self.ui.txtBucarFac.text()
            tabla.clear()

            query = QtSql.QSqlQuery()
            if dni != "":
                query.prepare("select id_factura, matrAuto from facturas where dniCli = :dni")
                query.bindValue(":dni", str(dni))
            else:
                self.mostrarTabFacturas()

            if query.exec():
                while query.next():
                    tabla.setRowCount(indice + 1)

                    tabla.setItem(indice, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
                    tabla.setItem(indice, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))

                    indice = indice + 1
        except Exception as error:
            print(error)

    def alinearTablaServicios(self):
            """

            Ajusta el tama??o de la tabla de servicios.

            """
            try:
                header = self.ui.tabProd.horizontalHeader()
                for i in range(header.model().columnCount()):
                    header.setSectionResizeMode(i,QtWidgets.QHeaderView.ResizeMode.Stretch)
                    if i == 0:
                        header.setSectionResizeMode(i,QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            except Exception as error:
                print(error)

    def limpiaTabla(self, tabla):
        """

        Limpia la tabla objetivo.

        :param tabla: tabla que se desea limpiar.
        """
        try:
            tabla.clearContents()
        except Exception as error:
            print(error)

    def factura(self):
        """

        Imprime una factura en pdf.

        """
        self.report = canvas.Canvas("informes/factura.pdf")
        titulo = "FACTURA"
        self.pieInforme()
        self.topInforme()

        items = ['ID', 'Servicio', 'Precio', 'Unidades', 'Total']

        cliente = []
        dni=str(self.ui.textBoxDniCliFac.text())
        cliente = self.consultaDni(dni)
        print(cliente)
        num = str(self.ui.txtNumFac.text())

        i = 60
        j = 530

        self.report.setFont('Helvetica',size=14)
        self.report.drawString(270, 695, titulo)
        self.report.line(45, 680, 550, 680)

        self.report.setFont('Helvetica', size=9)
        self.report.drawString(55, 660, 'DATOS DEL CLIENTE')
        self.report.drawString(450, 660, 'N?? de factura: '+str(num))
        self.report.drawString(55, 640, 'DNI/CIF: ' + str(dni))
        self.report.drawString(55, 625, 'Nombre: ' + str(cliente[0]))
        self.report.drawString(55, 610, 'Direcci??n: ' + str(cliente[1]))
        self.report.drawString(55, 595, 'Provincia: ' + str(cliente[3]))
        self.report.drawString(55, 580, 'Municipio: ' + str(cliente[4]))

        self.report.line(45, 570, 550, 570)

        self.report.line(45, 560, 550, 560)
        self.report.setFont('Helvetica-Bold', size=10)
        self.report.drawString(60, 550, items[0])
        self.report.drawString(120, 550, items[1])
        self.report.drawString(270, 550, items[2])
        self.report.drawString(360, 550, items[3])
        self.report.drawString(460, 550, items[4])
        self.report.line(45, 545, 550, 545)

        query = QtSql.QSqlQuery()
        query.prepare('select idVentas, servicioId, cantidad, precio from ventas where facturaId = :fac')
        query.bindValue(":fac", str(num))

        if query.exec():
            while query.next():
                query2 = QtSql.QSqlQuery()
                query2.prepare('select servicio from servicios where id = :id')
                query2.bindValue(":id", str(query.value(1)))
                query2.exec()
                while query2.next():
                    self.report.drawString(i, j, str(query.value(0)))
                    self.report.drawString(i + 60, j, str(query2.value(0)))
                    self.report.drawString(i + 210, j, str(query.value(3)))
                    self.report.drawString(i + 300, j, str(query.value(2)))
                    self.report.drawString(i + 400, j, str(int(query.value(3))*int(query.value(2))))
                    j = j - 20


        self.report.save()
        rootPath = '.\\informes'
        for file in os.listdir(rootPath):
            if file.endswith('factura.pdf'):
                os.startfile('%s/%s' % (rootPath, file))



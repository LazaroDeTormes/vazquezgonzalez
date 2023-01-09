import sys
from PyQt6 import QtWidgets
from controllers import Main


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())




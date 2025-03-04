from PyQt5.QtWidgets import QApplication
from gui.gui import GUI
import sys

def run():
    app = QApplication(sys.argv)
    ventana = GUI()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()
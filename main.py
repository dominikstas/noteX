import sys
from PyQt5.QtWidgets import QApplication
from ui import UiClass

#running program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UiClass()
    ui.show()
    sys.exit(app.exec_())
import sys

from PyQt5 import QtWidgets

from MainWindow import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(app=app)
    window.show()
    try:
        app.exec_()
        print('App closed by user')
        sys.exit()
    except KeyboardInterrupt:
        print('App terminate by KeybaordInterrupt')
        sys.exit()
from PyQt4 import QtGui
from gui.app import SearchEventApp


def main():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    app = QtGui.QApplication(sys.argv)
    form = SearchEventApp()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()

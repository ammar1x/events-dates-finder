from PyQt4 import QtGui
from PyQt4 import QtCore
import logic


class QEventItemWidget(QtGui.QWidget):
    ''' Display custom list item in list widget '''
    def __init__(self, parent):
        super(QEventItemWidget, self).__init__(parent)
        # layout managers
        self.vBoxLayout = QtGui.QVBoxLayout()
        # labels
        self.titleLabel = QtGui.QLabel()
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setMaximumWidth(parent.width() - 30)

        self.dateLabel = QtGui.QLabel()
        self.dateLabel.setWordWrap(True)
        self.dateLabel.setMaximumWidth(parent.width() - 30)
        # add widgets
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.dateLabel)
        self.setLayout(self.vBoxLayout)

        # stylesheet for labels
        self.titleLabel.setStyleSheet(''' color: rgb(26,13,171) ''')
        self.dateLabel.setStyleSheet(''' color: rgb(13,171,26) ''')

    def set_text(self, text):
        self.titleLabel.setText(text)

    def set_date(self, date):
        self.dateLabel.setText(str(date))


class Worker(QtCore.QThread):
    '''Background thread for processing data - downloading pages, and
    extracting dates from them'''
    def __init__(self, query=None, n=10):
        QtCore.QThread.__init__(self)
        self.events = None
        self.query = query
        self.n = n
        self.exception = None

    def set_query(self, query, n=10):
        self.query = query
        self.n = n

    def __del__(self):
        self.wait()

    def run(self):
        self.events = []
        if self.query:
            try:
                self.events = logic.get_n_events(self.query, self.n)
                self.emit(QtCore.SIGNAL('worker_finished()'))
            except logic.EngineQueryError as er:
                print er
                self.exception = er
                self.emit(QtCore.SIGNAL('worker_error()'))
            except IOError as er:
                print er
                self.exception = er
                self.emit(QtCore.SIGNAL('worker_error()'))

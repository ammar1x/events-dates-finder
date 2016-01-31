from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
import searchUI
from helpers import QEventItemWidget, Worker
import logic


class SearchEventApp(QtGui.QMainWindow, searchUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(SearchEventApp, self).__init__(parent)
        self.setupUi(self)
        self.searchButton.clicked.connect(self.search_events)
        self.progressBar.setRange(0, 1)
        self.progressBar.setStyleSheet('''
QProgressBar
{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center;
}
QProgressBar::chunk
{
    background-color: #d7801a;
    width: 2.15px;
    margin: 0.5px;
}''')

        self.paint_cell_calendar_old = self.calendarWidget.paintCell
        self.calendarWidget.paintCell = self.paint_calendar_cell
        self.calendarWidget.clicked.connect(self.handle_date_clicked)

        # QtCore.QObject.connect(self.searchInput, QtCore.SIGNAL('keyPressed()'), self.search_events)
        self.searchInput.returnPressed.connect(self.search_events)

        self.worker = Worker()
        self.connect(self.worker, QtCore.SIGNAL("worker_finished()"), self.search_done)
        self.connect(self.worker, QtCore.SIGNAL("worker_error()"), self.search_error)

    def search_error(self):
        self.searchInput.setEnabled(True)
        self.searchButton.setEnabled(True)
        self.progressBar.setRange(0, 1)

        t = self.worker.exception

        msg = ""
        if isinstance(t, IOError):
            msg = "check your connection. Network is unreachable."
        elif isinstance(t, logic.EngineQueryError):
            msg = "cannot retrieve results. %s" % str(t)

        mbox = QtGui.QMessageBox(QtGui.QMessageBox.Critical, "Application error", msg)
        mbox.exec_()

    def handle_date_clicked(self, date):
        # TODO: handle date clicked
        print date

    def paint_calendar_cell(self, painter, rect, date):

        # TODO: handle drawing date
        # self.paint_cell_calendar_old(painter, rect, date)
        # self.calendarWidget.par.paintCell(self, painter, rect, date)

        painter.drawText(rect.topLeft() + QtCore.QPoint(20, 20), str(date.day()))
        text_option = QtGui.QTextOption()
        text_option.setWrapMode(QtGui.QTextOption.WordWrap)
        tests = ["hello world", "zlot milosnikow zlota", "wino i dziewczyny",
                 "klaendarz jest taki glupi ze tego sobie nie wyborazasz",
                 "kiedy w koncu zaczniesz pracowac",
                 "nie wiem co ja tutaj robie, nie wiem czym sie kierowac w zyciu",
                 "podstawa wszystkiego jest wiedza nabyta w sposob doswiadczalny, nie oznacza to jednak zawansowany"]
        if date.day() % 5 == 0:  # example condition based on date
            text = tests[date.day() % len(tests)]
            # if len(text) > 20:
            #     text = text[:17] + "..."
            #
            w = rect.width()
            h = rect.height()
            new_rect = QtCore.QRectF(rect)
            new_rect.setTopLeft(new_rect.topLeft() + QtCore.QPointF(0.1 * w, 0.5 * h))
            painter.drawText(new_rect, text, text_option)

    def search_done(self):

        # self.disconnect(self.worker, QtCore.SIGNAL('terminated()'), self.search_done)

        self.searchInput.setEnabled(True)
        self.searchButton.setEnabled(True)

        self.progressBar.setRange(0, 1)

        results = self.worker.results
        if results:
            self.listView.clear()
            i = 0

            for result in results:
                # setup event item look
                item = QEventItemWidget(self.listView)
                item.set_text(result.title)
                item.set_date(result.href)

                # some code that is necessary evil
                event_list_widget_item = QtGui.QListWidgetItem(self.listView)
                event_list_widget_item.setSizeHint(item.sizeHint())

                self.listView.addItem(event_list_widget_item)
                self.listView.setItemWidget(event_list_widget_item, item)

                i = (i + 1) % 2

    def search_events(self):

        self.searchInput.setEnabled(False)
        self.searchButton.setEnabled(False)

        self.worker.set_query(self.searchInput.text(), 10)
        self.worker.start()

        self.progressBar.setRange(0, 0)


def main():
    app = QtGui.QApplication(sys.argv)
    form = SearchEventApp()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()

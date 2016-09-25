import sys

from tab import get_tab_text
from main import get_tabs_for_search

from PyQt5.QtWidgets import (QApplication, QTextBrowser,
    QToolTip, QPushButton, QMessageBox, QDesktopWidget,
    QMainWindow, QWidget, QTableWidgetItem, QTableWidget,
    QLineEdit, QDialog)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize


class TabSelectButton(QPushButton):

    def __init__(self, label, parent=None):
        super(TabSelectButton, self).__init__(label, parent)

        def _empty_callback():
            pass

        self.clicked.connect(_empty_callback)
        self.show()

    def set_callback(self, fn, args):
        self.clicked.connect(lambda: fn(args))


class TabDisplayWindow(QDialog):
    def __init__(self, tab_text, parent=None):
        super(QDialog, self).__init__(parent)
        self.tab_text = tab_text
        self.initUI()

    def initUI(self):
        default_size = (600, 600)

        self.resize(*default_size)
        self.center()
        self.setWindowTitle("Tab Window")

        self.textShow = QTextBrowser(self)
        self.textShow.resize(*default_size)
        self.textShow.setText(self.tab_text)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        self.textShow.resize(event.size())

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Message',
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Yes)    # pre-selected

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class TabSelectWidget(QWidget):

    table_width = 4
    header_labels = ["Select", "Artist", "Tab-Name", "Type"]

    def __init__(self, parent=None):
        super(TabSelectWidget, self).__init__(parent)
        self.initUI()

        # List of tuples of the form
        # (artist, tab-name, type, url)
        self.tab_data = []

    def initUI(self):

        def do_search(query):
            self.tab_data = get_tabs_for_search(query)
            self.updateTable()

        self.resize(500, 500)

        self.search_text = QLineEdit("Enter Search Query", self)
        self.search_btn = QPushButton("Search", self)
        self.search_btn.clicked.connect(
            lambda: do_search(self.search_text.text()))
        self.search_text.move(self.search_btn.size().width(), 0)
        self.search_text.setMaximumWidth(300)
        self.search_text.setMinimumWidth(300)

        self.table = QTableWidget(0, self.table_width, self)
        self.table.setHorizontalHeaderLabels(self.header_labels)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        self.table.verticalHeader().hide()
        self.table.resize(500, 500)
        self.table.move(0, 25)

        self.show()

    def updateTable(self):
        for row_idx, row_data in enumerate(self.tab_data):
            self.table.insertRow(row_idx)

            def dummy_callback(url):
                tdw = TabDisplayWindow(get_tab_text(url))
                tdw.exec_()

            self.table.setCellWidget(
                row_idx, 0, TabSelectButton("SELECT", self))
            self.table.cellWidget(row_idx, 0).set_callback(
                dummy_callback, row_data[3])

            self.table.setItem(row_idx, 1, QTableWidgetItem(row_data[0]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(row_data[1]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(row_data[2]))

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

        self.all_modes = ["SEARCH", "SELECT", "DISPLAY"]
        self.mode = self.all_modes[0]

    def initUI(self):
        # Basic window size
        default_size = (600, 600)

        # TODO: Do we need Tooltips? This is how we do it
        # QToolTip.setFont(QFont('SansSerif', 10))
        # self.setToolTip('This is a <b>QWidget</b> widget')

        # TODO: Do we need a Statusbar? This is how we do it
        # self.statusBar().showMessage('Ready')

        def my_func(i):
            print("gello {}".format(i))

        # self.textShow = QTextBrowser(self)
        # self.textShow.resize(*default_size)
        # self.textShow.setText(get_tab_text())

        self.mainWidget = TabSelectWidget(self)

        self.resize(*default_size)
        self.center()
        self.setWindowTitle("Tooltips")
        self.setWindowIcon(QIcon("shroom.ico"))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        pass
        # self.table.resize(event.size())
        # self.textShow.resize(event.size())

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Message',
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Yes)    # pre-selected

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

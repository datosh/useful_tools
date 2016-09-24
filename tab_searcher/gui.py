import sys

from tab import get_tab_text

from PyQt5.QtWidgets import (QApplication, QTextBrowser,
    QToolTip, QPushButton, QMessageBox, QDesktopWidget,
    QMainWindow)
from PyQt5.QtGui import QIcon, QFont


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        default_size = (600, 600)

        QToolTip.setFont(QFont('SansSerif', 10))
        # self.setToolTip('This is a <b>QWidget</b> widget')

        self.statusBar().showMessage('Ready')

        def my_func():
            print("gello")

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        btn.clicked.connect(my_func)

        self.textShow = QTextBrowser(self)
        self.textShow.resize(*default_size)
        self.textShow.setText(get_tab_text())

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


def main():
    app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

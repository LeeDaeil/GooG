import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QGuiApplication
from main_ui_file import Ui_Form
from PySide2 import QtCore


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.temp = ''

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.send_text)
        timer.start(60)

    def send_text(self):
        text = self.ui.Read_contents.toPlainText()
        show_text = text.replace('\n', ' ')

        if show_text != self.temp:
            self.temp = show_text
            QGuiApplication.clipboard().clear()
            QGuiApplication.clipboard().setText(show_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

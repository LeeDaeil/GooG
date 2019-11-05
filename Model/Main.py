import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QGuiApplication
from PySide2 import QtWidgets
from PySide2 import QtCore, QtWebEngineWidgets


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1000, 500)
        self.Read_contents = QtWidgets.QPlainTextEdit(self)

        self.Read_contents.setGeometry(QtCore.QRect(5, 5, 990, 20))
        self.Read_contents.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.web = QtWebEngineWidgets.QWebEngineView(self)
        self.web.setGeometry(QtCore.QRect(5, 30, 990, 480))

        self.temp = ''

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.send_text)
        timer.start(60)

    def send_text(self):
        text = self.Read_contents.toPlainText()
        show_text = text.replace('\n', ' ')

        if show_text != self.temp:
            self.temp = show_text
            send_web_text = show_text.replace(' ', '%20')
            self.web.setUrl(QtCore.QUrl("https://translate.google.co.kr/?hl=ko#view=home&op=translate&sl=en&tl=ko&text={}".format(send_web_text)))

    def resizeEvent(self, e):
        self.web.setGeometry(QtCore.QRect(5, 30, self.geometry().width() - 10, self.geometry().height() - 20))
        self.Read_contents.setGeometry(QtCore.QRect(5, 5, self.geometry().width() - 10, 20))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # window = Form()
    window.show()
    sys.exit(app.exec_())

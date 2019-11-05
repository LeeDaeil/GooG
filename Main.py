from googletrans import Translator
import requests
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile
from main_ui_file import Ui_Form

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.translator = Translator()

        self.headers = {"X-Naver-Client-Id": "qakk9vZRtM6mjjBiYzAJ", "X-Naver-Client-Secret": "4UTOj98s46"}

        self.ui.Ok.clicked.connect(self.send_text)

    def send_text(self):
        text = self.ui.Read_contents.toPlainText()
        # out = self.translator.translate(text.replace('\n', ' '), src='en', dest='ko')
        params = {"source": "en", "target": "ko", "text": text.replace('\n', ' ')}
        response = requests.post("https://openapi.naver.com/v1/papago/n2mt", headers=self.headers, data=params)
        result = response.json()
        self.ui.Show_contents.setPlainText(result['message']['result']['translatedText'])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

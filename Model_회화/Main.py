import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide2.QtGui import QGuiApplication
from PySide2 import QtWidgets
from PySide2 import QtCore, QtWebEngineWidgets
import pandas as pd
import numpy as np
import re


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(800, 500)
        self.setWindowTitle('댈번역기, F1:데이터베이스')
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

    def keyPressEvent(self, e):
        if e.key() == 16777264: # F1 키로 호출
            self.serch_win = search_window()


class search_window(QMainWindow):
    def __init__(self):
        super(search_window, self).__init__()
        self.resize(600, 300)
        self.setWindowTitle('엔터:서치, F3:저장, F4:새로운열생성, F5:모든데이터보기')
        # 파일 존재 여부 체크 없음 새로 만들기
        # db col = {'K': '', 'E': ''}
        try:
            self.db = pd.read_pickle('db.pkl')
            print('Read DB file')
        except:
            print('No DB file and Make DB')
            self.db = pd.DataFrame([['테스트', 'Test'], ['비', 'a'], ['테스', 'a']], columns=['K', 'E'])
            #       K       E
            #   0   테스트   Test
            self.db.to_pickle('db.pkl')
        # 데이터 읽기 완료
        # ------------------------------------

        self.search_input_box = QtWidgets.QLineEdit(self)  # 1단 Search input box
        self.search_input_box.setGeometry(QtCore.QRect(5, 5, self.geometry().width() - 10, 30))
        
        # Tabel
        self.search_result_box = QtWidgets.QTableWidget(self)
        self.search_result_box.setWordWrap(True)    # 자동으로 줄 바꿈
        self.search_result_box.resizeRowsToContents()
        self.search_result_box.setGeometry(QtCore.QRect(5, 40, self.geometry().width() - 10,
                                                        self.geometry().height() - 50))
        self.search_result_box.setAlternatingRowColors(True)
        self.search_result_box.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)    # 1개 선택 가능
        self.search_result_box.cellChanged.connect(self.db_update_due_to_changed_val)
        self.search_result_box.setColumnCount(3)
        self.search_result_box.setHorizontalHeaderLabels(["DB_row", "Korea", "English"])

        # Tabel 열 너비
        self.search_result_box.setColumnWidth(0, 50)
        self.search_result_box.setColumnWidth(1, (self.search_result_box.geometry().width() - 50) / 2 - 10)
        self.search_result_box.setColumnWidth(2, (self.search_result_box.geometry().width() - 50) / 2 - 10)
        
        self.show()

    def db_update_due_to_changed_val(self):
        # cell 값 변경 시 db 업데이트 및 저장하기.
        selected_cell = self.search_result_box.currentIndex()
        if selected_cell.column() != -1:
            # 업데이트된 변수 찾기
            get_changed_db_index = self.search_result_box.item(selected_cell.row(), 0).text()   # get DB_row
            get_changed_db_k = self.search_result_box.item(selected_cell.row(), 1).text()       # get DB_row
            get_changed_db_e = self.search_result_box.item(selected_cell.row(), 2).text()       # get DB_row
            # db 업데이트
            self.db.loc[int(get_changed_db_index)] = [str(get_changed_db_k), str(get_changed_db_e)]
            # 저장하려면 F3 누르기

    def show_all_Db(self):
        self.search_result_box.clear()
        self.search_result_box.setHorizontalHeaderLabels(["DB_row", "Korea", "English"])

        get_searched_db = self.db
        self.search_result_box.setRowCount(len(get_searched_db))  # 데이터가 몇개가 존재하는지 테이블 row 선정

        # --- 찾은 데이터들을 표로 표기
        i = 0
        for nub_index in get_searched_db.index:
            item_k = QtWidgets.QTableWidgetItem()
            item_k.setText(get_searched_db.loc[nub_index].K)
            item_e = QtWidgets.QTableWidgetItem()
            item_e.setText(get_searched_db.loc[nub_index].E)
            item_row = QtWidgets.QTableWidgetItem()
            item_row.setText(str(nub_index))
            item_row.setFlags(QtCore.Qt.ItemIsEnabled)
            self.search_result_box.setItem(i, 0, item_row)
            self.search_result_box.setItem(i, 1, item_k)
            self.search_result_box.setItem(i, 2, item_e)
            i += 1
        # --- 찾은 데이터들을 표로 표기 end

    def update_table_from_search_input(self):
        # 현재 서치 박스의 text 기반으로 업데이트
        self.search_result_box.clear()
        self.search_result_box.setHorizontalHeaderLabels(["DB_row", "Korea", "English"])
        search_txt = self.search_input_box.text()
        if search_txt != '':
            # print(f'Search {search_txt}')                 # db 업데이트 확인용
            # table update
            get_searched_db = self.search_in_DB(search_txt)
            # print(get_searched_db)                        # db 업데이트 확인용
            # print(len(get_searched_db))                   # db 업데이트 확인용

            self.search_result_box.setRowCount(len(get_searched_db))    # 데이터가 몇개가 존재하는지 테이블 row 선정

            # --- 찾은 데이터들을 표로 표기
            i = 0
            for nub_index in get_searched_db.index:
                item_k = QtWidgets.QTableWidgetItem()
                item_k.setText(get_searched_db.loc[nub_index].K)
                item_e = QtWidgets.QTableWidgetItem()
                item_e.setText(get_searched_db.loc[nub_index].E)
                item_row = QtWidgets.QTableWidgetItem()
                item_row.setText(str(nub_index))
                item_row.setFlags(QtCore.Qt.ItemIsEnabled)
                self.search_result_box.setItem(i, 0, item_row)
                self.search_result_box.setItem(i, 1, item_k)
                self.search_result_box.setItem(i, 2, item_e)
                i += 1
            # --- 찾은 데이터들을 표로 표기 end

        else:
            print('No Search Value')
            mg = QMessageBox(text='No Search Value')
            mg.exec_()
            self.search_result_box.clear()          # 데이터 지우고
            self.search_result_box.setRowCount(0)   # 표 row 0 으로 초기화
        # 자동 줄 바꿈
        self.search_result_box.resizeRowsToContents()

    def search_in_DB(self, search_val):
        # db에서 찾고 싶은 파라메터를 추출해서 반환
        # print(self.db)
        hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', search_val))
        if hanCount > 0:
            return self.db[self.db.K.str.contains(search_val)]
        else:
            return self.db[self.db.E.str.contains(search_val)]

    def make_db(self):
        max_row = self.search_result_box.rowCount()
        self.search_result_box.setRowCount(max_row + 1)  # 데이터가 몇개가 존재하는지 테이블 row 선정
        # print(max_row)
        item_row = QtWidgets.QTableWidgetItem()
        item_row.setText(str(len(self.db)))
        item_row.setFlags(QtCore.Qt.ItemIsEnabled)
        item_k = QtWidgets.QTableWidgetItem()
        item_e = QtWidgets.QTableWidgetItem()
        self.search_result_box.setItem(max_row, 0, item_row)
        self.search_result_box.setItem(max_row, 1, item_k)
        self.search_result_box.setItem(max_row, 2, item_e)
        # Tabel 열 너비
        self.search_result_box.setColumnWidth(0, 50)
        self.search_result_box.setColumnWidth(1, (self.search_result_box.geometry().width() - 50) / 2 - 10)
        self.search_result_box.setColumnWidth(2, (self.search_result_box.geometry().width() - 50) / 2 - 10)

    def save_all_file(self):
        # 빈 변수 지우기
        self.db.replace('', np.nan, inplace=True)       # '' 빈변수를 nan 값으로 처리
        self.db.dropna(inplace=True)                    # nan 값 날리기
        self.db.reset_index(drop=True, inplace=True)    # 숫자 인텍스 초기화
        # db 저장하기
        self.db.to_pickle('db.pkl')

    def keyPressEvent(self, e):
        # print(e.key())
        if e.key() == 16777220: # 엔터 키로 내용 서치
            self.update_table_from_search_input()
        elif e.key() == 16777266: # F3 키으로 변경된 내용 저장
            # db 저장하기
            self.save_all_file()
        elif e.key() == 16777267: # F4 키로 새로운 열 생성
            # 열생성
            self.make_db()
        elif e.key() == 16777268: # F5 키로 모든 db 보기
            self.show_all_Db()

    def resizeEvent(self, e):
        self.search_input_box.setGeometry(QtCore.QRect(5, 5, self.geometry().width()-10, 30))
        self.search_result_box.setGeometry(QtCore.QRect(5, 40, self.geometry().width()-10, self.geometry().height()-50))
        # Tabel 열 너비
        self.search_result_box.setColumnWidth(0, 50)
        self.search_result_box.setColumnWidth(1, (self.search_result_box.geometry().width()-50)/2-10)
        self.search_result_box.setColumnWidth(2, (self.search_result_box.geometry().width()-50)/2-10)
        # 자동 줄 바꿈
        self.search_result_box.resizeRowsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # window = Form()
    window.show()
    sys.exit(app.exec_())

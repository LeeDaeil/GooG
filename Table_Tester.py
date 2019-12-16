from PySide2.QtWidgets import QMainWindow, QApplication, QTableWidget, QAction, QTableWidgetItem
from PySide2.QtCore import SLOT, QSize
from PySide2 import QtCore
import sys


class MyGui(QMainWindow):
    def __init__(self):
        super(MyGui, self).__init__()
        self.initMenu()
        self.showTable()
        self.setGeometry(50, 50, 700, 400)
        self.show()

    def showTable(self):
        self.table = QTableWidget(3, 3)
        # 자동 줄바꿈
        self.table.setWordWrap(True)

        self.table.setColumnCount(3)
        self.table.setColumnWidth(0, 20)                   # 각 컬럼의 크기를 정함
        self.table.setColumnWidth(1, 50)                   # 각 컬럼의 크기를 정함
        self.table.setHorizontalHeaderLabels(["Make", "Model", "Price"])
        # 숫자
        self.table.setItem(0, 0, QTableWidgetItem('1'))
        self.table.setItem(1, 0, QTableWidgetItem('3'))
        self.table.setItem(2, 0, QTableWidgetItem('2'))
        # 아이템 추가 하기
        item_test = QTableWidgetItem('Test')
        self.table.setItem(0, 1, item_test)
        # 체크가 가능한 아이템 추가
        item_test_2 = QTableWidgetItem('Test')
        item_test_2.setCheckState(QtCore.Qt.Unchecked)
        self.table.setItem(1, 1, item_test_2)
        #
        # 2줄로 입력
        item_test_3 = QTableWidgetItem('This is my\nlong text.')
        self.table.setItem(2, 1, item_test_3)
        print(self.table.sizeHintForRow(0))
        # print(self.table.item(2, 1).setSizeHint(QSize(37, 50)))
        # self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        print(self.table.rowViewportPosition(0)) # 이걸 통해서 높이에 대한 힌트 파악
        print(self.table.rowViewportPosition(1)) # 이걸 통해서 높이에 대한 힌트 파악
        print(self.table.rowViewportPosition(2)) # 이걸 통해서 높이에 대한 힌트 파악
        #
        # 오름차순/내림차순 만들기
        self.table.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)  # 낮은 번호가 위로 가는 기능 - 오름차순
        # self.table.sortItems(0, QtCore.Qt.SortOrder.DescendingOrder)  # 높은 번호가 위로 가는 기능 - 내림차순
        #
        # cell을 더블 클릭 및 클릭하였을때 함수 호출
        self.table.cellDoubleClicked.connect(self.call_test_print)
        self.table.cellClicked.connect(self.call_test_print)
        #
        self.setCentralWidget(self.table)
        #

    def call_test_print(self):
        print(self.table.item(0, 0))
        print(self.table.viewportSizeHint())
        get_cell_1 = self.table.item(0, 0)

    def initMenu(self):
        # 메뉴를 추가하는 Function
        menubar = self.menuBar()

        fileMenu = menubar.addMenu("File")
        open = QAction("Open", self)
        open.triggered.connect(self.openFile)
        fileMenu.addAction(open)

        quit = QAction("Quit", self)
        quit.triggered.connect(self.close)
        fileMenu.addAction(quit)

    def openFile(self):
        print('Test open file')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mygui = MyGui()
    sys.exit(app.exec_())
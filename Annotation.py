import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QPushButton, QTableWidget, \
                            QTableWidgetItem, QVBoxLayout, QHBoxLayout
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt


#Main Window
class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        self.title = 'Video Annotator'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # self.frame = QFrame()
        # self.frame.setGeometry(QtCore.QRect(5, 5, 290, 190))
        # self.frame.setFrameShape(QFrame.StyledPanel)
        # self.frame.setFrameShadow(QFrame.Sunken)

        # self.createTable() 

        layout = QHBoxLayout()
        tableWidget = Table()
        layout.addWidget(tableWidget)
        buttonLayout = QHBoxLayout()

        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        # Push button to add row
        addRowBtn = QPushButton('Add')
        addRowBtn.clicked.connect(tableWidget.addRowBtn_clicked)
        layout.addWidget(addRowBtn)

        remRowBtn = QPushButton('Remove')
        # self.remButton.setGeometry(QtCore.QRect(30, 20, 201, 31))
        remRowBtn.clicked.connect(tableWidget.remRowBtn_clicked)
        layout.addWidget(remRowBtn)
        # self.pushButton_3.setObjectName("pushButton_3")


        #Show window
        self.show()

class Table(QTableWidget):
    def __init__(self):
        super().__init__(1, 2)

        self.setHorizontalHeaderLabels(("Time", "Annotation"))


        #Create table
        # def createTable(self):
        #     self.tableWidget = QTableWidget()
        #     self.model = QtGui.QStandardItemModel(self.tableWidget)
        #     self.tableWidget.setGeometry(QtCore.QRect())
        #     self.tableWidget.setShowGrid(True)
        #     self.tableWidget.setModel(self.model)
        #Column and Row Count
        # self.tableWidget.setColumnCount(2)
        # self.tableWidget.setRowCount(0)
        # self.tableWidget.setHorizontalHeaderLabels(("Object", "Value"))
        self.setColumnWidth(0, 20)
        self.setColumnWidth(1, 80)

        #Table will fit the screen horizontally
        self.horizontalHeader().setStretchLastSection(True)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

     # def addRow(self, tableWidget, model):
        #     indices = tableWidget.selectionModel().selectedRows()
        # # in case none selected or no table to select
        #     if len(indices) == 0 :
        #         model.insertRow(0)
        #     else:
        #         for index in sorted(indices):
        #             model.insertRow(index)

    # @QtCore.pyqtSlot()
    def addRowBtn_clicked(self):
        rowCount = self.rowCount()
        self.insertRow(rowCount )

    def remRowBtn_clicked(self):
        if self.rowCount() > 0:
            self.removeRow(self.rowCount()-1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.resize(640, 480)
    sys.exit(app.exec_())

    # player = App()
    # player.resize(640, 480)
    # player.show()
    # sys.exit(app.exec_())





    #Resources
    # https://www.geeksforgeeks.org/pyqt5-qtablewidget/
    # https://forum.qt.io/topic/89827/pyqt5-button-to-add-row-to-a-qtableview
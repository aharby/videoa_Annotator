from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem


class Table(QTableWidget):
    def __init__(self, lablesList):
        super().__init__(1,3)
        self.setHorizontalHeaderLabels(lablesList)
        self.verticalHeader().setDefaultSectionSize(50)
        self.horizontalHeader().setDefaultSectionSize(100)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        #self.setStyleSheet("background-color: #4F4D4C;")
        
    def addRow(self):
        rowCount = self.rowCount()
        self.insertRow(rowCount)

    def _removeRow(self):
        if self.rowCount() > 0:
            self.removeRow(self.rowCount() - 1)


    def addItem(self, entry):
        rowCount = self.rowCount()
        self.setItem(rowCount - 1, 0, QTableWidgetItem(entry))
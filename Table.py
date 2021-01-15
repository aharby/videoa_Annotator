from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, QVBoxLayout, QPushButton, QHBoxLayout


class Table(QTableWidget):
    def __init__(self, mainWindow, lablesList):
        super().__init__(0, len(lablesList))
        self.mainWindow = mainWindow
        self.setHorizontalHeaderLabels(lablesList)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableLayout = QVBoxLayout()

        self.addButton = QPushButton("Save")
        self.addButton.clicked.connect(self.save)
        self.remButton = QPushButton("Delete")
        self.remButton.clicked.connect(self.save)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addWidget(self.addButton, 10)
        self.buttonsLayout.addWidget(self.remButton, 10)

    def addRow(self):
        rowCount = self.rowCount()
        self.insertRow(rowCount)

    def _removeRow(self):
        if self.rowCount() > 0:
            self.removeRow(self.rowCount() - 1)

    def addItem(self, entry):
        rowCount = self.rowCount()
        self.setItem(rowCount, 0, QTableWidgetItem(entry))

    def addStamp(self, start, end):
        rowCount = self.rowCount()
        print(start)
        print(end)
        self.addRow()
        start = "{:10.4f}".format(start)
        end = "{:10.4f}".format(end)
        self.setItem(rowCount, 1, QTableWidgetItem(start))
        self.setItem(rowCount, 2, QTableWidgetItem(end))

    def addRowItem(self, attribute, start, end, entry):
        rowCount = self.rowCount()
        self.addRow()
        self.setItem(rowCount, 0, QTableWidgetItem(attribute))
        self.setItem(rowCount, 1, QTableWidgetItem(start))
        self.setItem(rowCount, 2, QTableWidgetItem(end))
        self.setItem(rowCount, 3, QTableWidgetItem(entry))

    def save(self):
        for x in range(0, self.rowCount() - 1):
            attribute = self.item(x, 0).text()
            start = self.item(x, 1).text()
            end = self.item(x, 2).text()
            entry = self.item(x, 3).text()
            self.mainWindow.annotationSet.annotate(attribute, start, end, entry)



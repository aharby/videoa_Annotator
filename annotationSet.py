import numpy as np
from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtWidgets import QFileDialog, QStyle
import pandas as pd



class annotationSet:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        self.fileName = ''
        self.start = 0
        self.end = 0

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self.mainWindow, "Open Annotation",
                                                  QDir.homePath())
        if fileName != '':
            self.fileName = fileName
            self.setDataFrame()

    def setDataFrame(self):
        if self.fileName.__contains__('.csv'):
            self.dataFrame = pd.read_csv(self.fileName, sep=';')
        if self.fileName.__contains__('.xlsx'):
            self.dataFrame = pd.read_excel(self.fileName, engine="openpyxl")

        self.dataFrame.set_index(['Parent', 'Start'], inplace=True)
        self.dataFrame.sort_index(level='Start', inplace=True)
        self.dataFrame.drop_duplicates(inplace=True)
        self.loadAnnotation()

    def annotate(self, parent, start, end, entry):
        df2 = pd.DataFrame(np.array([[parent, start, end, entry]]),
                           columns=['Parent', 'Start', 'End', 'Entry'])
        df2.set_index(['Parent', 'Start'], inplace=True)
        self.dataFrame = self.dataFrame.append(df2)
        self.dataFrame.sort_index(level='Start', inplace=True)
        self.dataFrame.to_csv(self.fileName, sep=';')



    def loadAnnotation(self):
        self.dataFrame.reset_index(inplace=True)
        print(self.dataFrame)
        for x in range(0, len(self.dataFrame.index) - 1):
            attribute = self.dataFrame.iat[x, 0]
            start = self.dataFrame.iat[x, 1]
            end = self.dataFrame.iat[x, 2]
            #entry = self.dataFrame.iat[x, 3]
            start = "{:10.4f}".format(start)
            end = "{:10.4f}".format(end)
            print(attribute)
            self.mainWindow.annotationTable.addRowItem(attribute, start, end, end)
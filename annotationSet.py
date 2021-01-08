import numpy as np
from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtWidgets import QFileDialog, QStyle
import pandas as pd



class annotationSet:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        self.fileName = ''

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self.mainWindow, "Open Excel",
                                                  QDir.homePath())
        if fileName != '':
            self.fileName = fileName
            self.setDataFrame()


    def setDataFrame(self):
       self.dataFrame = pd.read_excel(self.fileName, engine="openpyxl")
       self.dataFrame = self.dataFrame.set_index('Time')



    def annotate(self, position, commentType ,value):
        columnCheck = commentType in self.dataFrame
        if not (columnCheck):
            self.dataFrame[commentType] = np.nan

        self.dataFrame.loc[position, commentType] = value
        self.dataFrame.sort_index(inplace=True)
        self.dataFrame.to_excel(self.fileName)
        #self.setDataFrame()







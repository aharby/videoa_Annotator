from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtWidgets import  QFileDialog,QStyle
import pandas as pd


class Dataset:
    def __init__(self, mainWindow):
        
        self.mainWindow= mainWindow
        
        self.fileName = ''
        
        
        

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self.mainWindow, "Open Excel",
                QDir.homePath())

        if fileName != '':
            self.fileName= fileName
            self.dataFrame = pd.read_csv(fileName, skiprows=6, sep=';')
            self.mainWindow.showFrameParameters.parametersList = list(self.mainWindow.dataset.dataFrame.columns)
            self.mainWindow.showFrameParameters.timeList = list(self.mainWindow.dataset.dataFrame['Time'])
            
    def showTimeElapesed(self,position):
        elapsedtime= position/1000
        self.mainWindow.label1.setText('elapsed time: '+str(elapsedtime))
        
    def showParameter(self,position):
        valuelist = list(self.dataFrame['Time'])
        elapsedtime= position/1000
        newvalue = min(valuelist, key=lambda x:abs(x-elapsedtime))
        V_ACCEL_X= self.dataFrame[self.dataFrame['Time']==newvalue]['V_SPEED'].values[0]        
        self.mainWindow.label2.setText('Speed: '+str(V_ACCEL_X))
        
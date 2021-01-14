from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import (  QTableWidget, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget,QInputDialog,QLineEdit)
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox

import pyqtgraph as pg

class ShowFrameParameters:
    
    def __init__(self,mainWindow):
        
        self.mainWindow = mainWindow

        self.parametersLayout= QVBoxLayout()
        
        self.table =QTableWidget()
        
        
        self.parametersList = []
        self.timeList = []
                
        self.position= 0
        
        self.parametersToShow= {}
        
        self.initTable()


        
        self.addButton = QPushButton("ADD")
        self.remButton = QPushButton("REMOVE")
        self.addButton.clicked.connect(self.addParameter)
        self.remButton.clicked.connect(self.remParameter)
        
        self.buttonsLayout= QHBoxLayout()
        self.buttonsLayout.addWidget(self.addButton)
        self.buttonsLayout.addWidget(self.remButton)
        
        self.parametersLayout.addWidget(self.table)
        self.parametersLayout.addLayout(self.buttonsLayout)
    
    def setPosition(self,position):
        self.position = position
        
        
    def addParameter(self):
        graphWidgetIndex= 2
        table=self.table
        text, okPressed = QInputDialog.getText(self.mainWindow, "Add Parameter","Parameter:", QLineEdit.Normal, "")
        if okPressed :
            parameterName =text
            
            if parameterName in self.parametersList :
                if parameterName not in self.parametersToShow.keys() :
                    parameter = Parameter(parameterName, self.mainWindow, graphWidgetIndex)
                    self.parametersToShow.update({parameterName:parameter})
                    rowCount = table.rowCount()
                    table.insertRow(rowCount)
                    table.setCellWidget(rowCount,0,parameter.labelName)
                    table.setCellWidget(rowCount,1,parameter.labelValue)
                    table.setCellWidget(rowCount,2,parameter.graphButton)
                    graphWidgetIndex+=1
                else:
                    QMessageBox.about(self.mainWindow, 'Add Parameter', parameterName+' already shown!')
            else:
                QMessageBox.about(self.mainWindow, 'Add Parameter', parameterName+' doesnt exist!')

        
        
    def remParameter(self):
        
        text, okPressed = QInputDialog.getText(self.mainWindow, "Remove Parameter","Parameter:", QLineEdit.Normal, "")
        if okPressed :
            parameterName =text
            
            
        if parameterName in self.parametersToShow :
            del self.parametersToShow[parameterName]
            QMessageBox.about(self.mainWindow, 'Remove Parameter', 'parameter removed!')
        else:
            QMessageBox.about(self.mainWindow, 'Remove Parameter', 'Nan!')

       
    
            
    def update(self,position):
        
        df= self.mainWindow.dataset.dataFrame
        elapsedtime= position/1000
        timePosition = min(self.timeList, key=lambda x:abs(x-elapsedtime))

        
        for parameter in self.parametersToShow.keys():
            parameterValue = df[df['Time']==timePosition][parameter].values[0]
            self.parametersToShow[parameter].labelValue.setText(str(parameterValue))

    def initTable(self):
        table= self.table
        table.setRowCount(0)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Attibute','Value','Graph'])
        
        #initialize time to show
        parameterName ='Time'
        graphWidgetIndex= 1
        parameter = Parameter(parameterName, self.mainWindow, graphWidgetIndex)
        self.parametersToShow.update({parameterName:parameter})
        rowCount = table.rowCount()
        table.insertRow(rowCount)
        table.setCellWidget(rowCount,0,parameter.labelName)
        table.setCellWidget(rowCount,1,parameter.labelValue)


class Parameter:
    
    def __init__(self, parameterName, mainWindow,graphWidgetIndex):
        self.mainWindow= mainWindow
        self.parameter= parameterName
        self.graphWidgetIndex= graphWidgetIndex
        self.graphButton = QPushButton("GRAPH")
        self.graphButton.clicked.connect(self.showGraph)
        self.labelName= QLabel(self.parameter)
        self.labelValue= QLabel()
        self.graphWidget= pg.PlotWidget()        
        self.mainWindow.graphLayout.addWidget(self.graphWidget)

    def showGraph(self):
        df= self.mainWindow.dataset.dataFrame
        self.graphWidget.plot(df['Time'],df[self.parameter])
        self.mainWindow.graphLayout.setCurrentIndex(self.graphWidgetIndex)
        

        
        
        
        



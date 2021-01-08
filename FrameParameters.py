from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import (  QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget,QInputDialog,QLineEdit)
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox
class ShowFrameParameters:
    
    def __init__(self,mainWindow):
        
        self.parametersLayout= QVBoxLayout()
        self.mainWindow = mainWindow
        
        self.parametersList = []
        self.timeList = []
                
        self.position= 0
        
        self.parametersToShow= {}
        
        self.addButton = QPushButton("ADD")
        self.remButton = QPushButton("REMOVE")
        self.addButton.clicked.connect(self.addParameter)
        self.remButton.clicked.connect(self.remParameter)
        
        self.buttonsLayout= QHBoxLayout()
        self.buttonsLayout.addWidget(self.addButton)
        self.buttonsLayout.addWidget(self.remButton)
        
        self.parametersLayout.addLayout(self.buttonsLayout)
    
    def setPosition(self,position):
        self.position = position
        
        
    def addParameter(self):
        
        text, okPressed = QInputDialog.getText(self.mainWindow, "Add Parameter","Parameter:", QLineEdit.Normal, "")
        if okPressed :
            parameterName =text
            
        if parameterName in self.parametersList :
            if parameterName not in self.parametersToShow.keys() :
                parameter = Parameter(parameterName)
                self.parametersToShow.update({parameterName:parameter})
                self.parametersLayout.addWidget(parameter.label)
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
            self.parametersToShow[parameter].label.setText(parameter+': '+str(parameterValue))
            #label= QLabel(parameter+': '+str(parameterValue))
            #self.parametersLayout.addWidget(label)


class Parameter:
    
    def __init__(self, parameterName):
        self.parameter= parameterName
        #self.graphButton = QPushButton()
        #self.graphButton.clicked.connect(self.showGraph)
        self.label= QLabel(parameterName)
        
    
        

    #def showGraph(self):
        
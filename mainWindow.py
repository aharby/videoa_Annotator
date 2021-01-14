# PyQt5 Video player
#!/usr/bin/env python

#https://pythonprogramminglanguage.com/pyqt5-video-widget/

from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import (  QHBoxLayout,QGridLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget,QStackedWidget)
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox
from PyQt5.QtGui import QIcon
import sys

import pyqtgraph as pg


from Video import Video
from Dataset import Dataset
from Sync import Sync
from FrameParameters import ShowFrameParameters
from Table import Table
from annotationSet import annotationSet
class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Video Annotator") 
        #self.setStyleSheet("background-color: #4F4D4C;") 

        self.faceVideo = Video(self)
        self.video360 = Video(self)
        self.beepRef = Video(self)
        self.annotationTable = Table(["Time", "Attribute", "Entry"])
        self.showParametersTable= Table(["parameter","value"])
        self.dataset= Dataset(self)
        self.annotationset = annotationSet(self)
        
        
        #graph layout
        self.graphLayout= QStackedWidget()
        self.graphWidgetIndex= 0
        self.graphWidget = pg.PlotWidget()
        self.graphLayout.addWidget(self.graphWidget)
        self.graphLayout.setCurrentIndex(0)
        self.graphWidgetIndex+= 1
        
        self.showFrameParameters = ShowFrameParameters(self)
        

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        
        self.syncButton= QPushButton('Sync')
        self.syncButton.clicked.connect(self.syncronize)
        
        #annotation start and stop buttons
        self.startAnnotationButton = QPushButton('start')
        self.stopAnnotationButton = QPushButton('stop')
        
        #slider
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create new action
        openVideo1 = QAction(QIcon('open.png'), '&Upload Face Video', self)        
        openVideo2 = QAction(QIcon('open.png'), '&Upload 360 Video', self)        
        openRefVideo = QAction(QIcon('open.png'), '&Upload Reference Beep', self)  
        openDataset = QAction(QIcon('open.png'),'&Upload Dataset',self)
        openAnnotationSet = QAction(QIcon('open.png'), '&Upload Annotation Set', self)

        openVideo1.triggered.connect(self.faceVideo.openFile)
        openVideo2.triggered.connect(self.video360.openFile)
        openRefVideo.triggered.connect(self.beepRef.openFile)
        openDataset.triggered.connect(self.dataset.openFile)
        openAnnotationSet.triggered.connect(self.annotationset.openFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openVideo1)
        fileMenu.addAction(openVideo2)
        fileMenu.addAction(openRefVideo)
        fileMenu.addAction(openDataset)
        fileMenu.addAction(openAnnotationSet)
        
        #show menu
        showMenu= menuBar.addMenu('&Show')
        


        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        buttonsLayout=  QHBoxLayout()
        buttonsLayout.setContentsMargins(0, 0, 0, 0)
        buttonsLayout.addWidget(self.playButton)
        buttonsLayout.addWidget(self.syncButton)
        #controlLayout.addWidget(self.positionSlider)
        buttonsLayout.addWidget(self.startAnnotationButton)
        buttonsLayout.addWidget(self.stopAnnotationButton)
        
        controlLayout = QVBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addLayout(buttonsLayout)
        controlLayout.addWidget(self.positionSlider)

        
        #video layout
        videoLayout = QHBoxLayout()
        videoLayout.setContentsMargins(0, 0, 0, 0)
        videoLayout.addWidget(self.faceVideo.videoWidget)
        videoLayout.addWidget(self.video360.videoWidget)
        

        layout= QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)        
        layout.addLayout(videoLayout)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)
        
        
        bottomLayout= QHBoxLayout()
        bottomLayout.addWidget(self.annotationTable,70)

        bottomLayout.addWidget(self.graphLayout,30)
        
        upperLayout= QHBoxLayout()
        upperLayout.addLayout(self.showFrameParameters.parametersLayout,30)
        upperLayout.addLayout(layout,70)
        
        layoutMain= QVBoxLayout()
        layoutMain.addLayout(upperLayout,70)
        layoutMain.addLayout(bottomLayout,30)
        

        # Set widget to contain window contents
        wid.setLayout(layoutMain)

    def syncronize(self):
        vRef= self.beepRef.fileName
        v1= self.faceVideo.fileName
        if not ((vRef=='')|(v1=='')):
            sync= Sync(vRef,v1)
            syncedFaceVid= sync.get_synced_video()
            if syncedFaceVid != '':
                self.faceVideo.setMediaPlayer(syncedFaceVid)
                self.video360.setMediaPlayer(self.video360.fileName)
                QMessageBox.about(self, 'video Annotator', 'Sync process is done!')
            else:
                QMessageBox.about(self, 'video Annotator', 'Sync process failed. Please try again.')
        else:
            QMessageBox.about(self, 'video Annotator', 'Please upload the videos first!')
            
    
    def play(self):
        self.faceVideo.play()
        self.video360.play()
        
    def setPosition(self, position):
        self.faceVideo.setPosition(position)
        self.video360.setPosition(position)
        
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        self.showFrameParameters.setPosition(position)
        self.showFrameParameters.update(position)

        
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
    

    def exitCall(self):
        sys.exit(app.exec_())
        

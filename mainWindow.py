# PyQt5 Video player
#!/usr/bin/env python

#https://pythonprogramminglanguage.com/pyqt5-video-widget/

from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import (  QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox
from PyQt5.QtGui import QIcon
import sys

import annotationTable
from Video import Video
from Dataset import Dataset
from Sync import Sync
from annotationSet import annotationSet


class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Video Annotator") 


        self.faceVideo = Video(self)
        self.video360 = Video(self)
        self.beepRef = Video(self)

        self.dataset= Dataset(self)

        self.position = 0

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.syncButton= QPushButton('Sync')
        self.syncButton.clicked.connect(self.syncronize)

        self.annotateButton = QPushButton('Annotate')
        self.annotateButton.clicked.connect(self.annotate)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        self.annotationset = annotationSet(self)

        # Create new action
        openVideo1 = QAction(QIcon('open.png'), '&Add Face Video', self)        
        openVideo2 = QAction(QIcon('open.png'), '&Add 360 Video', self)        
        openRefVideo = QAction(QIcon('open.png'), '&Add Reference Beep', self)  
        openDataset = QAction(QIcon('open.png'),'&Add Dataset',self)
        openAnnotation = QAction(QIcon('open.png'), '&Add Annotation', self)

        openVideo1.triggered.connect(self.faceVideo.openFile)
        openVideo2.triggered.connect(self.video360.openFile)
        openRefVideo.triggered.connect(self.beepRef.openFile)
        openDataset.triggered.connect(self.dataset.openFile)
        openAnnotation.triggered.connect(self.annotationset.openFile)

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
        fileMenu.addAction(openAnnotation)
        
        
        #show menu
        showMenu= menuBar.addMenu('&Show')
        


        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        layoutRight = QVBoxLayout()
        self.tableWidget = annotationTable.AnnotationTable()
        layoutRight.addWidget(self.tableWidget)
        buttonLayout = QHBoxLayout()

        layoutRight.addLayout(buttonLayout)
        self.setLayout(layoutRight)

        # Push button to add row
        addRowBtn = QPushButton('Add')
        addRowBtn.clicked.connect(self.addAnnotation)
        layoutRight.addWidget(addRowBtn)

        remRowBtn = QPushButton('Remove')
        # self.remButton.setGeometry(QtCore.QRect(30, 20, 201, 31))
        #remRowBtn.clicked.connect(self.tableWidget.remRowBtn_clicked)
        layoutRight.addWidget(remRowBtn)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.syncButton)
        controlLayout.addWidget(self.annotateButton)
        controlLayout.addWidget(self.positionSlider)

        

        #parameters Layout
        self.label1 = QLabel('elapsed time:')
        self.label2 = QLabel('speed:')
        parameterLayout= QHBoxLayout()
        parameterLayout.setContentsMargins(0, 0, 0, 0)
        parameterLayout.addWidget(self.label1)
        parameterLayout.addWidget(self.label2)
        
        #video layout
        videoLayout = QVBoxLayout()
        videoLayout.addWidget(self.faceVideo.videoWidget)
        videoLayout.addWidget(self.video360.videoWidget)
        
        
        layout= QVBoxLayout()
        layout.addLayout(videoLayout)
        layout.addLayout(controlLayout)
        layout.addLayout(parameterLayout)
        layout.addWidget(self.errorLabel)

        layoutAll = QHBoxLayout()
        layoutAll.addLayout(layout)
        layoutAll.addLayout(layoutRight)


        # Set widget to contain window contents
        wid.setLayout(layoutAll)

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
            QMessageBox.about(self, 'video Annotator', 'Please add the videos first!')
            
    def setLocalPosition(self, position):
        self.position = position

    def play(self):
        self.faceVideo.play()
        self.video360.play()
        
    def setPosition(self, position):
        self.faceVideo.setPosition(position)
        self.video360.setPosition(position)
        
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        self.dataset.showTimeElapesed(position)
        self.setLocalPosition(position)

        if self.dataset.fileName !='' :
            self.dataset.showParameter(position)
        
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        
    def addAnnotation(self):
        self.annotationset.annotate(self.position/1000, self.tableWidget.item(self.tableWidget.rowCount()-1,1).text(), self.tableWidget.item(self.tableWidget.rowCount()-1,2).text())
        self.tableWidget.addRow()

    def annotate(self):
        self.play()
        float_as_str = "{:10.4f}".format(self.position/1000)
        self.tableWidget.addItem(float_as_str)

    def exitCall(self):
        sys.exit(app.exec_())
        

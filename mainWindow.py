# PyQt5 Video player
#!/usr/bin/env python

#https://pythonprogramminglanguage.com/pyqt5-video-widget/

from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import (  QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox
from PyQt5.QtGui import QIcon
import sys

from Video import Video
from Sync import Sync

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Video Annotator") 


        self.faceVideo = Video(self)
        self.video360 = Video(self)
        self.beepRef = Video(self)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.syncButton= QPushButton('Sync')
        self.syncButton.clicked.connect(self.syncronize)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create new action
        openAction1 = QAction(QIcon('open.png'), '&Upload Face Video', self)        
        openAction2 = QAction(QIcon('open.png'), '&Upload 360 Video', self)        
        openAction3 = QAction(QIcon('open.png'), '&Upload Reference Beep', self)        

        openAction1.triggered.connect(self.faceVideo.openFile)
        openAction2.triggered.connect(self.video360.openFile)
        openAction3.triggered.connect(self.beepRef.openFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction1)
        fileMenu.addAction(openAction2)
        fileMenu.addAction(openAction3)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.syncButton)
        controlLayout.addWidget(self.positionSlider)

        videoLayout = QHBoxLayout()
        videoLayout.addWidget(self.faceVideo.videoWidget)
        videoLayout.addWidget(self.video360.videoWidget)
        
        layout= QVBoxLayout()
        layout.addLayout(videoLayout)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

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

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
    

    def exitCall(self):
        sys.exit(app.exec_())
        

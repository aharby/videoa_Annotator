# PyQt5 Video player
#!/usr/bin/env python

#https://pythonprogramminglanguage.com/pyqt5-video-widget/

# from PyQt5.QtCore import  Qt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (  QHBoxLayout, QLabel, QTableWidget,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QHBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox, QFrame
from PyQt5.QtGui import QIcon
import sys
from PyQt5 import QtCore

from Video import Video
from Dataset import Dataset
from Sync import Sync

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Video Annotator") 

        self.faceVideo = Video(self)
        self.video360 = Video(self)
        self.beepRef = Video(self)
        self.dataset= Dataset(self)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        ##########
        # Frame1 #
        ##########
        self.frame = QFrame(wid)
        self.frame.setGeometry(QtCore.QRect(10, 10, 701, 841))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Sunken)

        # wid.addWidget(self.faceVideo.videoWidget)
        # wid.addWidget(self.video360.video)
        # self.faceVideo.videoWidget.setGeometry(QtCore.QRect(20, 370, 661, 351))
        # self.video360.videoWidget(self.frame)
        # self.video360.videoWidget.setGeometry(QtCore.QRect(20, 10, 661, 351))
        videolayout = QVBoxLayout(self.frame)
        videolayout.addWidget(self.faceVideo.videoWidget)
        self.faceVideo.videoWidget.setGeometry(QtCore.QRect(20, 10, 661, 351))
        videolayout.addWidget(self.video360.videoWidget)
        self.video360.videoWidget.setGeometry(QtCore.QRect(20, 370, 661, 351))

        self.playButton = QPushButton(self.frame)
        self.playButton.setGeometry(QtCore.QRect(30, 730, 31, 31))
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.syncButton= QPushButton('Sync Video', self.frame)
        self.syncButton.setGeometry(QtCore.QRect(520, 800, 171, 31))
        self.syncButton.clicked.connect(self.syncronize)

        self.positionSlider = QSlider(Qt.Horizontal, self.frame)
        self.positionSlider.setGeometry(QtCore.QRect(70, 730, 541, 31))
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.label1 = QLabel('00:00', self.frame)
        self.label1.setAlignment((Qt.AlignCenter | Qt.AlignVCenter))
        self.label1.setGeometry(QtCore.QRect(620, 730, 61, 31))

        # parameterLayout= QHBoxLayout()
        # parameterLayout.addWidget(self.positionSlider)
        # parameterLayout.addWidget(self.label1)
        # self.positionSlider.setGeometry(QtCore.QRect(70, 730, 580, 31)

        # self.label1 = QLabel('Elapsed time', self.frame)
        # self.label1.setGeometry(QtCore.QRect(620, 730, 61, 31))
        self.label2 = QLabel('Speed:', self.frame)
        self.label2.setGeometry(QtCore.QRect(30, 770, 141, 20))

        self.errorLabel = QLabel(self.frame)
        self.errorLabel.setGeometry(QtCore.QRect(30, 790, 141, 20))
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # layout= QVBoxLayout(self.frame)
        # layout.addLayout(videolayout)
        # layout.addLayout(parameterLayout)

        ###########
        # Frame 2 #
        ###########

        # For Data Annotation

        self.frame2 = QFrame(wid)
        self.frame2.setGeometry(QtCore.QRect(730, 10, 461, 461))
        self.frame2.setFrameShape(QFrame.StyledPanel)
        self.frame2.setFrameShadow(QFrame.Sunken)

        ###########
        # Frame 3 #
        ###########

        #Might be for Visualization

        self.frame_3 = QFrame(wid)
        self.frame_3.setGeometry(QtCore.QRect(729, 489, 461, 361))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Sunken)


        # Menu #
        ########

        # Create new action
        openVideo1 = QAction(QIcon('open.png'), '&Add Face Video', self)        
        openVideo2 = QAction(QIcon('open.png'), '&Add 360 Video', self)        
        openRefVideo = QAction(QIcon('open.png'), '&Add Reference Beep', self)  
        openDataset = QAction(QIcon('open.png'),'&Add Dataset',self)

        openVideo1.triggered.connect(self.faceVideo.openFile)
        openVideo2.triggered.connect(self.video360.openFile)
        openRefVideo.triggered.connect(self.beepRef.openFile)
        openDataset.triggered.connect(self.dataset.openFile)

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
        
        #show menu
        showMenu= menuBar.addMenu('&Show')
        

    def syncronize(self):
        vRef= self.beepRef.fileName
        v1= self.faceVideo.fileName
        if not ((vRef=='')|(v1=='')):
            sync= Sync(vRef,v1)
            syncedFaceVid= sync.get_synced_video()
            if syncedFaceVid != '':
                self.faceVideo.setMediaPlayer(syncedFaceVid)
                self.video360.setMediaPlayer(self.video360.fileName)
                QMessageBox.about(self, 'video Annotator', 'Sync done!')
            else:
                QMessageBox.about(self, 'video Annotator', 'Sync failed. Pleas try again')
        else:
            QMessageBox.about(self, 'video Annotator', 'Please upload videos first')
            
    
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
        

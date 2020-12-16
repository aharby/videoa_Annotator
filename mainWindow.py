# PyQt5 Video player
#!/usr/bin/env python

#https://pythonprogramminglanguage.com/pyqt5-video-widget/

from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import (  QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtGui import QIcon
import sys

from Video import Video

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Video Annotator") 


        self.video1 = Video(self)
        self.video2 = Video(self)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create new action
        openAction1 = QAction(QIcon('open.png'), '&Open1', self)        
        openAction2 = QAction(QIcon('open.png'), '&Open2', self)        

        openAction1.triggered.connect(self.video1.openFile)
        openAction2.triggered.connect(self.video2.openFile)

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
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(self.video1.videoWidget)
        layout.addWidget(self.video2.videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

    def play(self):
        self.video1.play()
        self.video2.play()
        
    def setPosition(self, position):
        self.video1.setPosition(position)
        self.video2.setPosition(position)
        
    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
    

    def exitCall(self):
        sys.exit(app.exec_())
        

from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import  QFileDialog,QStyle
        
#rom PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction



class Video:
    
    def __init__(self, mainWindow):
        
        self.mainWindow= mainWindow
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.videoWidget = QVideoWidget()
        
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.mainWindow.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.mainWindow.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        
        
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self.mainWindow, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.mainWindow.playButton.setEnabled(True)



    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mainWindow.playButton.setIcon(
                    self.mainWindow.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.mainWindow.playButton.setIcon(
                    self.mainWindow.style().standardIcon(QStyle.SP_MediaPlay))

 
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.mainWindow.playButton.setEnabled(False)
        self.mainWindow.errorLabel.setText("Error: " + self.mediaPlayer.errorString())


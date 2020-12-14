from PyQt5.QtWidgets import QApplication
import sys




from mainWindow import VideoWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())
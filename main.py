from PyQt5.QtWidgets import QApplication
import sys
import qdarkstyle




from mainWindow import VideoWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(1080, 600)
    
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    player.show()
    sys.exit(app.exec_())
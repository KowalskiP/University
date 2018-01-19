import sys
import re
import os
from PyQt4 import QtCore, QtGui, QtWebKit

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Flight Radar')
        self.setGeometry(100, 100, 640, 480)
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)

class MainWidget(QtGui.QWidget):
    def __init__(self,parent):
        super(MainWidget, self).__init__(parent)

        frame = QtGui.QFrame(self)
        gridlay = QtGui.QGridLayout(frame)

        web = QtWebKit.QWebView()
        gridlay.addWidget(web,0,0)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    aw = MainWindow(None)
    aw.show()
    sys.exit(app.exec_())
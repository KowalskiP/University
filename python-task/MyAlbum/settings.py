__author__ = 'kowalski'
import sys
import configparser

from PyQt4 import QtGui, QtCore

class MySettings(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MySettings, self).__init__(parent)
        self.setWindowTitle('Settings')
        self.setGeometry(100, 100, 666, 600)

        boxlay = QtGui.QVBoxLayout(self)

        frame1 = QtGui.QFrame(self)
        frame1.setFrameShape(QtGui.QFrame.StyledPanel)
        frame1.setFrameShadow(QtGui.QFrame.Raised)

        pathRoot = QtCore.QDir.rootPath()

        self.model = QtGui.QFileSystemModel(self)
        self.model.setRootPath(pathRoot)

        indexRoot = self.model.index(self.model.rootPath())

        treeView = QtGui.QTreeView(self)
        treeView.setModel(self.model)
        treeView.setRootIndex(indexRoot)
        treeView.clicked.connect(self.on_treeView_clicked)


        labelFilePath = QtGui.QLabel(self)
        labelFilePath.setText("File Path:")

        self.lineEditFilePath = QtGui.QLineEdit(self)

        gridLayout = QtGui.QGridLayout(frame1)
        gridLayout.addWidget(labelFilePath, 0, 0)
        gridLayout.addWidget(self.lineEditFilePath, 2, 0)

        # boxlay1 = QtGui.QVBoxLayout(frame1)

        # boxlay1.addLayout(gridLayout)
        gridLayout.addWidget(treeView, 1, 0)

        boxlay.addWidget(frame1)

        frame2 = QtGui.QFrame(self)
        frame2.setFrameShape(QtGui.QFrame.StyledPanel)
        frame2.setFrameShadow(QtGui.QFrame.Raised)

        treeView2 = QtGui.QTreeView(self)
        treeView2.setModel(self.model)
        treeView2.setRootIndex(indexRoot)
        treeView2.clicked.connect(self.on_treeView_clicked1)


        labelFilePath2 = QtGui.QLabel(self)
        labelFilePath2.setText("File Path:")

        self.lineEditFilePath2 = QtGui.QLineEdit(self)

        gridLayout2 = QtGui.QGridLayout(frame2)
        gridLayout2.addWidget(labelFilePath2, 0, 0)
        gridLayout2.addWidget(self.lineEditFilePath2, 2, 0)

        gridLayout2.addWidget(treeView2, 1, 0)

        boxlay.addWidget(frame2)

        frame3 = QtGui.QFrame(self)
        frame3.setFrameShape(QtGui.QFrame.StyledPanel)
        frame3.setFrameShadow(QtGui.QFrame.Raised)

        gridLayout3 = QtGui.QGridLayout(frame3)

        radio_group = QtGui.QGroupBox(u"Choose sort type:", frame3)
        radio_lay = QtGui.QVBoxLayout(radio_group)
        self.radio1 = QtGui.QRadioButton(u"Artist", radio_group)
        self.radio2 = QtGui.QRadioButton(u"Genre", radio_group)
        self.radio3 = QtGui.QRadioButton(u"Similary", radio_group)
        self.radio4 = QtGui.QRadioButton(u"None", radio_group)

        radio_lay.addWidget(self.radio1)
        radio_lay.addWidget(self.radio2)
        radio_lay.addWidget(self.radio3)
        radio_lay.addWidget(self.radio4)
        gridLayout3.addWidget(radio_group,0,0)

        but = QtGui.QPushButton(u"Save", frame3)
        but.clicked.connect(self.onclick)
        gridLayout3.addWidget(but,0,1)

        boxlay.addWidget(frame3)

    def onclick(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        sort = ''
        if self.radio1.isChecked():
            sort = "Artist"
        if self.radio2.isChecked():
            sort = 'Genre'
        if self.radio3.isChecked():
            sort = 'Sim'
        if self.radio4.isChecked():
            sort = 'None'
        config.set("paths", "search_path", self.lineEditFilePath.text())
        config.set("paths", "music_path", self.lineEditFilePath2.text())
        config.set("general", "sort", sort)

        with open("config.ini", "w") as cfg_file:
            config.write(cfg_file)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_treeView_clicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())

        filePath = self.model.filePath(indexItem)

        self.lineEditFilePath.setText(filePath)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_treeView_clicked1(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())

        filePath = self.model.filePath(indexItem)

        self.lineEditFilePath2.setText(filePath)




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    aw = MySettings()
    aw.show()
    sys.exit(app.exec_())
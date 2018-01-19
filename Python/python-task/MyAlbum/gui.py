__author__ = 'kowalski'
import sys
import threading

from PyQt4 import QtCore, QtGui

import lib.Data
import lib.file_control as FC

class MainWindow(QtGui.QMainWindow):
    def __init__(self, db, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('MyAlbum')
        self.setGeometry(100, 100, 640, 480)

        self.my_widget = MyWidget(self, db)
        self.setCentralWidget(self.my_widget)





class MyWidget(QtGui.QWidget):
    def __init__(self, parent, db):
        super(MyWidget, self).__init__(parent)
        self.db = db
        boxlay1 = QtGui.QVBoxLayout(self)


        frame1 = QtGui.QFrame(self)
        frame1.setFrameShape(QtGui.QFrame.StyledPanel)
        frame1.setFrameShadow(QtGui.QFrame.Raised)

        frame23 = QtGui.QFrame(self)
        frame23.setFrameShape(QtGui.QFrame.StyledPanel)
        frame23.setFrameShadow(QtGui.QFrame.Raised)

        frame2 = QtGui.QFrame(self)
        frame2.setFrameShape(QtGui.QFrame.StyledPanel)
        frame2.setFrameShadow(QtGui.QFrame.Raised)

        frame3 = QtGui.QFrame(self)
        frame3.setFrameShape(QtGui.QFrame.StyledPanel)
        frame3.setFrameShadow(QtGui.QFrame.Raised)

        boxlay2 = QtGui.QHBoxLayout(frame23)

        gridlay2 = QtGui.QGridLayout(frame2)

        self.tree_widget = QtGui.QTreeWidget()
        self.tree_widget.setHeaderLabels(['File name','Title', 'Artist',
                                         'Genre'])
        for i in db.music_file_list:
            QtGui.QTreeWidgetItem(self.tree_widget, [i.link, i.title, i.artist,
                                                  i.genre])

        self.tree_widget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tree_widget.resizeColumnToContents(1)
        self.tree_widget.resizeColumnToContents(2)
        self.tree_widget.resizeColumnToContents(3)
        self.tree_widget.hideColumn(0)

        gridlay2.addWidget(self.tree_widget, 0, 0)

        boxlay3 = QtGui.QVBoxLayout(frame3)

        but_update = QtGui.QPushButton(u"Update",frame3)
        but_update.clicked.connect(self.update_pressed)
        boxlay3.addWidget(but_update)

        but_settings = QtGui.QPushButton(u"Settings", frame3)
        boxlay3.addWidget(but_settings)


        boxlay1.addWidget(frame1)
        boxlay1.addWidget(frame23)
        # boxlay2.addWidget(frame1)
        boxlay2.addWidget(frame2)
        boxlay2.addWidget(frame3)


    def update_pressed(self):
        self.tree_widget.clear()
        thr = threading.Thread(target=FC.start, args=(self.db,))
        thr.start()
        thr.join()
        for i in self.db.music_file_list:
            QtGui.QTreeWidgetItem(self.tree_widget, [i.link, i.title, i.artist,
                                                  i.genre])
        self.tree_widget.resizeColumnToContents(1)
        self.tree_widget.resizeColumnToContents(2)
        self.tree_widget.resizeColumnToContents(3)

if __name__ == '__main__':
    db = lib.Data.DataBase()
    app = QtGui.QApplication(sys.argv)

    aw = MainWindow(db)
    aw.show()
    sys.exit(app.exec_())
__author__ = 'Антон'
import sys
import re
import os

from PyQt4 import QtCore, QtGui, QtWebKit

import get_page
import create_page

st = None

class MainWindow(QtGui.QMainWindow):
    def __init__(self, db, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('WIT')
        self.setGeometry(100, 100, 640, 480)

        self.my_widget = MyWidget(self, db)
        self.setCentralWidget(self.my_widget)


class MyWidget(QtGui.QWidget):
    threads = []

    def __init__(self, parent, db):
        super(MyWidget, self).__init__(parent)
        self.db = db
        boxlay = QtGui.QHBoxLayout(self)

        frame1 = QtGui.QFrame(self)
        frame1.setFrameShape(QtGui.QFrame.StyledPanel)
        frame1.setFrameShadow(QtGui.QFrame.Raised)

        gridlay = QtGui.QGridLayout(frame1)

        radio_group = QtGui.QGroupBox(u"Выбор транспорта", frame1)
        radio_lay = QtGui.QVBoxLayout(radio_group)
        self.radio1 = QtGui.QRadioButton(u"Трамвай", radio_group)
        self.radio2 = QtGui.QRadioButton(u"Троллейбус", radio_group)
        self.radio1.toggled.connect(self.radio_checked)
        self.radio2.toggled.connect(self.radio_checked)


        radio_lay.addWidget(self.radio1)
        radio_lay.addWidget(self.radio2)
        gridlay.addWidget(radio_group)


        # self.radio1.emit(QtCore.SIGNAL())

        self.list_widget = QtGui.QListWidget(frame1)
        self.list_widget.itemSelectionChanged.connect(self.button_pressed)

        gridlay.addWidget(self.list_widget)



        button1 = QtGui.QPushButton(u"Ок", frame1)
        button1.clicked.connect(self.button_pressed)
        gridlay.addWidget(button1)

        frame2 = QtGui.QFrame(self)
        frame2.setFrameShape(QtGui.QFrame.StyledPanel)
        frame2.setFrameShadow(QtGui.QFrame.Raised)

        gridlay2 = QtGui.QGridLayout(frame2)

        self.web = QtWebKit.QWebView()
        gridlay2.addWidget(self.web, 0, 0)
        # self.web.load(QtCore.QUrl("res/template.html"))

        self.lbl = QtGui.QLabel('', frame2)
        gridlay2.addWidget(self.lbl, 0, 1)

        boxlay.addWidget(frame1)
        boxlay.setStretch(0, 1)
        boxlay.addWidget(frame2)
        boxlay.setStretch(1, 2)

        self.radio1.setChecked(1)

        # self.list_widget

        # print('from main ' + str(self.threads))
        if len(self.threads) > 0:
            self.connect(self.threads[len(self.threads)-1], QtCore.SIGNAL('WEB_Update'), self.update_web)

    def radio_checked(self):
        """
        Загрузка списка остановок по выбранному транспорту
        """
        # print('radio is checked')
        sender = self.sender()
        self.list_widget.clear()
        if sender.isChecked():
            if sender.text() == 'Трамвай':
                for i in self.db.files[0]:
                    self.list_widget.addItem(i[1])
            else:
                for i in self.db.files[1]:
                    self.list_widget.addItem(i[1])
        self.list_widget.setItemSelected(self.list_widget.item(0),1)

    def button_pressed(self):
        """
        Отображение местоположения транспорта и остановки на карте
        :return:
        """

        # print('item is changed')
        global st
        # print(st)
        # print(type(st))
        selected_st = self.list_widget.selectedItems()[0].text()

        page = ''
        if self.radio1.isChecked():
            for i in self.db.files[0]:
                if selected_st == i[1]:
                    page = i[0]
        else:
            for i in self.db.files[1]:
                if selected_st == i[1]:
                    page = i[0]

        st = get_page.parse_page(page)
        # print(st)
        # print(type(st))
        self.threads.append(Update(st, parent=self))
        if len(self.threads)>1:
            self.disconnect(self.threads[len(self.threads)-2], QtCore.SIGNAL('WEB_Update'), self.update_web)
            # print('disconnected')
            self.connect(self.threads[len(self.threads)-1], QtCore.SIGNAL('WEB_Update'), self.update_web)
            # print('connected')
        self.threads[len(self.threads)-1].start()
        # print('from method ' + str(self.threads))
        #
        # print(st)
        # print(type(st))
        # if st.img is []:
        #     self.lbl.setText("Нет данных")
        # create_page.create(st)
        #
        # self.web.load(QtCore.QUrl("res/station.html"))
        #
        # s = ''
        # for i in st.trans:
        #     s += i[0] + ' ' + i[1] + ' ' + i[2] + '\n'
        # self.lbl.setText(s)

    def update_web(self, stat):
        # print('signal connected')
        if stat.img is []:
            self.lbl.setText("Нет данных")
        create_page.create(stat)

        # print(stat.page)
        num = re.search(r'\d+', stat.page).group(0)
        # print(num)
        # print(os.path.abspath(''))
        # print(os.path.exists('var\\station{}.html'.format(num)))
        self.web.load(QtCore.QUrl('var\\station{}.html'.format(num)))

        s = ''
        for i in stat.trans:
            s += i[0] + ' ' + i[1] + ' ' + i[2] + '\n'
        self.lbl.setText(s)

class Update(QtCore.QThread):
    def __init__(self, curr_st, parent=None):
        super(Update, self).__init__(parent)
        self.current_station = curr_st
        # print(self.current_station)

    def run(self):
        global st
        # print('enetered class')
        while st.page == self.current_station.page:
            # st = get_page.parse_page(st.page)

            # print(st)
            # print(type(st))
            # print('enetered loop')
            self.emit(QtCore.SIGNAL('WEB_Update'), st)
            # print('signal emitted')
            # if st.img is []:
            #      self.lbl.setText("Нет данных")
            # print('loaded lbl')
            # create_page.create(st)
            # print(1)
            # self.web.load(QtCore.QUrl("res/station.html"))
            # print(2)
            # s = ''
            # for i in st.trans:
            #     s += i[0] + ' ' + i[1] + ' ' + i[2] + '\n'
            # self.lbl.setText(s)
            #
            # time.sleep(5)
            self.sleep(15)
            st = get_page.parse_page(st.page)
            # print(self.current_station.page == st.page)
        self.exec_()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    aw = MainWindow(None)
    aw.show()
    sys.exit(app.exec_())
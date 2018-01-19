__author__ = 'Антон'
import sys
import os

from PyQt4 import QtGui

import Data
import gui

if not os.path.exists('var'):
    os.mkdir('var')
if not os.path.exists('var/OpenLayers.js'):
    os.link('res/OpenLayers.js', 'var/OpenLayers.js')

db = Data.Data()
db.update()
db.save()

app = QtGui.QApplication(sys.argv)
aw = gui.MainWindow(db)
aw.show()
sys.exit(app.exec_())


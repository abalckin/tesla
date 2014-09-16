#! /usr/bin/env python3
#
import sys
from PyQt4 import QtGui  # подключает основные модули PyQt
from forms.mainform import MainForm   # подключает модуль описания формы
import os
from PyQt4.QtCore import pyqtRemoveInputHook 

def main():
    pyqtRemoveInputHook()
    os.environ['LANG'] = "en_EN.UTF-8"
    app = QtGui.QApplication(sys.argv)  # создаёт основной объект программы
    # app.setStyle('Plastique')  # 'Windows', 'Motif', 'CDE',
    # 'Plastique', 'GTK+', 'Cleanlooks'
    mainform = MainForm(app)  # создаёт объект формы
    mainform.show()  # даёт команду на отображение объекта формы и содержимого
    app.exec_()  # запускает приложение

if __name__ == "__main__":
    sys.exit(main())

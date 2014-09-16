"""
Copyright (c) 2014 Verzunov S.N.
Institute of Informatics and Information tehnogology NAS of the Kyrgyz Republic
All rights reserved.
Code released under the GNU GENERAL PUBLIC LICENSE Version 2, June 1991
"""
#! /usr/bin/env python3
from PyQt4 import QtCore, QtGui, uic  # подключает основные модули PyQt


# прототип главной формы
class DataHeaderForm(QtGui.QDialog):
    # конструктор
    def __init__(self, header):
        super(DataHeaderForm, self).__init__()
        uic.loadUi("forms/dataheaderform.ui", self)
        self.buttonBox.accepted.connect(self.close)
        for key in header:
            if len(key[0][1:])>1:
                self.listWidget.addItem(key[0][1:])

        
        
        
        

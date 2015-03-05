"""
Copyright (c) 2014 Verzunov S.N.
Institute of Automation and Information tehnogology
NAS of the Kyrgyz Republic
All rights reserved.
Code released under the GNU GENERAL PUBLIC LICENSE Version 3, June 2007
"""
from PyQt4 import QtCore, QtGui, uic


class ProgressGroup(QtGui.QWidget):
    cancelled = QtCore.pyqtSignal()
    def __init__(self, label=None, statusbar=None):
        QtGui.QWidget.__init__(self)
        uic.loadUi("forms/progressgroup.ui", self)
        if label is not None:
            self.label.setText(label)
        self.cancelButton.clicked.connect(self._cancelled)
        if statusbar is not None:
            statusbar.clearMessage()
        
    def _cancelled(self):
        self.cancelled.emit()

    def setValue(self, value):
        self.progressBar.setValue(value)











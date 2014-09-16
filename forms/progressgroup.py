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











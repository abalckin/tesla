"""
Copyright (c) 2014 Verzunov S.N.
Institute of Informatics and Information tehnogology NAS of the Kyrgyz Republic
All rights reserved.
Code released under the GNU GENERAL PUBLIC LICENSE Version 2, June 1991
"""
#! /usr/bin/env python3
from PyQt4 import QtCore, QtGui, uic  # подключает основные модули PyQt
import sys
import matplotlib
import numpy
import scipy
from PyQt4.pyqtconfig import Configuration

# прототип главной формы
class AboutForm(QtGui.QDialog):
    # конструктор
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        uic.loadUi("forms/aboutform.ui", self)
        self.setModal(False)
        cfg = Configuration()
        self.pythonVer.setText('Python ver. {0}'.format(sys.version))
        self.qtVer.setText('Qt ver. {0}'.format(QtCore.qVersion()))
        self.matplotlibVer.setText('Matplotlib ver. {0}'.format(
            matplotlib.__version__))
        self.pyQtVer.setText('PyQt ver. {0}'.format(
            cfg.pyqt_version_str
            ))
        self.numpyVer.setText('Numpy ver. {0}'.format(
            numpy.__version__))
        self.sciPyVer.setText('Scipy ver. {0}'.format(
            scipy.__version__))


















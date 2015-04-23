#! /usr/bin/env python3
"""
Copyright (c) 2014 Verzunov S.N.
Institute of Automation and Information tehnogology
NAS of the Kyrgyz Republic
All rights reserved.
Code released under the GNU GENERAL PUBLIC LICENSE Version 3, June 2007
"""
import sys
from PyQt4 import QtGui  # connect PyQt
from forms.mainform import MainForm
import os
from PyQt4.QtCore import pyqtRemoveInputHook


def main():
    pyqtRemoveInputHook()
    os.environ['LANG'] = "en_EN.UTF-8"
    app = QtGui.QApplication(sys.argv)
    app.setStyle('Windows')  # 'Windows', 'Motif', 'CDE',
    # 'Plastique', 'GTK+', 'Cleanlooks'
    mainform = MainForm(app)
    mainform.show()
    app.exec_()

if __name__ == "__main__":
    sys.exit(main())

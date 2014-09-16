"""
Copyright (c) 2014 Verzunov S.N.
Institute of Informatics and Information tehnogology NAS of the Kyrgyz Republic
All rights reserved.
Code released under the GNU GENERAL PUBLIC LICENSE Version 2, June 1991
"""
import sys, os, random
from PyQt4 import QtGui, QtCore

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure, rcParams
from matplotlib.backend_bases import LocationEvent
from  matplotlib.backend_bases import Event
class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    canvasEnter=QtCore.pyqtSignal()
    mouseMotion = QtCore.pyqtSignal(Event)
    canvasLeave=QtCore.pyqtSignal()
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        rcParams.update({'font.size': 8})
        self._figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self._figure.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        self.compute_initial_figure()
        #
        FigureCanvas.__init__(self, self._figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self._figure.canvas.mpl_connect('motion_notify_event',
                                        lambda event: self.mouseMotion.emit(event))
        self._figure.canvas.mpl_connect('figure_enter_event',
                                        lambda event: self.canvasEnter.emit())
        self._figure.canvas.mpl_connect('figure_leave_event',
                                        lambda event: self.canvasLeave.emit())
        
    def saveFigure(self, fileName, dpi = 100):
        self._figure.savefig(fileName, dpi=dpi)
        
    def compute_initial_figure(self):
        pass

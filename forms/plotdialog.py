from PyQt4 import QtCore, QtGui,uic
from forms.mplqt4 import MyMplCanvas
import pylab
import datetime


class PlotDialog(QtGui.QDialog):
    def __call__(self, wa, parent=None, title='Plotted'):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("forms/plotdialog.ui", self)
        self.canvas = MyMplCanvas(self, width=13, height=2, dpi=100)
        self.canvasGridLayout.addWidget(self.canvas, 0,0,1,4)
        self.coordLabel.setText('')
        self.canvas.mouseMotion.connect(self.canvasMotion)
        self.canvas.canvasLeave.connect(lambda: self.coordLabel.setText(''))
        self.saveToolButton.clicked.connect(self.saveFigure)
        self.setWindowTitle(title)

    def canvasMotion(self, event):
        if event.xdata is not None and event.ydata is not None:
            self.coordLabel.setText('x=%s, y=%s' % (event.xdata, event.ydata))

    def saveFigure(self):
        title = self.windowTitle()
        self.scalogramFilename = QtGui.QFileDialog.getSaveFileName(
            None, 'Save {}'.format(title), 'images/{}.png'.format(title),
            'Portable Network Graphics (*.png)')
        self.signalCanvas.saveFigure(self.scalogramFilename, dpi=300)


class PeriodogramPlotDialog(PlotDialog):
    def __init__(self, wa, parent=None, title='Periodogram'):
        PlotDialog.__call__(self, wa, parent=parent, title=title)
        wa.plotPeriodogram(self.canvas.axes)


class ScalegramPlotDialog(PlotDialog):
    def __init__(self, wa, parent=None, title='Scalegram'):
        PlotDialog.__call__(self, wa, parent=parent, title=title)
        wa.plotScalegram(self.canvas.axes)

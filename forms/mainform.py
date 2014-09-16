"""
Copyright (c) 2014 Verzunov S.N.
Institute of Informatics and Information tehnogology NAS of the Kyrgyz Republic
All rights reserved.
Code released under the GNU GENERAL PUBLIC LICENSE Version 2, June 1991
"""
import time
from PyQt4 import QtCore, QtGui, uic  # подключает основные модули PyQt
from interfaces import spidr
from interfaces.spidr import CSVImpot
from forms.dataheaderform import DataHeaderForm
from forms.progressgroup import ProgressGroup
from forms.truescrollbar import TrueScrollBar
from forms.downloadform import DownloadForm
from forms.plotdialog import ScalegramPlotDialog, PeriodogramPlotDialog
from forms.mplqt4 import MyMplCanvas
from processing.wavelet import WaweletAnalysis as WA
from wavelets import cwt
import datetime
import inspect
import pylab
from forms.aboutform import AboutForm


class MainForm(QtGui.QMainWindow):
    def __init__(self, application):
        super(MainForm, self).__init__()
        #self.app=application    
        uic.loadUi("forms/mainform.ui", self)
        #Override VerticalScrollBar to TrueScrollBar
        self.sizeVerticalScrollBar = TrueScrollBar(self)
        self.sizeVerticalScrollBar.setMinimum(2)# min size=2**2
        self.signalGridLayout.addWidget(self.sizeVerticalScrollBar, 0, 2, 3, 1)
        self.notesVerticalScrollBar=TrueScrollBar(self)
        self.notesVerticalScrollBar.setMinimum(4)
        self.notesVerticalScrollBar.setMaximum(16)
        self.scalogramGridLayout.addWidget(self.notesVerticalScrollBar,0,2,3,1)
        self.actionQuit.triggered.connect(self.close)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionDownload.triggered.connect(self.downloadFile)
        self.actionAbout.triggered.connect(self.showAbout)
        self.actionDataHeader.triggered.connect(self.showDataHeader)
        self.actionClose.triggered.connect(self.closeFile)
        self.sizeVerticalScrollBar.invValueChanged.connect(self.sizeChanged)
        self.offsetHorizontalScrollBar.valueChanged.connect(self.offsetChanged)
        self.actionPlot_signal.triggered.connect(self.plotSignal)
        self.actionSave_image_signal_as.triggered.connect(self.saveSignalAs)
        self.actionSave_scalogram_as.triggered.connect(self.saveScalogramAs)
        self.actionPlot_periodogram.triggered.connect(self.plotPeriodogram)
        self.actionPlot_scalegram.triggered.connect(self.plotScalegram)
        self.offsetHorizontalScrollBar.sliderMoved.connect(self.offsetMoved)
        self.sizeVerticalScrollBar.invSliderMoved.connect(self.sizeMoved)
        self.scaleHorizontalScrollBar.valueChanged.connect(self.scaleCanged)
        self.scaleHorizontalScrollBar.sliderMoved.connect(self.scaleMoved)
        self.notesVerticalScrollBar.invValueChanged.connect(self.notesChanged)
        self.notesVerticalScrollBar.invSliderMoved.connect(self.notesMoved)
        self.waveletComboBox.currentIndexChanged.connect(self.replot)
        self.orderSpinBox.valueChanged.connect(self.replot)
        self.omega0SpinBox.valueChanged.connect(self.replot)
        self.minHspinBox.valueChanged.connect(self.minHchanged)
        self.maxHspinBox.valueChanged.connect(self.maxHchanged)
        self.actionDetrend.triggered.connect(self.detrendData)
        self.waveletComboBox.currentIndexChanged.connect(self.waveletChanged)
        self.lock = True
        for  name,obj  in inspect.getmembers(cwt):
            #print(obj)
        
            if inspect.isclass(obj):
                if obj.__base__.__name__=='Cwt':
                    self.waveletComboBox.addItem(name,obj)
        
        self.moveToCenter()
    def canvasEnter(self):
        self.coord = QtGui.QLabel(self)
        self.statusbar.addWidget(self.coord)
    def canvasLeave(self):
        self.statusbar.removeWidget(self.coord)
    def canvasMotion(self, event):
        if event.xdata is not None and event.ydata is not None:
            self.coord.setText(
                'x=%s, y=%s' %
                (pylab.num2date(event.xdata).strftime('%d.%m.%y %H:%M'),
                event.ydata))
    def createCanvases(self):
        self.signalCanvas = MyMplCanvas(self, width=13, height=2, dpi=100)
        self.signalGridLayout.addWidget(self.signalCanvas,0,0,3,2)
        self.scalogramCanvas = MyMplCanvas(self, width=5, height=4, dpi=100)
        self.scalogramGridLayout.addWidget(self.scalogramCanvas,0,0,3,2)
        self.signalCanvas.canvasEnter.connect(self.canvasEnter)
        self.signalCanvas.mouseMotion.connect(self.canvasMotion)
        self.signalCanvas.canvasLeave.connect(self.canvasLeave)
        self.scalogramCanvas.canvasEnter.connect(self.canvasEnter)
        self.scalogramCanvas.mouseMotion.connect(self.canvasMotion)
        self.scalogramCanvas.canvasLeave.connect(self.canvasLeave)
    def moveToCenter(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        mysize = self.geometry()
        hpos = ( screen.width() - mysize.width() ) / 2
        vpos = ( screen.height() - mysize.height() ) / 2
        self.move(hpos, vpos)
        
    def openFile(self, fileName=None):
        if fileName is None or fileName == False:
            fileName = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                     './data',
        'Geomagnetic variations (*.gmv);;Solar wind Kp estimation (*.ske)')
        if QtCore.QFile.exists(fileName):
            if self.actionClose.isEnabled():
                self.closeFile() 
            self.progress=ProgressGroup('Loading data ...',self.statusbar)
            self.statusbar.insertWidget(0, self.progress)
            self.csv=CSVImpot(fileName)
            self.csv.notifyProgress.connect(self.progress.setValue)
            self.csv.loaded.connect(self.loadFile)
            self.progress.cancelled.connect(self.openFileTeminate)
            self.csv.start()
            
    def openFileTeminate(self):
        self.statusbar.removeWidget(self.progress)
        self.statusbar.showMessage('Load cancelled by user!',3000)
        self.csv.terminate()
            
    def loadFile(self):
        self.statusbar.removeWidget(self.progress)
        self.createCanvases()
        self.wa = WA(self.csv.time, self.csv.value)
        sizePow2 = self.wa.getMaxLengthAsPower2()
        self.sizeVerticalScrollBar.setMaximum(sizePow2)
        self.offsetMoved(0)
        self.notesVerticalScrollBar.setValue(
            self.notesVerticalScrollBar.minimum())
        self.lock = False
        self.sizeVerticalScrollBar.setValue(sizePow2)
        self.enableControlForOpen()

    def sizeChanged(self, value):
        self.sizeLabel.setText('2^%s' % value)
        self.offsetHorizontalScrollBar.setMaximum(self.wa.getLength()-2**value)
        self.scaleHorizontalScrollBar.setMaximum(2**value)
        self.replot()
    
    def scaleCanged(self,value):
        self.scaleLabel.setText(str(value))
        self.replot()
        
    def scaleMoved(self,value):
        self.scaleLabel.setText(str(value))
        
    def offsetMoved(self,value):
        self.offsetLabel.setText(self.wa.getDate(value).strftime('%d.%m.%y'))
        
    def sizeMoved(self, value):
        #value = self.wa.getMaxLengthAsPower2()-value
        self.sizeLabel.setText('2^%s' % value)
    
    def offsetChanged(self, value):
        print ('offset chang')
        self.offsetLabel.setText(self.wa.getDate(value).strftime('%d.%m.%y'))
        self.replot()

    def notesChanged(self, value):
        self.notesLabel.setText(str(value))
        self.replot()

    def notesMoved(self,value):
        self.notesLabel.setText(str(value))

    def plotPeriodogram(self):
        self.periodogramForm = PeriodogramPlotDialog(self.wa, parent=self)
        self.periodogramForm.show()

    def plotScalegram(self):
        self.scalegramForm = ScalegramPlotDialog(self.wa, parent=self)
        self.scalegramForm.show()

    def showDataHeader(self):
        self.dataHeaderForm = DataHeaderForm(self.csv.header)
        self.dataHeaderForm.show()

    def showAbout(self):
        aboutForm = AboutForm(self)
        aboutForm.exec_()
        
    def closeFile(self):
        self.clearCanvases()
        self.disableControlForClose()

        
    def plotSignal(self):
        print('size%s'% self.sizeVerticalScrollBar.value())
        self.wa.plotSignal(self.signalCanvas.axes,
        self.offsetHorizontalScrollBar.value(),
            2**self.sizeVerticalScrollBar.value(),
            xlabel = 'Date',
            ylabel = 'nT')
        self.signalCanvas.draw()
    
    def plotScalogram(self):
        self.progress = ProgressGroup('Plot scalogram ...', self.statusbar)
        self.statusbar.insertWidget(0, self.progress)
        self.wa.plotted.connect(self.scalogramPlotted)
        self.wa.notifyProgress.connect(self.progress.setValue)
        self.wa.cancelled.connect(self.scalogramPlotted)
        self.progress.cancelled.connect(self.wa.cancelScalogram)
        self.wa.plotScalogram(
            self.scalogramCanvas.axes,
            offset=self.offsetHorizontalScrollBar.value(),
            size=2**self.sizeVerticalScrollBar.value(),
            largestscale=self.scaleHorizontalScrollBar.value(),
            notes=self.notesVerticalScrollBar.value(),
            wavelet=self.waveletComboBox.itemData(
                self.waveletComboBox.currentIndex()),
            omega0=self.omega0SpinBox.value(),
            order=self.orderSpinBox.value(),
            min_h=self.minHspinBox.value(),
            max_h=self.maxHspinBox.value())

    def scalogramPlotted(self):
        self.statusbar.removeWidget(self.progress)
        self.statusbar.showMessage('Finished.', 100)
        self.scalogramCanvas.draw()
        self.signalGroupBox.setEnabled(True)
        self.scalogramGroupBox.setEnabled(True)
        self.toolGroupBox.setEnabled(True)
        self.lock = False

    def replot(self):
        if self.lock:
            return
        else:
            self.lock = True
            self.signalGroupBox.setEnabled(False)
            self.scalogramGroupBox.setEnabled(False)
            self.toolGroupBox.setEnabled(False)
            self.plotSignal()
            self.plotScalogram()

    def disableControlForClose(self):
        self.lock = True
        self.signalGroupBox.setEnabled(False)
        self.scalogramGroupBox.setEnabled(False)
        self.actionClose.setEnabled(False)
        self.signalGroupBox.setEnabled(False)
        self.actionSave_image_signal_as.setEnabled(False)
        self.actionSave_scalogram_as.setEnabled(False)
        self.actionDataHeader.setEnabled(False)
        self.toolGroupBox.setEnabled(False)
        self.actionDetrend.setEnabled(False)
        self.actionPlot_periodogram.setEnabled(True)
        self.actionPlot_scalegram.setEnabled(True)

    def clearCanvases(self):
        self.signalCanvas.close()
        self.scalogramCanvas.close()
        
    def enableControlForOpen(self):
        self.signalGroupBox.setEnabled(True)
        self.scalogramGroupBox.setEnabled(True)
        self.actionSave_image_signal_as.setEnabled(True)
        self.actionSave_scalogram_as.setEnabled(True)
        self.actionPlot_periodogram.setEnabled(True)
        self.actionPlot_scalegram.setEnabled(True)
        self.actionDataHeader.setEnabled(True)
        self.actionClose.setEnabled(True)
        self.toolGroupBox.setEnabled(True)
        self.actionDetrend.setEnabled(True)
    def saveSignalAs(self):
        self.signaFilename = QtGui.QFileDialog.getSaveFileName(None,'Save signal',
                            './images/signal.png','Portable Network Graphics (*.png)')
        self.signalCanvas.saveFigure(self.signaFilename,dpi=300)

    def saveScalogramAs(self):
        self.scalogramFilename = QtGui.QFileDialog.getSaveFileName(None, 'Save figure',
                            './images/scalogram.png','Portable Network Graphics (*.png)')
        self.scalogramCanvas.saveFigure(self.scalogramFilename,dpi=300)

    def minHchanged(self, value):
        self.maxHspinBox.setMinimum(value)
        self.replot()

    def maxHchanged(self, value):
        self.minHspinBox.setMaximum(value)
        self.replot()

    def downloadFile(self):
        self.downloadForm = DownloadForm(self)
        self.downloadForm.show()

    def detrendData(self):
        self.wa.detrend()
        self.replot()

    def waveletChanged(self, value):
        wavelet = self.waveletComboBox.itemData(value)
        if wavelet.__name__ == 'Morlet' or wavelet.__name__ == 'MorletReal':
            self.orderSpinBox.setEnabled(False)
            self.omega0SpinBox.setEnabled(True)
        else:
            self.orderSpinBox.setEnabled(True)
            self.omega0SpinBox.setEnabled(False)
            
#       import pdb
#        pdb.set_trace()




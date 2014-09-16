#! /usr/bin/env python3
from PyQt4 import QtCore, QtGui, uic  # подключает основные модули PyQt
import numpy as np
import datetime as dt
import os
from interfaces.spidr import CSVDownload
from forms.progressgroup import ProgressGroup
# прототип главной формы


class DownloadForm(QtGui.QDialog):
    # конструктор
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        uic.loadUi("forms/downloadform.ui", self)
        self.setModal(False)
        self.parent = parent
        self.fileLabel.linkActivated.connect(self.selectFile)
        self.stepComboBox.currentIndexChanged.connect(self.changeStep)
        self.obsComboBox.currentIndexChanged.connect(self.changeObs)
        self.obsComboBox.currentIndexChanged.connect(self.changeFile)
        self.fromDateEdit.dateChanged.connect(self.changeFrom)
        self.fromDateEdit.dateChanged.connect(self.changeFile)
        self.toDateEdit.dateChanged.connect(self.changeTo)
        self.toDateEdit.dateChanged.connect(self.changeFile)
        self.seriesComboBox.currentIndexChanged.connect(self.changeTo)
        self.buttonBox.accepted.connect(self.accept)
        self.stepComboBox.setCurrentIndex(0)

    def changeStep(self, value):
        if value == 0:
            file = 'forms/resource/obsmin.csv'
            self.step = 'min'
        elif value == 1:
            file = 'forms/resource/obshr.csv'
            self.step = 'hr'
        self.observatoryes = np.genfromtxt(file,
                                           dtype=['S5', 'S32',
                                                  'f2', 'f2', 'S32'],
                                           names=('Code', 'Name',
                                                  'Lat', 'Lon',
                                                  'Interval'),
                                           delimiter=",",
                                           comments='#')
        self.obsComboBox.addItems(self.observatoryes['Name'].astype(str))
        self.obsComboBox.setCurrentIndex(0)

    def changeObs(self, value):
        # import pdb; pdb.set_trace()
        interval = self.observatoryes['Interval'][value].astype(str)
        date1 = dt.datetime.strptime(interval[0:10], '%Y-%m-%d')
        date2 = dt.datetime.strptime(interval[-10:-1], '%Y-%m-%d')
        self.fromDateEdit.setMinimumDate(date1)
        self.toDateEdit.setMaximumDate(date2)

    def changeFile(self, _):
        fileName = ''.join((
            self.observatoryes['Code'][self.obsComboBox.currentIndex()].astype(str),
            self.fromDateEdit.date().toString(),
            self.toDateEdit.date().toString(),
            self.seriesComboBox.currentText(),
            '.gmv')).replace(' ', '')
        self.defaultFileName = ''.join((
            os.getcwd(),
            os.sep,
            'data',
            os.sep,
            fileName
            ))
        self.setFileName(self.defaultFileName)
         
    def selectFile(self):
        filename = QtGui.QFileDialog.getSaveFileName(self,
                                                     'Save file',
                                                     './data',
                                                     'Geomagnetic variations\
                                                     (*.gmv)')
        self.setFileName(filename)

    def setFileName(self, fileName):
        self.fileName = fileName
        self.fileLabel.setText(
            "<html> <a style = 'text-decoration:none'href ='link'>\
        {0}</a></html>".format(os.path.basename(fileName)))

    def changeFrom(self):
        self.toDateEdit.setMinimumDate(
            self.fromDateEdit.date())

    def changeTo(self):
        self.fromDateEdit.setMaximumDate(
            self.toDateEdit.date())

    def accept(self):
        code = self.observatoryes['Code'][self.obsComboBox.currentIndex()].astype(str)
        fromDate = self.fromDateEdit.date().toPyDate()
        toDate = self.toDateEdit.date().toPyDate()
        url = """http://spidr.ngdc.noaa.gov/spidr/servlet/GetData2?\
        format=csv&\
        datefrom={0}T00:00:00UTC&\
        dateto={1}T23:59:59UTC&\
        dataset=geom_{2}@Geom.{3}&\
        location={4}""".replace(' ', '').format(
            fromDate,
            toDate,
            self.seriesComboBox.currentText(),
            self.step,
            code[0:3])
        print (url)
        self.progress = ProgressGroup()
        self.message = QtGui.QLabel('Downloading data ...')
        self.formLayout.addRow(self.message, self.progress)
        self.dwl = CSVDownload(url, self.fileName)
        self.dwl.notifyProgress.connect(self.progress.setValue)
        self.dwl.loaded.connect(self.loadFile)
        self.progress.cancelled.connect(self.downloadFileTeminate)
        self.label = self.formLayout.labelForField(self.progress)
        self.dwl.start()

    def loadFile(self):
        if self.parent is not None:
            self.parent.openFile(self.fileName)
        self.close()

    def downloadFileTeminate(self):
        self.dwl.terminate()
        if self.label is not None:
            self.label.deleteLater()
        self.progress.deleteLater()






















"""
Copyright (c) 2014 Verzunov S.N.
Institute of Informatics and Information tehnogology NAS of the Kyrgyz Republic
All rights reserved.
Code released under the GNU GENERAL PUBLIC LICENSE Version 2, June 1991
"""
#http://spidr.ngdc.noaa.gov/spidr/servlet/GetData2?format=xml&datefrom=1980-01-01T00:00:00UTC&dateto=2001-01-01T00:00:00UTC&dataset=geom_f@Geom.hr&location=BOU
import csv
from PyQt4 import QtCore
import numpy as np
import datetime as dt
import os
import urllib.request


class CSVDownload(QtCore.QThread):
    notifyProgress = QtCore.pyqtSignal(int)
    loaded = QtCore.pyqtSignal()

    def __init__(self, url, fileName):
        QtCore.QThread.__init__(self)
        self.url = url
        self.fileName = fileName

    def run(self):
        urllib.request.urlretrieve(self.url, self.fileName, self.notify)
        self.loaded.emit()

    def notify(self, blocknum, blocksize, totalsize):
            self.notifyProgress.emit(blocknum % 100)


class CSVImpot(QtCore.QThread):
    notifyProgress = QtCore.pyqtSignal(int)
    loaded = QtCore.pyqtSignal()

    def __init__(self, fileName):
        QtCore.QThread.__init__(self)
        self.fileName = fileName
        self.header=[]

    def run(self):
        _, fileExtension = os.path.splitext(self.fileName)
        if fileExtension == '.gmv':
            print('Geomagnetic variation')
            with open(self.fileName, 'rt') as csvdata:
                date = []
                value = []
                for row in csv.reader(csvdata):
                    if ('#' in row[0]):
                        self.header.append(row)
                    else:
                        date.append(row[0])
                        value.append(row[1])
            self.notifyProgress.emit(20)
            signal = np.array((date, value), dtype=np.dtype('a25'))
            signal = signal[:, np.logical_not(
                np.isnan(signal[1, :].astype(np.float)))]
            self.notifyProgress.emit(40)
            self.value = signal[1, :].astype(np.float)
            # self.value=np.nan_to_num(self.value)
            self.notifyProgress.emit(60)
            self.time = signal[0, :].astype(np.datetime64).astype(dt.datetime)
            self.notifyProgress.emit(80)
            self.loaded.emit()
        elif fileExtension == '.ske':
            print('Kp estimation')
            with open(self.fileName, 'rt') as csvdata:
                date = []
                value = []
                for row in csv.reader(csvdata, delimiter=' '):
                    if ('#' in row[0]):
                        self.header.append(row)
                    else:
                        print(row)
                        if int(row[7]) < 2:
                            date.append(
                                dt.datetime.strptime(
                                    ''.join((row[0], row[1], row[2],
                                            row[4])),
                                    '%Y%m%d%H%M')),
                            value.append(float(row[-1])-float(row[-14]))  #4h
                            # value.append(float(row[-1])-float(row[19]))  # 1h
            self.notifyProgress.emit(20)
            signal = np.array((date, value), dtype=np.dtype('a25'))
            signal = signal[:, np.logical_not(
                np.isnan(signal[1, :].astype(np.float)))]
            self.notifyProgress.emit(40)
            self.value = signal[1, :].astype(np.float)
            # self.value=np.nan_to_num(self.value)
            self.notifyProgress.emit(60)
            self.time = signal[0, :].astype(np.datetime64).astype(dt.datetime)
            self.notifyProgress.emit(80)
            self.loaded.emit()

    def __del__(self):
        self.wait()

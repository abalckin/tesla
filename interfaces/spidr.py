"""
Copyright (c) 2014 Verzunov S.N.
Institute of Automation and Information tehnogology
NAS of the Kyrgyz Republic
All rights reserved.
Code released under the GNU GENERAL PUBLIC LICENSE Version 3, June 2007
"""
# http://spidr.ngdc.noaa.gov/spidr/servlet/GetData2?format=xml&datefrom=1980-01-
# 01T00:00:00UTC&dateto=2001-01-01T00:00:00UTC&dataset=geom_f@Geom.hr&location=BOU
import csv
from PyQt4 import QtCore
import numpy as np
import datetime as dt
import os
import urllib.request
import matplotlib.dates as dates
from scipy.signal import cspline1d, cspline1d_eval


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
        self.header = []
        self.interpolate = True

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
                            value.append(float(row[-1])-float(row[-14]))  # 4h
                            # value.append(float(row[-1])-float(row[19]))  # 1h
            self.notifyProgress.emit(20)
        signal_src = np.array((date, value), dtype=np.dtype('a25'))
        signal = signal_src[:, np.logical_not(
            np.isnan(signal_src[1, :].astype(np.float)))]
        self.notifyProgress.emit(60)
        if self.interpolate:
            self.time = signal_src[0, :].astype(np.datetime64).astype(
                dt.datetime)
            dx = dates.date2num(self.time[1])-dates.date2num(self.time[0])
            cj = cspline1d(signal[1, :].astype(float))
            self.value = cspline1d_eval(cj, dates.date2num(self.time),
                                        dx=dx,
                                        x0=dates.date2num(self.time[0]))
        else:
            self.time = dates.signal[0, :].astype(np.datetime64).astype(
                dt.datetime)
            self.value = signal[1, :].astype(np.float)
        self.notifyProgress.emit(80)
        self.loaded.emit()

    def __del__(self):
        self.wait()

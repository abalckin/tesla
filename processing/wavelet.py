"""
Copyright (c) 2014 Verzunov S.N.
Institute of Automation and Information tehnogology
NAS of the Kyrgyz Republic
All rights reserved.
Code released under the GNU GENERAL PUBLIC LICENSE Version 3, June 2007
"""
import numpy as np
import pylab as plb
import wavelets.cwt as wave
from PyQt4 import QtCore


class WaveletTransform(QtCore.QThread):
    notifyProgress = QtCore.pyqtSignal(int)
    transformed = QtCore.pyqtSignal(wave.Cwt)

    def __init__(self, data, wavelet=wave.Morlet,
                 scaling='log', notes=8, largestscale=4, order=2., omega0=5.):
        QtCore.QThread.__init__(self)
        self._wavelet = wavelet
        self._scaling = scaling
        self._notes = notes
        self._largestscale = largestscale
        self._order = order
        self._omega0 = omega0
        self._data = data
 

    def run(self):
        cw = self._wavelet(self._data, self.transformed, self.notifyProgress,
                           scaling=self._scaling, notes=self._notes,
                           omega0=self._omega0,
                           largestscale=self._largestscale,
                           order=self._order)
        return cw


class WaweletAnalysis(QtCore.QObject):
    notifyProgress = QtCore.pyqtSignal(int)
    plotted = QtCore.pyqtSignal()
    cancelled = QtCore.pyqtSignal()

    def __init__(self, time, values):
        QtCore.QObject.__init__(self)
        self._time = time
        self._values = values
        self._maxLength = 1 << ((self._values.shape[-1]-1).bit_length()-1)
        self._detrend = False
        
    def plotSignal(self, axes, offset, size, xlabel='', ylabel='', style='-'):
        if self._detrend:
            self._v = plb.detrend(self._values[offset:offset+size], key='linear')
        else:
            self._v = self._values[offset:offset+size]
        axes.plot_date(self._time[offset:offset+size],
                       self._v, style)

    def _plotScalogram(self, cw):
        self._cw = cw
        scales = cw.getscales()
        pwr = cw.getpower()
        y = cw.fourierwl*scales
        plotcwt = np.clip(pwr, self._min_h, self._max_h)
        self._axes.imshow(plotcwt,
                          cmap=plb.cm.hot_r,
                          extent=[plb.date2num(self._x[0]),
                                  plb.date2num(self._x[-1]),
                                  y[-1], y[0]], aspect='auto',
                                  interpolation=None)
        self._axes.xaxis_date()
        if self._scaling == "log":
            self._axes.set_yscale('log')
        self._axes.set_ylim(y[0], y[-1])
        self.plotted.emit()

    def plotScalogram(self, axes, size, offset, max_h=1000., min_h=0.,
                      p_label='', s_label='',
                      wavelet=wave.Morlet, scaling='log',
                      order=2, omega0=5.,
                      notes=4, largestscale=4):
        print(size)
        print(largestscale)
        if self._detrend:
            self._v = plb.detrend(self._values[offset:offset+size], key='linear')
        else:
            self._v = self._values[offset:offset+size]
        
        self._y = self._v
        self._x = self._time[offset:offset+size]
        self._min_h = min_h
        self._max_h = max_h
        self._axes = axes
        self._scaling = scaling
        self._wt = WaveletTransform(self._y, wavelet=wavelet, scaling=scaling,
                                    notes=notes,
                                    largestscale=size//largestscale,
                                    order=order,
                                    omega0=omega0)
        self._wt.transformed.connect(self._plotScalogram)
        self._wt.notifyProgress.connect(self._notifyProgress)
        self._wt.terminated.connect(lambda: self.cancelled.emit())
        self._wt.start()

    def plotPeriodogram(self, axes, xlabel='Power',
                        ylabel='Period', scaling='log'):
        # projected fourier spectrum
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)
        f = np.fft.fftfreq(self._x.shape[-1])
        fspec = np.abs(np.fft.fft(self._y))
        u = np.abs(fspec)[0:-self._x.shape[-1]/2]
        v = 1/f[0:-self._x.shape[-1]/2]
        if scaling == 'log':
            axes.loglog(u, v, 'b-')  # ,s,sv,'g-')
        else:
            axes.semilogx(u, v, 'b-')  # ,s,sv,'g-')
            axes.set_xlim(1e-1, np.max(fspec))
            axes.set_ylim(self._y[0], self._y[-1])

    def plotScalegram(self, axes, xlabel='Power',
                      abel='Period', scaling='log', min_h=0., max_h=1000.):
        pwr = self._cw.getpower()
        scales = self._cw.getscales()
        scalespec = np.sum(pwr, axis=1)/scales  # calculate scale spectrum
        axes.set_xlabel('Power')
        axes.set_ylabel('Period')
        vara = 1.0
        y = self._cw.fourierwl*scales
        if scaling == "log":
            axes.loglog(scalespec/vara+0.01, y, 'b-')
        else:
            axes.semilogx(scalespec/vara+0.01, y, 'b-')
        axes.set_xlim(1e-1, np.max(scalespec))
        axes.set_ylim(y[0], y[-1])

    def plotSceleton(self, axes, xlabel='Power',
                     ylabel='Period', scaling='log', min_h=0., max_h=1000.):
        cw = self._cw

        scales = cw.getscales()
        pwr = self.getSceleton(cw.getpower())
        y = cw.fourierwl*scales
        axes.imshow(pwr[0], cmap=plb.cm.hot_r,
                    extent=[plb.date2num(self._x[0]),
                            plb.date2num(self._x[-1]),
                            y[-1], y[0]], aspect='auto', interpolation=None)
        axes.xaxis_date()
        axes.imshow(pwr[1], cmap=plb.cm.hot_r,
                    extent=[plb.date2num(self._x[0]),
                    plb.date2num(self._x[-1]),
                    y[-1], y[0]], aspect='auto',
                    interpolation=None)
        axes.xaxis_date()
        if scaling == "log":
            axes.set_yscale('log')
        axes.set_ylim(y[0], y[-1])

    def cancelScalogram(self):
        self._wt.terminate()

    def _notifyProgress(self, value):
        self.notifyProgress.emit(value)

    def getMaxLengthAsPower2(self):
        return (self._values.shape[-1]-1).bit_length()-1

    def getLength(self):
        return self._values.shape[-1]

    def getDate(self, index):
        return self._time[index]

    def detrend(self, val):
        self._detrend = val

    def getSceleton(self, im):
        imp1 = np.pad(im, ((1, 1), (0, 0)), 'minimum')
        imp0 = np.pad(im, ((0, 0), (1, 1)), 'minimum')
        row = (np.diff(np.sign(np.diff(imp0, axis=1)), axis=1) < 0)
        col = (np.diff(np.sign(np.diff(imp1, axis=0)), axis=0) < 0)
        return (row*im, col*im)

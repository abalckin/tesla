"""
Copyright (c) 2014 Verzunov S.N.
Institute of Informatics and Information tehnogology NAS of the Kyrgyz Republic
All rights reserved.
Code released under the GNU GENERAL PUBLIC LICENSE Version 2, June 1991
"""
import numpy as np
import pylab as plb
import datetime as dt
import wavelets.cwt as wave
import time as profiler
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
                           omega0=self._omega0, largestscale=self._largestscale,
                           order=self._order)
        return cw

    
class WaweletAnalysis(QtCore.QObject):
    notifyProgress = QtCore.pyqtSignal(int)
    plotted = QtCore.pyqtSignal()
    cancelled = QtCore.pyqtSignal()
    def __init__(self,time,values):
        QtCore.QObject.__init__(self)
        self._time=time
        self._values=values
        self._maxLength=1<<((self._values.shape[-1]-1).bit_length()-1)
        
    def plotSignal(self,axes,offset,size,xlabel='',ylabel='',style='-'):
        axes.plot_date(self._time[offset:offset+size],
            self._values[offset:offset+size],style)
        #yearsFmt = plb.DateFormatter(dataFormatter)
        #axes.xaxis.set_major_formatter(yearsFmt)
        #axes.set_xlabel(xlabel)
        #axes.set_ylabel(ylabel)
    def _plotScalogram(self, cw):
        self._cw=cw
        start=profiler.time()
        scales=cw.getscales()     
        cwt=cw.getdata()
        pwr=cw.getpower()
        scalespec=np.sum(pwr,axis=1)/scales # calculate scale spectrum
        # scales
        y=cw.fourierwl*scales
        #x=np.arange(Nlo*1.0,Nhi*1.0,1.0)
        #mpl.xlabel('Date')
        #mpl.ylabel('Period, %s' % p_label)
        plotcwt=np.clip(pwr,self._min_h,self._max_h)
        print(y)
        print("Matr")
        print(plotcwt.shape)
        im=self._axes.imshow(plotcwt,cmap=plb.cm.hot_r,
        extent=[plb.date2num(self._x[0]),plb.date2num(self._x[-1]),
        y[-1],y[0]],aspect='auto', interpolation=None)
        self._axes.xaxis_date()
        #yearsFmt = mpl.DateFormatter('%m.%y')
        #axes.xaxis.set_major_formatter(yearsFmt)
        #mpl.gcf().autofmt_xdate()
        if self._scaling=="log": self._axes.set_yscale('log')
        self._axes.set_ylim(y[0],y[-1])
        print('Plot - %.03f s' % (profiler.time()-start))
        self.plotted.emit()

    def plotScalogram(self, axes,size,offset, max_h=1000., min_h=0.,p_label='', s_label='',wavelet=wave.Morlet, scaling='log',
        order=2, omega0=5.,notes=4, largestscale=4):
        print(size)
        print(largestscale)
        self._y=self._values[offset:offset+size]
        self._x=self._time[offset:offset+size]
        self._min_h=min_h
        self._max_h=max_h
        self._axes=axes
        self._scaling=scaling
        self._wt=WaveletTransform(self._y,wavelet=wavelet, scaling=scaling,
                    notes=notes, largestscale=size//largestscale, order=order,
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
        # vara = 1.0
        f = np.fft.fftfreq(self._x.shape[-1])
        fspec = np.abs(np.fft.fft(self._y))
        u = np.abs(fspec)[0:-self._x.shape[-1]/2]
        v = 1/f[0:-self._x.shape[-1]/2]
        # w=np.ones(win_len,'d')
        # s=np.convolve(w/w.sum(),u,mode='valid')
        # sv=v[win_len/2:-win_len/2+1]
        # print(len(s),len(sv))
        if scaling == 'log':
            axes.loglog(u, v, 'b-')  # ,s,sv,'g-')
        else:
            axes.semilogx(u, v, 'b-')  # ,s,sv,'g-')
            axes.set_xlim(1e-1,np.max(fspec))
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

    def cancelScalogram(self):
        self._wt.terminate()
        
    def _notifyProgress(self,value):
        self.notifyProgress.emit(value)
    
    def getMaxLengthAsPower2(self):
        return (self._values.shape[-1]-1).bit_length()-1
    
    def getLength(self):
        return self._values.shape[-1]

    def getDate(self, index):
        return self._time[index]

    def detrend(self):
        self._values = plb.detrend(self._values, key='linear')

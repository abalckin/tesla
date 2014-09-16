"""
Copyright (c) 2014 Verzunov S.N.
Institute of Informatics and Information tehnogology NAS of the Kyrgyz Republic
All rights reserved.
Code released under the GNU GENERAL PUBLIC LICENSE Version 2, June 1991
"""
from PyQt4 import QtGui, QtCore
class TrueScrollBar(QtGui.QScrollBar):
    invValueChanged=QtCore.pyqtSignal(int)
    invSliderMoved=QtCore.pyqtSignal(int)

    def __init__(self,label, parent=None):
        QtGui.QScrollBar.__init__(self,parent)
        self.__value=0
        self.setOrientation=QtCore.Qt.Vertical
        self.valueChanged.connect(self.__change)
        self.sliderMoved.connect(self.__moved)
        self.setTracking(False)
    def __change(self,value):
        self.__value=self.maximum() - value+self.minimum()
        self.invValueChanged.emit(self.__value)
        print('emit %s'%self.__value)

    def __moved(self, value):
        print('Move %s'% value)
        value=self.maximum() - value + self.minimum()
        self.invSliderMoved.emit(value)
    
    def setValue(self,value):
        print('setValue%s'%value)
        self.__value=value
        self.invValueChanged.emit(value)
        value=self.maximum()-value+self.minimum()
        #self.setSliderPosition(value)
        QtGui.QScrollBar.setValue(self,value)
        
        
    def value(self):
        print('Getvalue=%s'%self.__value)
        return self.__value


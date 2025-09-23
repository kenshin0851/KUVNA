# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 12:08:55 2025

@author: Sang-Wook Kim
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
#from superqt import QRangeSlider
from qtrangeslider import QRangeSlider

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from KUVNA_data import KUVNA_data


form_class = uic.loadUiType("vna_frontpanel3.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.startfreq = 100
        self.stopfreq = 6000
        self.NoP = 236
        self.RBW = 10
        self.power = -10
        
        self.dataFrag = False
        self.dispmode=0
        self.port = 1
        self.viewID = 0
        self.viewFormat = 0
        
        self.s11chkFlag = [2,2,2,2]
        self.s21chkFlag = [0,0,0,0]
        self.s22chkFlag = [0,0,0,0]
        self.s12chkFlag = [0,0,0,0]

        self.initUI()
        self.initSignal()     
        
        self.uvna = KUVNA_data() 
        self.uvna2 = KUVNA_data()
        self.portA = None
        self.portB = None

        
    def initUI(self):
        
        self.rhslider_frequency.setRange(self.startfreq, self.stopfreq)
        self.rhslider_frequency.setValue((self.startfreq, self.stopfreq))
        
        self.hslider_power.setRange(-26, 0)
        self.hslider_power.setSingleStep(2)
        self.hslider_power.setValue(self.power)
        
        self.hslider_nopoint.setRange(2, 1001)
        self.hslider_nopoint.setSingleStep(1)
        self.hslider_nopoint.setValue(self.NoP)
        
        self.hslider_rbw.setRange(1, 140)
        self.hslider_rbw.setSingleStep(1)
        self.hslider_rbw.setValue(self.RBW)
        
        self.ledit_startfreq.setText(str(self.startfreq))
        self.ledit_stopfreq.setText(str(self.stopfreq))
        self.ledit_nopoint.setText(str(self.NoP))
        self.ledit_rbw.setText(str(self.RBW))
        self.ledit_power.setText(str(self.power))
       
        self.rbtn_singleport.setChecked(True)
        
        self.rbtn_singledisp.setChecked(True)
        
        self.ckbox_s11.setCheckState(2)

        
        self.ckbox_s11.setTristate(False)
        self.ckbox_s21.setTristate(False)
        self.ckbox_s12.setTristate(False)
        self.ckbox_s22.setTristate(False)
        
        self.cbbox_view.addItem('1')
        
        self.cbbox_format.addItem('dB')
        self.cbbox_format.addItem('linear')
        
        self.ckbox_open_2.setEnabled(False)
        
    def initSignal(self):      
        #주파수 조절
        self.rhslider_frequency.valueChanged.connect(self.freqchanged)
        self.ledit_startfreq.returnPressed.connect(self.startfreqchanged)
        self.ledit_stopfreq.returnPressed.connect(self.stopfreqchanged)
        
        #파워 조절
        self.hslider_power.valueChanged.connect(self.powerSliderChanged)
        self.ledit_power.returnPressed.connect(self.powerLeditChanged)
        
        #점 갯수 조절
        self.hslider_nopoint.valueChanged.connect(self.NOPSliderChanged)
        self.ledit_nopoint.returnPressed.connect(self.NOPLeditChanged)
        
        #파장 길이 조절
        self.hslider_rbw.valueChanged.connect(self.RBWSliderChanged)
        self.ledit_rbw.returnPressed.connect(self.RBWLeditChanged)
        
        # 측정 버튼
        self.btn_measure.clicked.connect(self.measure)
 
        # 그래프 선택 버튼
        self.btn_showgraph.clicked.connect(self.displayGraph)
        self.btn_showgraph_2.clicked.connect(lambda: print("그래프 버튼 2 클릭"))
        self.btn_showgraph_3.clicked.connect(lambda: print("그래프 버튼 3 클릭"))
    
        # 라디오 버튼
        self.rbtn_singleport.clicked.connect(self.singlePort)
        self.rbtn_dualport.clicked.connect(self.dualPort)
    
        self.rbtn_singledisp.clicked.connect(self.changeSingleDisp)
        self.rbtn_dualdisp.clicked.connect(self.changeDualDisp)
        self.rbtn_quaddisp.clicked.connect(self.changeQuadDisp)
    
        # 체크박스
        self.ckbox_s11.stateChanged.connect(self.ckboxS11Change)
        self.ckbox_s21.stateChanged.connect(self.ckboxS21Change)
        self.ckbox_s12.stateChanged.connect(self.ckboxS12Change)
        self.ckbox_s22.stateChanged.connect(self.ckboxS22Change)

        self.ckbox_open_1.stateChanged.connect(self.ckboxOpen1Change)

                                             
        # 콤보박스
        self.cbbox_view.currentIndexChanged.connect(self.changeViewID)
        self.cbbox_format.currentIndexChanged.connect(self.changeViewFormat)
        self.cbbox_scaleview.currentIndexChanged.connect(lambda index: print(f"Scale View 콤보박스 선택: {self.cbbox_scaleview.currentText()}"))
        self.cbbox_mkrid.currentIndexChanged.connect(lambda index: print(f"Marker ID 선택: {self.cbbox_mkrid.currentText()}"))
    
        # 다이얼
        self.dial_mkrfreq.valueChanged.connect(lambda val: print(f"Marker Frequency Dial: {val}"))
        self.dial_scale.valueChanged.connect(lambda val: print(f"Scale Dial: {val}"))
        self.dial_scaleref.valueChanged.connect(lambda val: print(f"Scale Ref Dial: {val}"))
 
    
        # 파일 저장 액션
        self.actionSave_Data_as_CSV_files.triggered.connect(lambda: print("데이터 저장 액션 실행됨"))
       
        
    def measure(self):
        self.uvna.initialize([self.startfreq,self.stopfreq],self.NoP,self.RBW,self.power)
        self.portA, self.portB =self.uvna.measure()
        self.uvna.calc_s(self.portA[2],self.portA[1],self.portA[5],self.portA[4])
        self.uvna2.calc_s(self.portB[2],self.portB[1],self.portB[5],self.portB[4])
        self.dataFrag = True
        self.displayGraph()
     
    #주파수 변경    
    def freqchanged(self, value):
        self.startfreq = value[0]
        self.stopfreq = value[1]
        self.ledit_startfreq.setText(str(self.startfreq))        
        self.ledit_stopfreq.setText(str(self.stopfreq))        

    def startfreqchanged(self):
        self.startfreq = int(self.ledit_startfreq.text())
        self.rhslider_frequency.setValue((self.startfreq, self.stopfreq))
        
    def stopfreqchanged(self):
        self.stopfreq = int(self.ledit_stopfreq.text())
        self.rhslider_frequency.setValue((self.startfreq, self.stopfreq))
    
    #파워값 변경
    def powerSliderChanged(self,value):
        self.power = value
        self.ledit_power.setText(str(self.power))  
        
    def powerLeditChanged(self):
        self.power = int(self.ledit_power.text())
        self.hslider_power.setValue(self.power)
        
    #점갯수 변경
    def NOPSliderChanged(self,value):
        self.NoP = value
        self.ledit_nopoint.setText(str(self.NoP))  
        
    def NOPLeditChanged(self):
        self.NoP = int(self.ledit_nopoint.text())
        self.hslider_nopoint.setValue(self.NoP)
        
    #RBW 변경
    def RBWSliderChanged(self,value):
        self.RBW = value
        self.ledit_rbw.setText(str(self.RBW))  
        
    def RBWLeditChanged(self):
        self.RBW = int(self.ledit_rbw.text())
        self.hslider_rbw.setValue(self.RBW)
        
        
    def show_graph(self):
        if self.dataFrag == True:
            self.graph_viewer.canvas.axes.cla()
            self.graph_viewer.canvas.figure.clear()
            self.graph_viewer.canvas.draw()
            if self.viewFormat == 0:
                self.chackNdraw_db(self.graph_viewer.canvas.figure.add_subplot(1,1,1),0)
            elif self.viewFormat == 1:
                self.chackNdraw_linear(self.graph_viewer.canvas.figure.add_subplot(1,1,1),0)
            self.graph_viewer.canvas.axes.set_xlabel('frequency(MHz)')
            self.graph_viewer.canvas.axes.set_ylabel('dB')
            self.graph_viewer.canvas.draw()  
            
        else:
            print("data are not ready")
            
    def show_graph_2(self):
    	#x_list, y_list, y_err, data_name에 대한 설정 코드 
        
        if self.dataFrag == True:
            self.graph_viewer.canvas.axes.cla()
            self.graph_viewer.canvas.figure.clear()
            self.graph_viewer.canvas.draw()       
            if self.viewFormat == 0:
                self.chackNdraw_db(self.graph_viewer.canvas.figure.add_subplot(2,1,1),0)
            elif self.viewFormat == 1:
                self.chackNdraw_linear(self.graph_viewer.canvas.figure.add_subplot(2,1,1),0)
            self.graph_viewer.canvas.axes.set_xlabel('frequency(MHz)')
            self.graph_viewer.canvas.axes.set_ylabel('dB')
            self.graph_viewer.canvas.draw() 
        
            self.chackNdraw_ang(self.graph_viewer.canvas.figure.add_subplot(2,1,2),1)
            self.graph_viewer.canvas.axes.set_xlabel('frequency(MHz)')
            self.graph_viewer.canvas.axes.set_ylabel('phase')
            self.graph_viewer.canvas.draw() 
            
        else:
            print("data are not ready")
            
    def show_graph_3(self):
    	#x_list, y_list, y_err, data_name에 대한 설정 코드 
        
        if self.dataFrag == True:
            self.graph_viewer.canvas.axes.cla()
            self.graph_viewer.canvas.figure.clear()
            self.graph_viewer.canvas.draw()
            if self.viewFormat == 0:
                self.chackNdraw_db(self.graph_viewer.canvas.figure.add_subplot(2,2,1),0)
            elif self.viewFormat == 1:
                self.chackNdraw_linear(self.graph_viewer.canvas.figure.add_subplot(2,2,1),0)
            self.graph_viewer.canvas.axes.set_xlabel('frequency(MHz)')
            self.graph_viewer.canvas.axes.set_ylabel('dB')
            self.graph_viewer.canvas.draw() 
            
            if self.viewFormat == 0:
                self.chackNdraw_db(self.graph_viewer.canvas.figure.add_subplot(2,2,2),1)
            elif self.viewFormat == 1:
                self.chackNdraw_linear(self.graph_viewer.canvas.figure.add_subplot(2,2,2),1)
            self.graph_viewer.canvas.axes.set_xlabel('frequency(MHz)')
            self.graph_viewer.canvas.axes.set_ylabel('dB')
            self.graph_viewer.canvas.draw() 
            
            self.chackNdraw_ang(self.graph_viewer.canvas.figure.add_subplot(2,2,3),2)
            self.graph_viewer.canvas.axes.set_xlabel('frequency(MHz)')
            self.graph_viewer.canvas.axes.set_ylabel('phase')
            self.graph_viewer.canvas.draw() 
            
            self.chackNdraw_ang(self.graph_viewer.canvas.figure.add_subplot(2,2,4),3)
            self.graph_viewer.canvas.axes.set_xlabel('frequency(MHz)')
            self.graph_viewer.canvas.axes.set_ylabel('phase')
            self.graph_viewer.canvas.draw() 
            
        else:
            print("data are not ready")

    def show_graph2(self):
    	#x_list, y_list, y_err, data_name에 대한 설정 코드 
        self.graph_viewer.canvas.axes.cla()
        self.graph_viewer.canvas.figure.clear()
        self.graph_viewer.canvas.draw()
        x_list = np.arange(0,10)
        y_list = np.random.rand(10)
        self.graph_viewer.canvas.axes=self.graph_viewer.canvas.figure.add_subplot(221)
        self.graph_viewer.canvas.axes.plot(x_list, y_list)
#        self.graph_viewer.canvas.axes.legend()
        self.graph_viewer.canvas.axes.set_xlabel('x')
        self.graph_viewer.canvas.axes.set_ylabel('y')
        self.graph_viewer.canvas.draw() 

        self.graph_viewer.canvas.axes=self.graph_viewer.canvas.figure.add_subplot(222)
        self.graph_viewer.canvas.axes.plot(x_list, y_list)
#        self.graph_viewer.canvas.axes.legend()
        self.graph_viewer.canvas.axes.set_xlabel('x')
        self.graph_viewer.canvas.axes.set_ylabel('y')
        self.graph_viewer.canvas.draw() 
        self.graph_viewer.canvas.axes=self.graph_viewer.canvas.figure.add_subplot(223)
        self.graph_viewer.canvas.axes.plot(x_list, y_list)
#        self.graph_viewer.canvas.axes.legend()
        self.graph_viewer.canvas.axes.set_xlabel('x')
        self.graph_viewer.canvas.axes.set_ylabel('y')
        self.graph_viewer.canvas.draw() 
        self.graph_viewer.canvas.axes=self.graph_viewer.canvas.figure.add_subplot(224)
        self.graph_viewer.canvas.axes.plot(x_list, y_list)
#        self.graph_viewer.canvas.axes.legend()
        self.graph_viewer.canvas.axes.set_xlabel('x')
        self.graph_viewer.canvas.axes.set_ylabel('y')
        self.graph_viewer.canvas.draw() 

    def show_graph3(self):
    	#x_list, y_list, y_err, data_name에 대한 설정 코드 
        self.graph_viewer.canvas.axes.cla()
        self.graph_viewer.canvas.figure.clear()
        self.graph_viewer.canvas.draw()
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        Z = X**2 + Y**2

        self.graph_viewer.canvas.axes=self.graph_viewer.canvas.figure.add_subplot(1,1,1, projection = '3d')
        self.graph_viewer.canvas.axes.plot_wireframe(X,Y,Z, color='black')
        self.graph_viewer.canvas.axes.set_xlabel('x')
        self.graph_viewer.canvas.axes.set_ylabel('y')
        self.graph_viewer.canvas.axes.set_zlabel('z')
        self.graph_viewer.canvas.draw() 
        
        
    def changeSingleDisp(self):
        self.dispmode=0
        self.cbbox_view.clear()
        self.cbbox_view.addItem('1')
        self.displayGraph()
    
    def changeDualDisp(self):
        self.dispmode=1
        self.cbbox_view.clear()
        self.cbbox_view.addItem('1')
        self.cbbox_view.addItem('2')
        self.displayGraph()
    
    def changeQuadDisp(self):
        self.dispmode=2
        self.cbbox_view.clear()
        self.cbbox_view.addItem('1')
        self.cbbox_view.addItem('2')
        self.cbbox_view.addItem('3')
        self.cbbox_view.addItem('4')
        self.displayGraph()
        
    def displayGraph(self):
        if self.dispmode == 0 :
            self.show_graph()
        elif self.dispmode ==1:
            self.show_graph_2()
        elif self.dispmode ==2:
            self.show_graph_3()
            
    def singlePort(self):
        self.port = 1
        self.displayGraph()
        
    def dualPort(self):
        self.port = 2
        self.displayGraph()
        
    def chackNdraw_linear(self,axes,flag):
        if self.s11chkFlag[flag] == 2:
            axes.plot(self.uvna.freq_vec, self.uvna.s11_abs,label = "S11")
        if self.s21chkFlag[flag] == 2:
            axes.plot(self.uvna.freq_vec, self.uvna.s21_abs,label = "S21")
        if self.port == 2:
            if self.s22chkFlag[flag] == 2:
                axes.plot(self.uvna.freq_vec, self.uvna2.s22_abs,label = "S22")
            if self.s12chkFlag[flag] == 2:
                axes.plot(self.uvna.freq_vec, self.uvna2.s12_abs,label = "S12")
        axes.legend()
        
    def chackNdraw_db(self,axes,flag):
        if self.s11chkFlag[flag] == 2:
            axes.plot(self.uvna.freq_vec, self.uvna.s11_abs_db,label = "S11")
        if self.s21chkFlag[flag] == 2:
            axes.plot(self.uvna.freq_vec, self.uvna.s21_abs_db,label = "S21")
        if self.port == 2:
            if self.s22chkFlag[flag] == 2:
                axes.plot(self.uvna.freq_vec, self.uvna2.s22_abs_db,label = "S22")
            if self.s12chkFlag[flag] == 2:
                axes.plot(self.uvna.freq_vec, self.uvna2.s12_abs_db,label = "S12")
        axes.legend()
        
    def chackNdraw_ang(self,axes,flag):
        if self.s11chkFlag[flag] == 2:
            axes.plot(self.uvna.freq_vec, self.uvna.s11_ang,label = "S11")
        if self.s21chkFlag[flag] == 2:
            axes.plot(self.uvna.freq_vec, self.uvna.s21_ang,label = "S21")
        if self.port == 2:
            if self.s22chkFlag[flag] == 2:
                axes.plot(self.uvna.freq_vec, self.uvna2.s22_ang,label = "S22")
            if self.s12chkFlag[flag] == 2:
                axes.plot(self.uvna.freq_vec, self.uvna2.s12_ang,label = "S12")
        axes.legend()
        
    def changeViewID(self,text):
        self.viewID = int(text)
        self.ckbox_s11.setCheckState(self.s11chkFlag[self.viewID])
        self.ckbox_s21.setCheckState(self.s21chkFlag[self.viewID])
        self.ckbox_s22.setCheckState(self.s22chkFlag[self.viewID])
        self.ckbox_s12.setCheckState(self.s12chkFlag[self.viewID])
        self.displayGraph()
        
    
    def ckboxS11Change(self,state):
        self.s11chkFlag[self.viewID] = state
        self.displayGraph()
        
    def ckboxS21Change(self,state):
        self.s21chkFlag[self.viewID] = state
        self.displayGraph()
        
    def ckboxS22Change(self,state):
        self.s22chkFlag[self.viewID] = state
        self.displayGraph()
        
    def ckboxS12Change(self,state):
        self.s12chkFlag[self.viewID] = state
        self.displayGraph()
        
    def changeViewFormat(self,text):
        self.viewFormat = int(text)
        self.displayGraph()
        
    def ckboxOpen1Change(self):
        QMessageBox.information(self, "Caution", "Please connect OPEN to port 1")
        self.uvna.GmOpenP1=self.uvna.measureOpenP1()
        
    def ckboxShort1Change(self):
        QMessageBox.information(self, "Caution", "Please connect SHORT to port 1")
        self.uvna.GmShortP1=self.uvna.measureShortP1()
        
    def ckboxLoad1Change(self):
        QMessageBox.information(self, "Caution", "Please connect LOAD to port 1")
        self.uvna.GmLoadtP1=self.uvna.measureLoadP1()

    def ckboxOpen2Change(self):
        QMessageBox.information(self, "Caution", "Please connect OPEN to port 2")
        self.uvna.GmOpenP2=self.uvna.measureOpenP2()
        
    def ckboxShort2Change(self):
        QMessageBox.information(self, "Caution", "Please connect SHORT to port 2")
        self.uvna.GmShortP2=self.uvna.measureShortP2()
        
    def ckboxLoad2Change(self):
        QMessageBox.information(self, "Caution", "Please connect LOAD to port 2")
        self.uvna.GmLoadtP2=self.uvna.measureLoadP2()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()  
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 15:21:27 2025

@author: kimke
"""
import numpy as np
from KUVNA import KUVNA


class KUVNA_data(KUVNA):
    def __init__(self):
        super().__init__()
        self.a1 = None
        self.b1 = None
        self.a2 = None
        self.b2 = None
        self.s11 = None
        self.s21 = None
        self.s12 = None
        self.s22 = None
        self.s11_abs = None
        self.s21_abs = None
        self.s12_abs = None
        self.s22_abs = None
        self.s11_abs_db = None
        self.s21_abs_db = None
        self.s12_abs_db = None
        self.s22_abs_db = None
        self.s11_ang = None
        self.s21_ang = None
        self.s12_ang = None
        self.s22_ang = None
        
        
    def calc_s(self,a1=None,b1=None,a2=None,b2=None):      
        self.a1 = a1
        self.b1 = b1
        self.a2 = a2
        self.b2 = b2
        
        self.s11 = np.array(b1)/np.array(a1)
        self.s21 = np.array(b2)/np.array(a1)
        self.s12 = np.array(b1)/np.array(a2)
        self.s22 = np.array(b2)/np.array(a2)
            
        self.s11_abs = np.abs(self.s11)
        self.s21_abs = np.abs(self.s21)
        self.s12_abs = np.abs(self.s12)
        self.s22_abs = np.abs(self.s22)
        
        self.s11_ang = np.angle(self.s11)
        self.s21_ang = np.angle(self.s21)
        self.s12_ang = np.angle(self.s12)
        self.s22_ang = np.angle(self.s22)
    
        self.s11_abs_db = 10*np.log10(np.abs(self.s11))
        self.s21_abs_db = 10*np.log10(np.abs(self.s21))
        self.s12_abs_db = 10*np.log10(np.abs(self.s12))
        self.s22_abs_db = 10*np.log10(np.abs(self.s22))
    
    
    
        
    

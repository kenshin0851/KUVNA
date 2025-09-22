# -*- coding: utf-8 -*-
"""
Created on Sat Aug  2 14:11:30 2025

@author: kimken
"""

import numpy as np
from vnakit_ex import getSettingsStr, loadGammaListed
from vnakit_ex.hidden import ab2G, ab2S, measure2Port, userMsg, \
                            prompt1PortMeasure,prompt2PortMeasure, \
                            getIdealSparams, get2PortResponseModel,userMsg,\
                            ab2S_SwitchCorrect,correctResponse, \
                            measure1Port,readSnP,prompt2PortSOLT,get12TermModel, \
                            correct12Term,writeSnP, get8TermModel, \
                            get8TermModelUThru, correct8Term, get1PortModel, correct1Port
import vnakit


class KUVNA:
    def __init__(self):
        self.ports = {'Tx1': 3, 'Rx1A': 2, 'Rx1B': 1, 'Tx2': 6, 'Rx2A': 5, 'Rx2B': 4}
        self.freq_vec = None
        self.settings = None


    def initialize(self,freq=[100,6000], NoP=236, Bandwidth=1, Power=-10):
        vnakit.Init()
        self.settings = vnakit.RecordingSettings(
            vnakit.FrequencyRange(freq[0], freq[1], NoP),
            Bandwidth,
            Power,
            self.ports['Tx1'],
            vnakit.VNAKIT_MODE_TWO_PORTS
        )
        vnakit.ApplySettings(self.settings)
        self.freq_vec = np.array(vnakit.GetFreqVector_MHz())
        #print setting value
        settings_str = getSettingsStr(self.settings)
        return settings_str
        

    def measure(self):
        print('Recording...', end='')
        rec_tx1, rec_tx2 = measure2Port(vnakit, self.settings, self.ports)
        print('Done.\n')
        return  rec_tx1,rec_tx2
    
    def measureOpenP1(self):
        print('Recording...',end='')
        MeasOpenP1 = measure1Port(vnakit, self.settings, self.ports['Tx1'])
        IncOpenP1 = np.array(list(MeasOpenP1[5]))
        RefOpenP1 = np.array(list(MeasOpenP1[4]))
        GmOpenP1 = RefOpenP1/IncOpenP1
        print('Done.\n')
        return GmOpenP1
    
    def measureShortP1(self):
        print('Recording...',end='')
        MeasShortP1 = measure1Port(vnakit, self.settings, self.ports['Tx1'])
        IncShortP1 = np.array(list(MeasShortP1[5]))
        RefShortP1 = np.array(list(MeasShortP1[4]))
        GmShortP1 = RefShortP1/IncShortP1
        print('Done.\n')
        return GmShortP1
    
    def measureLoadP1(self):
        print('Recording...',end='')
        MeasLoadP1 = measure1Port(vnakit, self.settings, self.ports['Tx1'])
        IncLoadP1 = np.array(list(MeasLoadP1[5]))
        RefLoadP1 = np.array(list(MeasLoadP1[4]))
        GmLoadP1 = RefLoadP1/IncLoadP1
        print('Done.\n')
        return GmLoadP1
    
    def measureOpenP2(self):
        print('Recording...',end='')
        MeasOpenP2 = measure1Port(vnakit, self.settings, self.ports['Tx2'])
        IncOpenP2 = np.array(list(MeasOpenP2[2]))
        RefOpenP2 = np.array(list(MeasOpenP2[1]))
        GmOpenP2 = RefOpenP2/IncOpenP2
        print('Done.\n')
        return GmOpenP2
    
    def measureShortP2(self):
        print('Recording...',end='')
        MeasShortP2 = measure1Port(vnakit, self.settings, self.ports['Tx2'])
        IncShortP2 = np.array(list(MeasShortP2[2]))
        RefShortP2 = np.array(list(MeasShortP2[1]))
        GmShortP2 = RefShortP2/IncShortP2
        print('Done.\n')
        return GmShortP2
    
    def measureLoadP2(self):
        print('Recording...',end='')
        MeasLoadP2 = measure1Port(vnakit, self.settings, self.ports['Tx2'])
        IncLoadP2 = np.array(list(MeasLoadP2[2]))
        RefLoadP2 = np.array(list(MeasLoadP2[1]))
        GmLoadP2 = RefLoadP2/IncLoadP2
        print('Done.\n')
        return GmLoadP2
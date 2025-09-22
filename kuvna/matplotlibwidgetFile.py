# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 12:07:35 2025

@author: Sang-Wook Kim
"""

from PyQt5.QtWidgets import*
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class matplotlibWidget(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure())

        self.vertical_layout=QVBoxLayout()
        self.vertical_layout.addWidget(self.canvas)
        self.vertical_layout.setContentsMargins(1, 1, 1, 1)
        self.canvas.axes=self.canvas.figure.add_subplot(111)
        self.setLayout(self.vertical_layout)

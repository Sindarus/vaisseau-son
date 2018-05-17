#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-17

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import (QApplication, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox,
    QPushButton, QLabel)
from PyQt5.QtGui import QPixmap

class ImageButton(QLabel):

    def __init__(self, filename):
        super().__init__()
        self.img = QPixmap(filename);
        self.setPixmap(self.img)

    def resize(self, width, height, aspect_ratio_mode = Qt.KeepAspectRatio):
        if self.img is not None:
            self.setPixmap(self.img.scaled(width, height, aspect_ratio_mode))


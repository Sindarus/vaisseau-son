#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-17

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

import sys
from PyQt5.QtCore import Qt, QRect, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtWidgets import (QApplication, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox,
    QPushButton, QLabel)
from PyQt5.QtGui import QPixmap


class ImageButtonGroup(QObject):

    def __init__(self):
        super().__init__()
        self.image_buttons = []

    def add_image_button(self, button):
        self.image_buttons.append(button)
        button.selected.connect(self.button_was_clicked)

    @pyqtSlot()
    def button_was_clicked(self):
        sender = self.sender()
        for image_button in self.image_buttons:
            if image_button != self.sender():
                image_button.unselect()

    def report(self):
        for i, button in enumerate(self.image_buttons):
            print(i+1, "th button is", "selected" if button.is_selected else "not selected")
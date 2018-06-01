#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-17

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

from PyQt5.QtCore import pyqtSignal

from ImageButton import ImageButton


class ImageOptionButton(ImageButton):
    selected = pyqtSignal()

    def __init__(self, img_path, name):
        super().__init__(img_path)
        self.name = name

        self.setCheckable(True)
        self.setAutoExclusive(True)

        self._set_style_()

    def _set_style_(self):
        self.setStyleSheet("""
            QPushButton
            {
              padding: 5px;
              border: none;
              background-color: #ff0000;
            }
            QPushButton:pressed
            {
              background-color: #cccccc;
            }
            ImageOptionButton:checked
            {
                border: 3px solid green;
            }
            """)

    def get_name(self):
        return self.name

#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-17

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
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

        self._set_style_unselected()

    def _set_style_selected(self):
        self.setStyleSheet("""
            QFrame, QLabel, QToolTip {
                border: 5px solid green;
            }
            """)

    def _set_style_unselected(self):
        self.setStyleSheet("""
            QFrame, QLabel, QToolTip {
                border: 5px solid;
            }
            """)

    def get_name(self):
        return self.name

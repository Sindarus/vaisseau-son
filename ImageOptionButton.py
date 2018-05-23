#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-17

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class ImageOptionButton(QLabel):
    selected = pyqtSignal()

    def __init__(self, filename):
        super().__init__()

        # draw picture
        self.img = QPixmap(filename)
        self.setPixmap(self.img)

        self.is_selected = False
        self._set_style_unselected()

    def resize_image(self, width, height, aspect_ratio_mode=Qt.KeepAspectRatio):
        if self.img is not None:
            self.setPixmap(self.img.scaled(width, height, aspect_ratio_mode))

    def mousePressEvent(self, event):
        self.is_selected = True
        if self.is_selected:
            self.selected.emit()
            self._set_style_selected()

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

    def unselect(self):
        self.is_selected = False
        self._set_style_unselected()

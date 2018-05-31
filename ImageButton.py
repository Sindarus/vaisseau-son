#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-23

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton


class ImageButton(QPushButton):

    def __init__(self, img_path):
        super().__init__()

        self.img_path = img_path
        self.img = QPixmap(img_path)

        icon = QIcon(self.img)
        self.setIcon(icon)

        self._set_style()

    def resize_image(self, width, height):
        self.setIconSize(QSize(width, height))

    def _set_style(self):
        self.setStyleSheet("""
            QPushButton
            {
              border: none;
            }
            QPushButton:pressed
            {
              background-color: #cccccc;
            }
            """)

    def __repr__(self):
        return "ImageButton : " + str(self.img_path)

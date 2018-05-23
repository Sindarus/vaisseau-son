#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-23

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton


class ImageButton(QPushButton):

    def __init__(self, filename):
        super().__init__()

        self.img = QPixmap(filename)

        icon = QIcon(self.img)
        self.setIcon(icon)

    def resize_image(self, width, height):
        self.setIconSize(QSize(width, height))

#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-28

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy


class CaptionedImage(QWidget):
    clicked = pyqtSignal()

    def __init__(self, text, image_path):
        super().__init__()

        self.resized = False
        self.resized_width = None
        self.resized_height = None

        self.image_label = QLabel()
        self.img = QPixmap(image_path)
        self.image_label.setPixmap(self.img)
        image_layout = QHBoxLayout()
        image_layout.addStretch(1)
        image_layout.addWidget(self.image_label)
        image_layout.addStretch(1)

        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        text_layout = QHBoxLayout()
        text_layout.addStretch(1)
        text_layout.addWidget(text_label)
        text_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(image_layout)
        layout.addLayout(text_layout)

        self.setLayout(layout)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def resize_image(self, width, height):
        self.image_label.setPixmap(self.img.scaled(width,
                                                   height,
                                                   transformMode=Qt.SmoothTransformation))
        self.resized = True
        self.resized_width = width
        self.resized_height = height

    def change_image(self, image_path):
        self.img = QPixmap(image_path)
        if self.resized:
            self.image_label.setPixmap(self.img.scaled(self.resized_width,
                                                       self.resized_height,
                                                       transformMode=Qt.SmoothTransformation))
        else:
            self.image_label.setPixmap(self.img)

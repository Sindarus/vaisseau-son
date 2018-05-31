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

    def __init__(self, text=None, image_path=None):
        super().__init__()

        self.img = None
        self.resized = False
        self.resized_width = None
        self.resized_height = None

        self.image_label = QLabel()

        image_layout = QHBoxLayout()
        image_layout.addStretch(1)
        image_layout.addWidget(self.image_label)
        image_layout.addStretch(1)

        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignCenter)
        text_layout = QHBoxLayout()
        text_layout.addStretch(1)
        text_layout.addWidget(self.text_label)
        text_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(image_layout)
        layout.addLayout(text_layout)

        self.setLayout(layout)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        if text is not None:
            self.load_caption(text)
        if image_path is not None:
            self.load_image(image_path)

    def resize_image(self, width, height):
        """If this function is called before an image was loaded, we will keep the requested size in memory for
        future images to be correctly resized"""
        if self.img is not None:
            self.image_label.setPixmap(self.img.scaled(width, height,
                                                       transformMode=Qt.SmoothTransformation))
        self.resized = True
        self.resized_width = width
        self.resized_height = height

    def load_caption(self, text):
        self.text_label.setText(text)

    def load_image(self, image_path):
        self.img = QPixmap(image_path)
        if self.resized:
            self.image_label.setPixmap(self.img.scaled(self.resized_width,
                                                       self.resized_height,
                                                       transformMode=Qt.SmoothTransformation))
        else:
            self.image_label.setPixmap(self.img)

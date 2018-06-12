#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-30

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout

from ImageButton import ImageButton


class LabeledImageButton(QWidget):
    """Widget that contains an :py:class:`ImageButton` and a label"""

    clicked = pyqtSignal()
    """This signal is emited when the :py:class:`ImageButton` is clicked"""

    def __init__(self, text, image_path):
        super().__init__()

        self.image_button = ImageButton(image_path)
        self.image_button.clicked.connect(lambda: self.clicked.emit())
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)

        image_button_layout = QHBoxLayout()
        image_button_layout.addStretch(1)
        image_button_layout.addWidget(self.image_button)
        image_button_layout.addStretch(1)

        label_layout = QHBoxLayout()
        label_layout.addStretch(1)
        label_layout.addWidget(self.label)
        label_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(image_button_layout)
        layout.addLayout(label_layout)
        self.setLayout(layout)

    def resize_image(self, *args):
        self.image_button.resize_image(*args)

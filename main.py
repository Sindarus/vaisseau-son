#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-16

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox,
    QPushButton, QLabel)

from ImageButton import ImageButton


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        #Create widgets
        title = QLabel("Atelier son", self)
        button = QPushButton("Envoyer", self)
        sounds_group = QGroupBox("Choisir un son", self)
        sound1 = ImageButton("test.jpg")
        sound1.resize(200, 200)
        sound2 = QLabel("son2", self)

        #Create Layouts
        main_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        sounds_layout = QGridLayout()

        #Setup main layout
        self.setLayout(main_layout)
        main_layout.addLayout(title_layout)
        main_layout.addWidget(sounds_group)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)

        #Setup title
        title_layout.addStretch(1)
        title_layout.addWidget(title)
        title_layout.addStretch(1)

        #Setup bank of sounds
        sounds_group.setLayout(sounds_layout)
        sounds_layout.addWidget(sound1, 0, 0, Qt.AlignCenter)
        sounds_layout.addWidget(sound2, 0, 1, Qt.AlignCenter)

        #Setup button
        button_layout.addStretch(1)
        button_layout.addWidget(button)

        #Configure window
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Borne son')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
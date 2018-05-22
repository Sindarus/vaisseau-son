#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-16

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, qApp, QShortcut,
    QVBoxLayout, QHBoxLayout, QGridLayout, QMainWindow,
    QGroupBox, QPushButton, QLabel)
from PyQt5.QtGui import QKeySequence

from ImageButton import ImageButton
from ImageButtonGroup import ImageButtonGroup
from WaveformDisplay import WaveformDisplay


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        #Create a group for sound selector buttons
        self.sound_button_group = ImageButtonGroup()

        #Create widgets
        self.central_widget = QWidget()
        title = QLabel("Atelier son", self)
        button = QPushButton("Envoyer", self)
        sounds_group = QGroupBox("Choisir un son", self)
        selected_sound_display = WaveformDisplay()
        selected_sound_display.load_audio("212764__qubodup__lion-roar.flac")

        sounds_buttons = [ImageButton("test.jpg") for i in range(8)]
        for sound_button in sounds_buttons:
            sound_button.resize_image(150, 150)
            self.sound_button_group.add_image_button(sound_button)

        #Create Layouts
        main_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        sounds_layout = QGridLayout()

        #Setup main layout
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(main_layout)
        main_layout.addLayout(title_layout)
        main_layout.addWidget(sounds_group)
        main_layout.addWidget(selected_sound_display)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)

        #Setup title
        title_layout.addStretch(1)
        title_layout.addWidget(title)
        title_layout.addStretch(1)

        #Setup bank of sounds
        sounds_group.setLayout(sounds_layout)
        positions = [(i,j) for i in range(2) for j in range(4)]
        for pos, sound_button in zip(positions, sounds_buttons):
            sounds_layout.addWidget(sound_button, pos[0], pos[1], Qt.AlignCenter)

        #Setup button
        button_layout.addStretch(1)
        button_layout.addWidget(button)

        #actions
        self.quit_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q), self)
        self.quit_shortcut.activated.connect(qApp.quit)

        #Configure window
        self.setGeometry(0, 0, 700, 700)
        self.setWindowTitle('Borne son')
        self.showFullScreen()

        button.clicked.connect(lambda : self.sound_button_group.report())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
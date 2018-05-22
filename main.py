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

from SoundChooser import SoundChooser


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        #Create widgets
        self.central_widget = QWidget()
        title = QLabel("Atelier son", self)
        button = QPushButton("Envoyer", self)
        sound_chooser = SoundChooser(self)

        #Create Layouts
        main_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        #Setup main layout
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(main_layout)
        main_layout.addLayout(title_layout)
        main_layout.addWidget(sound_chooser)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)

        #Setup title
        title_layout.addStretch(1)
        title_layout.addWidget(title)
        title_layout.addStretch(1)

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

        button.clicked.connect(lambda : sound_chooser.report())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
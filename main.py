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

from MainWidget import MainWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        fullscreen = False

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        #actions
        self.quit_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q), self)
        self.quit_shortcut.activated.connect(qApp.quit)

        #Configure window
        self.setGeometry(0, 0, 700, 700)
        self.setWindowTitle('Borne son')
        self.showFullScreen() if fullscreen else self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
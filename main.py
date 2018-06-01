#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-16

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QApplication, qApp, QShortcut, QMainWindow)

from Config import Config
from MainWidget import MainWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self._set_style()
        self.init_ui()
        self.main_widget.after_show_init()

    def init_ui(self):
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        # actions
        self.quit_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q), self)
        self.quit_shortcut.activated.connect(qApp.quit)

        # Configure window
        self.setGeometry(0, 0, Config.WINDOW_MODE_WIDTH, Config.WINDOW_MODE_HEIGHT)
        self.setWindowTitle('Borne son')
        self.showFullScreen() if Config.FULLSCREEN else self.show()

    def closeEvent(self, event):
        self.main_widget.close_child_windows()
        super().closeEvent(event)

    def _set_style(self):
        self.setStyleSheet("""
            MainWindow {
                background: """ + Config.LIGHT_LIGHT_BLUE + """;
                color: """ + Config.FONT_COLOR + """;
            }
        """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

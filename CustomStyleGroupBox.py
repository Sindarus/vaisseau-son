#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-06-01

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

from PyQt5.QtWidgets import QGroupBox

from Config import Config


class CustomStyleGroupBox(QGroupBox):

    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet("""
            QGroupBox {
                background-color: """ + Config.LIGHT_BLUE + """;
                border: 2px solid """ + Config.BORDER_BLUE + """;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 5px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                position: relative;
                left: 20px;
                padding: 2px 10px;
                background-color: """ + Config.VIVID_BLUE + """;
                border-radius: 5px;
            }
        """)

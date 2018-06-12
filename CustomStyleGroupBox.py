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
    """Groupbox that implements required style"""

    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet("""
            CustomStyleGroupBox {
                background-color: """ + Config.LIGHT_BLUE + """;
                border: 2px solid """ + Config.BORDER_BLUE + """;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 5px;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }

            CustomStyleGroupBox::title {
                subcontrol-origin: margin;
                position: relative;
                left: 20px;
                padding: 2px 10px;
                background-color: """ + Config.VIVID_BLUE + """;
                border-radius: 5px;
            }
        """)

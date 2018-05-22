#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-17

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSizePolicy, QWidget
from PyQt5.QtGui import QPixmap, QPainter


class WaveformDisplay(QLabel):

    def __init__(self):
        super().__init__()

        #This property holds whether the label will scale its contents to fill all available space.
        self.setScaledContents(True)

        #Expanding : "the widget can be shrunk and still be useful. The widget can make use of extra space,
        #             so it should get as much space as possible"
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.setStyleSheet("""
            QFrame, QLabel, QToolTip {
                border: 5px solid red;
            }
            """)

    def load_audio(self, filename):
        #the file to open should be in sounds/
        input_filename = "sounds/" + filename
        output_filename = "waveforms/" + filename + "_waveform" + ".png"
        img_size="1500x300"

        subprocess.run(["ffmpeg",
                "-y",
                "-i",
                input_filename,
                "-filter_complex",
                """[0:a]aformat=channel_layouts=mono,
                showwavespic=s="""+img_size+""":colors=#9cf42f[fg];
                color=s="""+img_size+""":color=#44582c,
                drawgrid=width=iw/10:height=ih/5:color=#9cf42f@0.1[bg];
                [bg][fg]overlay=format=rgb,drawbox=x=(iw-w)/2:y=(ih-h)/2:w=iw:h=1:color=#9cf42f""",
                "-vframes",
                "1",
                output_filename], check=True, stderr=subprocess.DEVNULL)

        #draw picture
        self.img = QPixmap(output_filename)
        self.setPixmap(self.img)

#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-17

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

import subprocess, os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSizePolicy

from Config import Config


class WaveformDisplay(QLabel):

    def __init__(self):
        super().__init__()

        # This property holds whether the label will scale its contents to fill all available space.
        self.setScaledContents(True)

        # Expanding : "the widget can be shrunk and still be useful. The widget can make use of extra space,
        #             so it should get as much space as possible"
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.setStyleSheet("""
            QFrame, QLabel, QToolTip {
                border: 5px solid red;
            }
            """)

    def load_audio(self, input_path):
        assert os.path.isfile(input_path)
        filename = input_path.split('/')[-1]  # "split" gives a list of names, [-1] returns the last one of them
        name = filename.split('.')[0]
        output_path = "waveforms/" + name + "_waveform" + ".png"
        my_stderr = subprocess.STDOUT if Config.DEBUG_FFMPEG else subprocess.DEVNULL

        # check output folder
        if not os.path.exists("waveforms/"):
            os.makedirs("waveforms/")

        subprocess.run(["ffmpeg",
                        "-y",
                        "-i",
                        input_path,
                        "-filter_complex",
                        """[0:a]aformat=channel_layouts=mono,
                        showwavespic=s=""" + Config.WAVEFORM_IMG_SIZE + """:colors=#9cf42f[fg];
                        color=s=""" + Config.WAVEFORM_IMG_SIZE + """:color=#44582c,
                        drawgrid=width=iw/10:height=ih/5:color=#9cf42f@0.1[bg];
                        [bg][fg]overlay=format=rgb,drawbox=x=(iw-w)/2:y=(ih-h)/2:w=iw:h=1:color=#9cf42f""",
                        "-vframes",
                        "1",
                        output_path], check=True, stderr=my_stderr)

        # draw picture
        self.img = QPixmap(output_path)
        self.setPixmap(self.img)

    def reset(self):
        self.img = None
        self.clear()

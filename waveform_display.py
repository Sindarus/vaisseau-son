#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-17

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""

import os
import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QSizePolicy

from config import Config


class WaveformDisplay(QLabel):
    """Widget to display a sound as a waveform"""

    def __init__(self):
        super().__init__()
        self._set_style()

        # This property holds whether the label will scale its contents to fill all available space.
        #  By setting to *True*, the contents will get scaled to always match the size of the :py:class:`QLabel`
        self.setScaledContents(True)

        # Expanding : "the widget can be shrunk and still be useful. The widget can make use of extra space,
        #             so it should get as much space as possible"
        # By setting the horizontal size policy to *Expanding*, the widget will automatically take as much width as it
        # can, and it will shrink down if the window gets thinner
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)

        self.setMinimumWidth(1)  # Allows this widget to shrink below pixmap's width
        self.setFixedHeight(Config.WAVEFORM_DISPLAY_HEIGHT)  # This widget will always have the same height

        self.setAlignment(Qt.AlignCenter)
        self.load_placeholder_text()

    def load_placeholder_text(self):
        """Load a placeholder text to be displayed instead of a waveform"""
        self.setText(Config.WAVEFORM_DISPLAY_PLACEHOLDER_MSG)

    def load_audio(self, input_path):
        """Load an audio recording for display.

        This function handles calling the external program *ffmpeg* with a set of arguments to produce a picture of
        the waveform."""
        assert os.path.isfile(input_path)
        filename = input_path.split('/')[-1]  # "split" gives a list of names, [-1] returns the last one of them
        name = filename.split('.')[0]  # retrieves name without file extension
        output_path = "waveforms/" + name + "_waveform" + ".png"
        my_stderr = subprocess.STDOUT if Config.DEBUG_FFMPEG else subprocess.DEVNULL

        # check output folder
        if not os.path.exists("waveforms/"):
            os.makedirs("waveforms/")

        subprocess.run(["ffmpeg", "-y", "-i", input_path, "-filter_complex",
                        "[0:a]aformat=\
                            channel_layouts=mono,\
                        showwavespic=\
                            s=" + Config.WAVEFORM_IMG_SIZE + ":\
                            colors=" + Config.BLUE + "[fg],\
                        color=\
                            s=" + Config.WAVEFORM_IMG_SIZE + ":\
                            color=" + Config.LIGHT_BLUE + ",\
                        drawgrid=\
                            width=iw/10:\
                            height=ih/5:\
                            color=" + Config.BLUE + "@" + Config.WAVEFORM_DISPLAY_GRID_OPACITY + "[bg],\
                        [bg][fg]overlay=\
                            format=rgb,\
                        drawbox=\
                            x=(iw-w)/2:\
                            y=(ih-h)/2:\
                            w=iw:\
                            h=1:\
                            color=" + Config.BLUE,
                        "-vframes", "1", output_path], check=True, stderr=my_stderr)
        # Explanations about the options :
        # https://stackoverflow.com/questions/32254818/generating-a-waveform-using-ffmpeg#32276471

        # draw picture
        self.img = QPixmap(output_path)
        self.setPixmap(self.img)

    def reset(self):
        """Clear the display and load placeholder"""
        self.img = None
        self.clear()
        self.load_placeholder_text()

    def _set_style(self):
        self.setStyleSheet("""
            WaveformDisplay
            {
                border: 2px solid """ + Config.BORDER_BLUE + """;
                background-color: """ + Config.LIGHT_BLUE + """;
                font-size: 16px;
            }
        """)

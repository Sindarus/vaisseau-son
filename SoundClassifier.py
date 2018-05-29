#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-29

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""

from threading import Thread
import time

from Config import Config

class SoundClassifier(Thread):

    def __init__(self, user_sound_path, callback_func):
        super().__init__()
        self.user_sound_path = user_sound_path
        self.callback_func = callback_func

    def run(self):
        time.sleep(1)
        #TODO: do some real calculation
        results = [("lion", 85), ("police", 20), ("cow", 5), ("wind", 3)]
        self.callback_func(results)

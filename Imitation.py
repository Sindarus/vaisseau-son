#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-07-05

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""
import os
from shutil import copyfile

from AudioPlayer import AudioPlayer
from Config import Config


class Imitation:

    def __init__(self, temp_path, label, datetime):
        self.temp_path = temp_path
        self.label = label
        self.dt = datetime

    def save(self, db, submitted):
        """Save the imitation to its final location, and saves its info in database.

        Save the sound file at the right location according to the specifications of the final directory tree, and
        save its informations to the database, still according to specs.

        :param db: connection object from the _mysql module
        :param bool submitted: whether the currently recorded sound was submitted."""

        self.duration = AudioPlayer.get_wav_duration(self.temp_path)

        # preparing paths
        final_dir = str(self.dt.year) + "/" \
                    + str(self.dt.year) + "-" + "%.2d" % self.dt.month + "/" \
                    + str(self.dt.year) + "-" + "%.2d" % self.dt.month + "-" + "%.2d" % self.dt.day
        final_path = final_dir + "/" + str(int(self.dt.timestamp())) + ".wav"
        final_dir_with_root_dir = Config.FINAL_SOUNDS_DIR + final_dir
        final_path_with_root_dir = Config.FINAL_SOUNDS_DIR + final_path

        # Copying file to final destination folder
        # This could be done with a single one-line string formatting, but the sake of readability I did not do that.
        if not os.path.isdir(final_dir_with_root_dir):
            #  makedirs creates all intermediate-level directories needed to contain the leaf directory,
            # while os.mkdir does not.
            os.makedirs(final_dir_with_root_dir)
        copyfile(self.temp_path, final_path_with_root_dir)

        # Adding sound info in database
        try:
            db.add_sound(final_path, self.label, submitted, self.dt, self.duration)
        except Exception as e:
            print("Could not add sound info to database. Cancelling changes.")
            os.remove(final_path_with_root_dir)
            raise e

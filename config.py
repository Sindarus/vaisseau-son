#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-23

Reference for style conventions : https://www.python.org/dev/peps/pep-0008/#naming-conventions
"""


class Config:
    FULLSCREEN = False
    SOUNDS = {
        "lion":     {'sound_path': "sounds/232289__zglar__zombie-or-monster-or-lion-roar.wav",
                     'image_path': "images/lion.png"},
        "cow":      {'sound_path': "sounds/58277__benboncan__cow.wav",
                     'image_path': "images/cow.png"},
        "police":   {'sound_path': "sounds/90014__thfc140491__police-siren-perpignan_cropped.wav",
                     'image_path': "images/police.png"},
        "wind":     {'sound_path': "sounds/84111__benboncan__wind-on-door-short_cropped.wav",
                     'image_path': "images/wind.png"}
    }
    TITLE = "Atelier son"
    VALIDATE_BUTTON = "Envoyer"
    WAVEFORM_IMG_SIZE = "1500x200"
    DEBUG_FFMPEG = False
    SOUND_IMAGE_SIZE = 150
    PLAYBACK_BUTTON_ICON_SIZE = 100
    SOUND_IMAGES_COLUMNS = 4
    SOUND_IMAGES_ROWS = 1

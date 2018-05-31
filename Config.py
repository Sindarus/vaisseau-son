#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-25

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""


class Config:
    SOUNDS = {
        "lion": {'sound_path': "sounds/232289__zglar__zombie-or-monster-or-lion-roar.wav",
                 'image_path': "images/lion.png",
                 'display_name': "un rugissement"},
        "cow": {'sound_path': "sounds/58277__benboncan__cow.wav",
                'image_path': "images/cow.png",
                'display_name': "un beuglement"},
        "police": {'sound_path': "sounds/90014__thfc140491__police-siren-perpignan_cropped.wav",
                   'image_path': "images/police.png",
                   'display_name': "un sifflement de vent"},
        "wind": {'sound_path': "sounds/84111__benboncan__wind-on-door-short_cropped.wav",
                 'image_path': "images/wind.png",
                 'display_name': "un sifflement de vent"}
    }
    DEBUG_FFMPEG = False

    # UI
    FULLSCREEN = False
    SOUND_IMAGE_SIZE = 150
    PLAYBACK_BUTTON_ICON_SIZE = 100
    SOUND_IMAGES_COLUMNS = 4
    SOUND_IMAGES_ROWS = 1
    MAIN_RESULT_IMAGE_SIZE = 400
    EXTRA_RESULT_IMAGE_SIZE = 150
    NAV_ICON_SIZE = 75
    NOTIFICATION_MESSAGES_TIMEOUT = 5000  # in msec
    # Waveform
    WAVEFORM_IMG_SIZE = "2000x250"
    WAVEFORM_DISPLAY_HEIGHT = 250
    WAVEFORM_DISPLAY_WAVE_COLOR = "9cf42f"
    WAVEFORM_DISPLAY_BG_COLOR = "44582c"
    WAVEFORM_DISPLAY_GRID_OPACITY = "0.1"

    # Text
    TITLE = "Atelier son"
    VALIDATE_BUTTON = "Envoyer"
    LOADING_TEXT = "L'IA analyse votre son, merci de patienter :)"
    CANCEL_IA_TEXT = "Annuler"
    RESULTS_GROUP_TEXT = "Résultats"
    BACK_ARROW_TEXT = "Retour"
    RELOAD_ICON_TEXT = "Tout recommencer"
    RESULT_ITEM_TEXT = "L'IA a reconnu %s avec une certitude de %i%%"
    EXTRA_RESULT_ITEM_TEXT = "%i%%"
    REC_TOO_SHORT_TOOLTIP_MSG = "Maintenez enfoncé pour enregistrer"

    # Audio
    N_CHANNELS = 1
    SAMPLE_SIZE = 32  # in bits
    SAMPLE_RATE = 44100  # in hertz
    TOO_SHORT_THRESHOLD = 0.5  # minimum duration of a user recording. If shorter, it will not be taken into account

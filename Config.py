#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Clément Saintier
Creation date: 2018-05-25

Reference for style conventions : https://www.python.org/dev/peps/pep-0008
"""


class Config:
    """Class that contains all configuration options"""

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
    """Sounds that the user shall try to imitate. To add new sounds, you should respect the preexisting syntax,
    add the sound files and images files to the *sounds/* and *images/* folder, and change
    :py:attr:`SOUND_IMAGES_COLUMNS` and :py:attr:`SOUND_IMAGES_ROWS` accordingly"""

    DEBUG_FFMPEG = False
    """If set to one, the ffmpeg output will be printed on stdout. The ffmpeg programm is used to generate waveform
    pictures from a sound file. """

    # UI
    FULLSCREEN = False
    """If set to true, the app will be launched in fullscreen mode"""
    WINDOW_MODE_WIDTH = 1000
    """Window's default width when :py:attr:`FULLSCREEN` is disabled"""
    WINDOW_MODE_HEIGHT = 1020
    """Window's default height when :py:attr:`FULLSCREEN` is disabled"""
    SOUND_IMAGE_SIZE = 150
    """Size of the sound buttons (in :py:class:`SoundChooser`). These buttons are squared, that's why there's only
    one dimension size to set """
    PLAYBACK_BUTTON_ICON_SIZE = 100
    """Size of the play and record buttons implemented in the class :py:class:`AudioPlayer`"""
    SOUND_IMAGES_COLUMNS = 4
    """Number of columns in the grid display for sound buttons"""
    SOUND_IMAGES_ROWS = 1
    """Number of rows in the grid display of sound buttons"""
    MAIN_RESULT_IMAGE_SIZE = 400
    """Size of the picture of the first ranking result on the :py:class:`ResultsWindow`"""
    EXTRA_RESULT_IMAGE_SIZE = 150
    """Size of the pictures of the following results on the :py:class:`ResultsWindow`"""
    NAV_ICON_SIZE = 75
    """Size of the picture of the buttons that are used to navigate, such as the "reload" button or the "process"
    button"""
    LITTLE_NAV_ICON_SIZE = 50
    """Alternative size for small navigation buttons"""
    NOTIFICATION_MESSAGES_TIMEOUT = 5000  # in msec
    """Time after which a message is removed from the notification zone on the :py:class:`MainWidget`"""
    IMAGE_BUTTON_HOLD_BORDER_WIDTH = 4
    """width of the border that is displayed around an :py:class:`ImageButton` when it is being pressed down."""
    AUDIO_RECORD_TIMOUT = 10000  # in msec
    """Maximum duration of a user recording. After this time, the recording will be automatically interrupted."""
    DISABLE_ANALYSING_SOUNDS = False
    """Disable sending sounds to AI when the user clicks the _send_ button. Sounds are still saved in database as
    _submitted_. """

    # Waveform
    WAVEFORM_IMG_SIZE = "1500x270"
    """Size of the images that ffmpeg produces. The image is being scaled by :py:class:`WaveformDisplay` afterwards
    anyway, but higher values can produce better quality render """
    WAVEFORM_DISPLAY_HEIGHT = 270
    """Vertical size of a :py:class:`WaveformDisplay`"""
    WAVEFORM_DISPLAY_WAVE_COLOR = "3232c8"
    """Color of the waveform of a :py:class:`WaveformDisplay`"""
    WAVEFORM_DISPLAY_BG_COLOR = "b3d0fc"
    """Color of the background of a :py:class:`WaveformDisplay`"""
    WAVEFORM_DISPLAY_GRID_OPACITY = "0.4"
    """Opacity of the grid of a :py:class:`WaveformDisplay`"""
    # Colors
    LIGHT_LIGHT_BLUE = "#dae8fc"
    LIGHT_BLUE = "#b3d0fc"
    BLUE = "#3232c8"
    BORDER_BLUE = "#6c8ebf"
    VIVID_BLUE = "#008cff"
    FONT_COLOR = "#4d4d4d"

    # Text
    TITLE = "Atelier son"
    """Text displayed on top of the main window"""
    VALIDATE_BUTTON = "Envoyer"
    """Label of the button to launch classifying process"""
    LOADING_TEXT = "L'IA analyse votre son, merci de patienter :)"
    """Text displayed while the classifying process is running"""
    CANCEL_IA_TEXT = "Annuler"
    """Label of the button to cancel the classifying process"""
    RESULTS_GROUP_TEXT = "Résultats"
    """Name of the results section"""
    BACK_ARROW_TEXT = "Retour"
    """Label of the button to go back to the main window from the results window"""
    RELOAD_ICON_TEXT = "Tout recommencer"
    """Label of the button to reset the app"""
    RESULT_ITEM_TEXT = "L'IA a reconnu %s\navec une certitude de %i%%"
    """Caption of the image associated with the main result. The first argument is the display name of the sound,
    second argument is the confidence of the classifier as a percent."""
    EXTRA_RESULT_ITEM_TEXT = "%i%%"
    """Caption of the image associated with a secondary result. The first argument is the confidence of the
    classifier. """
    WAVEFORM_DISPLAY_PLACEHOLDER_MSG = "Votre extrait sonore apparaitra ici après enregistrement"
    """Placeholder message to display on a :py:class:`WaveformDisplay` when the user hasn't recorded a sound yet."""
    CURRENTLY_RECORDING_MSG = "Enregistrement en cour !"
    """Notification message to display while a recording is running"""

    # Audio
    N_CHANNELS = 1
    SAMPLE_SIZE = 32  # in bits
    SAMPLE_RATE = 44100  # in hertz
    TOO_SHORT_THRESHOLD = 0.5  # minimum duration of a user recording. If shorter, it will not be taken into account

    # Saving sounds to DB
    SAVE_TO_DB = True
    """Enable saving sounds to specific folder and sound info to database"""
    FINAL_SOUNDS_DIR = "sound_storage/"
    """Root directory where to store sound files as specified in the """
    DB_ADDR = "localhost"
    """Address of the DBMS (Database Management System)"""
    SOUND_DB_NAME = "user_sounds"
    """Name of the sound database"""
    DB_USER = "vaisseau_son"
    """User under which this programm will identify to the DBMS"""
    DB_PASSWD_GET_METHOD = "envvar"
    """Mothod to get the database password

    Set to "envvar" to get password from a environment variable
    Set to "config" to get password from the :py:attr:`DB_PASSWD` config variable (not recommended!)
    """
    DB_PASSWD_ENV_VAR_NAME = "VAISSEAU_SON_DB_PASSWD"
    """Name of the environment variable which contains the password of :py:attr:`DB_USER`"""
    DB_PASSWD = ""
    """Database password (not recommended!).

    You can specify the database password here, but it not recommanded, since the password will be visible by anyone with
    access to this file. This method is however provided for testing environments."""
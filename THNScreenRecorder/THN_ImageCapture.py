#!/usr/bin/python3
"""This module captures the screen and saves the files to a cache folder."""

import time

import mss
import mss.tools
import numpy as np

from PySide6.QtCore import QObject

from THNScreenRecorder.THN_PySideSignals import PySideSignals
from THNScreenRecorder.THN_FileManagement import (LOCAL_CACHE, CACHE_FORMAT,
                                                  LOGGER, create_folder)


class ImageCapture(QObject):
    """Starts capturing the user's screen and saves the frames to disk.

    The coordinates of the screen covered by the main UI are used to grab 
    images of the users screen and save the information in temp numpy arrays 
    which are output to temporary .npy files to be converted once the 
    capturing is complete.

    Args:
        width: Integer for the width of the UI window.
        height: Integer for the height of the UI window.
        widget_pos: Tuple for the (x, y) coordinates of the UI window using the 
            upper left corner.
        clip_name: String for the name of the clip being recorded, input by the
            user. 
    """

    # **************************************************************************
    # Init
    def __init__(self, width, height, widget_pos, clip_name, fps):
        """Inits ImageCapture with class attributes."""

        super().__init__()

        # User signals class to manage outgoing Signals.
        self.signals = PySideSignals()

        # Set folder for frames based on user name input.
        self.cache = f'{LOCAL_CACHE}\\{clip_name}'

        # Default 
        self.capturing = False
        self.capturing_paused = False
        self.frame_width = width
        self.frame_height = height
        self.widget_position = widget_pos
        self.fps = fps

    # **************************************************************************
    # Funtions
    def run(self):
        """This method is triggered once the QThread is started."""

        LOGGER.info('Image capture initiated')
        self.capturing = True
        self.capture_screen()

    def update_position(self, new_position):
        LOGGER.info('Updating window position')
        self.frame_width = new_position[0]
        self.frame_height = new_position[1]
        self.widget_position = new_position[2]
        log_txt = (f'New window dimentions: {self.frame_width},'
                   f'{self.frame_height}, {self.widget_position}')
        LOGGER.info(log_txt)

    def cancel_capture(self):
        """If user cancels the process emit Signals to UI to stop QThread."""

        if self.capturing:
            LOGGER.warning('Canceling capture sent from app exit')
            self.capturing = False
            self.signals.canceled.emit()
        self.signals.finished.emit()

    def stop_capture(self):
        """Once the process is stopped emit Signals to UI to stop QThread.

        When capture process is stopped the cache file is emitted back to the
        main UI to be used to collect recorded files.
        """

        LOGGER.info('Capture stopped')
        self.capturing = False
        self.signals.captured_frames.emit(self.cache)
        self.signals.finished.emit()

    def capture_screen(self):
        """Creates cache folder and saves .npy files of captured screen.

        Each captured frame is saved as a numpy binary file so that images are
        not stored in memory but read and converted to image files once the 
        capturing is complete.

        Returns:
            False if there are errors defining the output path.
        """

        self.prev = 0
        num = 0

        cache_folder = create_folder(self.cache)
        if not cache_folder:
            LOGGER.error('Error creating cache folder')
            return

        while self.capturing:
            if self.capturing_paused:
                continue
            time_elapsed = time.time() - self.prev

            if time_elapsed > 1. / self.fps:
                self.prev = time.time()
                frame = self.screen_grab_mss(self.frame_width, self.frame_height,
                                             self.widget_position)
                np.save(f'{self.cache}\\frame_{num:04}{CACHE_FORMAT}', frame)
                num += 1

        LOGGER.info('Capturing screen finished')

    def screen_grab_mss(self, w, h, pos):
        """Grabs area of the screen to be saved to image sequence.

        Using the variables defined when the class is executed on the QThread,
        the specific area of the screen is saved. The mss module is used for 
        this over PIL as it's much faster.

        Returns:
            mss.screenshot.ScreenShot object to be saved as numpy binary file.
        """

        left = pos.x()
        upper = pos.y()
        right = w
        lower = h
        with mss.mss() as sct:
            monitor = {"top": upper, "left": left, "width": right, "height": lower}
            sct_img = sct.grab(monitor)
            return sct_img

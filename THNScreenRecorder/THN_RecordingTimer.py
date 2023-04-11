#!/usr/bin/python3
"""This module is the timer used to monitor the duration of recordings."""

from PySide6.QtCore import QObject, QTimer

from THNScreenRecorder.THN_PySideSignals import PySideSignals
from THNScreenRecorder.THN_FileManagement import LOGGER


class RecordingTimer(QObject):
    """Starts a QTimer object to keep track of recording duration.

    This class is used as a worker object which is run on a QThread from the 
    main UI class.
    """

    # **************************************************************************
    # Init
    def __init__(self):
        """Inits RecordingTimer with class attributes."""

        super().__init__()

        # User signals class to manage outgoing Signals.
        self.signals = PySideSignals()

        # Qtimer object and resetting class variables.
        self.timer = QTimer(self)
        self.timer_paused = False
        self.timer_running = False
        self.counter = 0

    # **************************************************************************
    # Funtions
    def run(self):
        """This method is triggered once the QThread is started."""

        LOGGER.info('Starting timer')
        # Connect timeout Signal to 'begin_timer' method.
        self.timer.timeout.connect(self.begin_timer)

        # Start timer with 100 ms accuracy.
        self.timer.start(100)
        self.timer_running = True
        self.begin_timer()

    def begin_timer(self):
        """Starts QTimer object and emits the current duration to main UI."""

        if self.timer_running:
            if not self.timer_paused:
                self.counter += 1
                time_output = self.stopwatch(self.counter)
                self.signals.record_duration.emit(str(time_output))
        else:
            self.end_timer()

    def end_timer(self):
        """Stops QTimer object and emits 'finished' Signal to main UI"""

        self.timer_running = False
        self.timer.stop()
        self.signals.finished.emit()

    def stopwatch(self, count):
        """Formats current Qtimer time to correct format to display on UI.

        Args:
            count: Integer for the current count in ms.

        Returns:
            String of the current time in the format MM:SS.
        """

        self.time_now = count//10
        self.seconds = self.time_now % 60
        self.minutes = self.time_now//60

        if self.seconds < 10:
            self.seconds = f'0{self.seconds}'

        if int(self.minutes) > 1:
            self.signals.stop_capture.emit()

        text = f'0{self.minutes}:{self.seconds}'
        return text

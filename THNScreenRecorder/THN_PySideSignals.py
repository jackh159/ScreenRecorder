#!/usr/bin/python3
"""This module stores all the PySide Signals used by each class."""

from PySide6.QtCore import QObject, Signal


class PySideSignals(QObject):
    """Class to store all PyQt Signals which are used by other classes."""

    finished = Signal()
    canceled = Signal()
    stop_capture = Signal()
    progress = Signal(float)
    record_duration = Signal(str)
    captured_frames = Signal(str)

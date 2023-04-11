#!/usr/bin/python3
"""This is a custom QWidget created for the THN Screen Recorder.

This script contains two classes, the first is the base CircularProgressBar 
widget which is used to create the progress bar line using QPainter and QPen. 
It contains all the default settings and the necessary methods to update itself 
visually.
The second class is ProgressBar to be imported in to the Screen Recorder, it's 
created using a QMainWindow and holds the base CircularProgressBar class as 
well as extra QLabels and text for the application use case.
"""

import sys

from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QFrame,
                               QVBoxLayout, QGraphicsDropShadowEffect, QLabel)


class CircularProgressBar(QWidget):
    """Base class for the circular progress bar."""

    def __init__(self, parent=None):
        """Inits CircularProgressBar with class attributes."""

        super().__init__(parent)

        self.main_ui = parent

        # Window size
        self.width = 200
        self.height = 200

        # Progress bar.
        self.value = 0
        self.max_value = 100
        self.progress_width = 10
        self.progress_rounded_cap = False

        # Text settings.
        self.font_family = 'Segoe UI'
        self.font_size = 20
        self.suffix = '%'

        # UI colours.
        self.rgb_colour = (80, 150, 220)
        self.rgb_bg_colour = (120, 120, 120)  # Not currently used.

        self.set_window_size(self.width, self.height)

    def set_window_size(self, width, height):
        """Changes the width and height of the widget."""

        self.resize(width, height)

    def add_shadow(self):
        """Adds a drop shadow effect to the progress bar.

        This method is currently not being used as it's very expensive and 
        causes the main UI to hang when using QThreadPool / QRunnable classes. 
        """

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)

    def get_qcolour(self, rgb_value):
        """Returns a QColor object from an RGB tuple."""

        return QColor(rgb_value[0], rgb_value[1], rgb_value[2])

    def set_value(self, value):
        """Sets the value of the progress bar.

        Once the repaint method is called it will trigger the paintEvent to 
        redraw the progress bar line.
        
        Args:
            value: Integer for the value to apply to progress bar.
        """

        self.value = value
        self.repaint()        

    def paintEvent(self, event):
        """Built in Qwidget method which is sent to widgets that need updating.

        The progress bar itself is created using a QPen to draw a line of the
        QPainter object using the settings from __init__
        """

        width = self.width - self.progress_width
        height = self.height - self.progress_width
        margin = self.progress_width / 2
        value = self.value * 360 / self.max_value

        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing)
        paint.setFont(QFont(self.font_family, self.font_size))

        rect = QRect(0, 0, self.width, self.height)
        paint.setPen(Qt.NoPen)
        paint.drawRect(rect)

        pen = QPen()
        pen.setColor(self.get_qcolour(self.rgb_colour))
        pen.setWidth(self.progress_width)

        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)

        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90 * 16, -value * 16)

        pen.setColor(self.get_qcolour(self.rgb_colour))
        paint.setPen(pen)
        paint.drawText(rect, Qt.AlignCenter, f'{self.value}{self.suffix}')


class ProgressBar(QMainWindow):
    """Custom progress bar to be imported in to the main application.

    This class takes the base CircularProgressBar class and applys the default
    settings for the screen recorder. A status label is also added to indicate
    to the user the current task.
    """

    def __init__(self, parent=None):
        """Inits CircularProgressBar with class attributes."""

        super().__init__(parent)

        self.main_ui = parent
        self.resize(300, 300)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.container = QFrame()
        self.container.setStyleSheet('background-color: transparent')
        self.layout = QVBoxLayout()
        self.progress = CircularProgressBar()
        self.progress.value = 0
        # self.progress.add_shadow()  # Causes the UI to hang :(
        self.progress.setMinimumSize(self.progress.width, self.progress.height)
        self.layout.addWidget(self.progress, Qt.AlignCenter, Qt.AlignCenter)
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        self.create_status_label()

    def create_status_label(self):
        """Creates and adds a QLabel to the UI"""

        self.label = QLabel(self)
        self.label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label.setText('Processing Images...')
        self.label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.label.setFont(
            QFont(self.progress.font_family, self.progress.font_size))
        style_sheet = f'color: rgb{self.progress.rgb_colour}; \n'
        self.label.setStyleSheet(style_sheet)
        self.layout.addWidget(self.label, Qt.AlignCenter, Qt.AlignCenter)

    def change_value(self, value):
        """Updates the percentage of the progress bar.
    
        Args:
            value: Integer for the new percentage to be applied.
        """
        self.progress.set_value(value)


def open_window():
    # Creates the QMainWindow to check the properties before importing.
    app = QApplication(sys.argv)
    window = ProgressBar()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # Used for testing outside of the main tool.
    open_window()

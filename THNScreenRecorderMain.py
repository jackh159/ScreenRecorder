#!/usr/bin/python3
"""This is the THN Screen Recorder script that launches the tool.

This tool is used to create screen recordings of assets and environment for 
morning reviews. Recordings are saved as a tiff image sequence in the 
'ReviewData' folder for the following day. The default location for the 
'ReviewData' folder is L:/ReviewData.

Typical usage:

    Set the verbosity of the logger using the 'level_input' parameter with
    set_console_logger() function when the tool is launched.

    Start the program using open_window() to open the main UI.
"""

__version__ = '2.7.3'
__author__ = 'Jack Hunter'

import os
import sys
import time
import ctypes
import string
import logging

import psutil
from hurry.filesize import size

from PIL import Image, ImageFont, ImageDraw
from PySide6.QtGui import QColor, Qt, QIcon, QFontDatabase
from PySide6.QtCore import QCoreApplication, QThread, QPoint, QSize
from PySide6.QtWidgets import (QApplication, QGraphicsOpacityEffect, QSizeGrip,
                               QMainWindow)

from THNScreenRecorderUI import Ui_MainWindow
from THNScreenRecorder import (PySideSignals, RecordingTimer, ImageCapture,
                               ProgressBar, ImageProcessor, SETTINGS_FILE,
                               CONFIG, LOGGER, write_image, create_folder,
                               get_next_workday, get_config_values,
                               save_config_file, clean_cache_folder,
                               collect_files)

USERNAME = str(os.getlogin())
TOOL_NAME = 'thn_screenrecorder2.0'
FRAME_RATE = 15
IMAGE_FORMAT = '.tiff'
CACHE_FORMAT = '.npy'
LEGAL_TXT_CHARACTERS = ' _-0123456789'

# File path variables.
TOOL_PATH = sys.argv[0]  # returns location of where the script is run from
SLATE_BG = f'{os.path.dirname(TOOL_PATH)}\\reviewSlateBack.tif'
SLATE_SWATCHES = f'{os.path.dirname(TOOL_PATH)}\\reviewSlateSideSwatches.tga'
LOGGER.setLevel(logging.NOTSET)


# Integers to be used for ctypes message prompts in message_box() funtion.
MB_OK = 0
MB_OKCANCEL = 1
MB_YESNOCANCEL = 3
MB_YESNO = 4
IDOK = 1
IDCANCEL = 2
IDABORT = 3
IDYES = 6
IDNO = 7


def launch_checks(output_folder):
    """Set of checks which need to be passed before tool can launch.

    Args:
        output_folder: String for the desired output folder for recordings.

    Returns:
        String for the output folder which will store the user recordings.
        False if checks are failed.
    """

    if not os.path.exists(output_folder):
        local_folder_path = 'C:\\ReviewData'
        message_box_title = 'Folder Not Found'
        txt = (f'Output folder {output_folder} Cannot be found.\n'
               f'Use {local_folder_path} instead?')
        LOGGER.warning(txt)
        result = message_box(txt, message_box_title, MB_YESNO)
        response = f'Response = {result}'
        LOGGER.info(response)
        if result == IDNO:
            return False

        output_folder = local_folder_path
        if not os.path.exists(output_folder):
            create_folder(output_folder)

    # Check for overlay files.
    slate_check = file_checker(SLATE_BG)
    if not slate_check:
        return False
    swatches_check = file_checker(SLATE_SWATCHES)
    if not swatches_check:
        return False

    return output_folder


def file_checker(file_path):
    """Checks if required file can be found and informs the user.

    Args:
        file_path: String representing the path of the file.

    Returns:
        True if user wishes to launch tool without files, False if otherwise.
    """

    warning_title = 'File Not Found'
    if not os.path.exists(file_path):
        file_name = os.path.basename(file_path)
        log_warning = f'{file_name} not found'
        LOGGER.warning(log_warning)
        txt = f'{file_name} cannot be found, launch anyway?'
        result = message_box(txt, warning_title, MB_YESNO)
        if result == IDNO:
            return False
    return True


def message_box(message, title, prompt_type=4):
    """Informs the user of information and prompts for a response if needed.

    Args:
        message: String for the message to be displayed to the user.
        title: String for the title of the message box.
        prompt_type: Integer for the type of prompt displayed.

    Returns:
        Displays message box window to the user. 
        True if user selects 'Yes' or 'OK', False if otherwise.
    """

    return ctypes.windll.user32.MessageBoxW(0, message, title, prompt_type)


def save_version_file():
    """Saves current version of tool to file."""

    script_folder = os.path.dirname(TOOL_PATH)
    log_txt = f'Tool is launching from {script_folder}'
    LOGGER.info(log_txt)
    output_path = f'{script_folder}\\CurrentVersion.ini'
    section_name = TOOL_NAME
    current_version = {'version': __version__}
    save_config_file(section_name, current_version, output_path)


def set_console_logger(level_input=0):
    """Sets desired verbosity of console loggging output.

    Args:
        level_input: Integer for verbosity level. Levels are as follows;
        notset=0, debug=10, info=20, warning=30, error=40, critical=50
    """

    console_log = logging.StreamHandler()
    console_log.setLevel(level=level_input)
    console_handler_format = '%(asctime)s | %(levelname)s: %(message)s'
    console_log.setFormatter(logging.Formatter(console_handler_format))

    LOGGER.addHandler(console_log)


def enable_output_logger(level_input=0):
    """Sets desired verbosity of loggging output file.

    The log file will be saved to the library, if the network cannot be reached
    the logging directory will be on the local C:/ drive.

    Args:
        level_input: Integer for verbosity level. Levels are as follows;
        notset=0, debug=10, info=20, warning=30, error=40, critical=50
    """

    log_path = 'L:\\Library\\_tools\\logs'
    if not os.path.exists(log_path):
        log_path = 'C:\\logs'

        if not os.path.exists(log_path):
            create_folder(log_path)

    log_name = f'{USERNAME}_{TOOL_NAME}'
    output_file = f'{log_path}\\{log_name}.log'

    log_output = logging.FileHandler(output_file)
    log_output.setLevel(level=level_input)
    handler_format = ('%(asctime)s | %(levelname)s | '
                      '%(funcName)s | %(lineno)d: %(message)s')
    log_output.setFormatter(logging.Formatter(handler_format))

    LOGGER.addHandler(log_output)


# ******************************************************************************
# Classes
class ScreenRecorderUI(QMainWindow):
    """Opens the main UI for the Screen Recorder.

    Typical usage:
        The main UI also indicates the area of the screen which will be 
        captured so each corner of window can be adjusted to increase or 
        decrease the total recording size. The name of video clip as well as 
        the current working project is set by the user via text inputs.

    Args:
        review_folder: String indicating the folder path to be used to save any
            captured image files.
    """

    def __init__(self, review_folder):
        """Inits ScreenRecorderUI with class attributes."""

        super().__init__()

        self.signals = PySideSignals()

        # Setup UI.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f'THN Screen Recorder {__version__}')

        self.review_folder = review_folder
        self.project_list = self.ui.ddl_project_list
        self.border_widgets = self.get_border_widgets()
        self.clip_name = None
        self.output_path = None
        self.user = os.getlogin()
        self.progress_bar = None

        # Qthread worker objects.
        self.stopwatch_thread = None
        self.processing_started = False
        self.capture_canceled = False
        self.capture_thead = None

        # Private variable for mouse press on UI.
        self.__press_pos = QPoint()

        # Set defaults on launch.
        self.set_ui_defaults()

        # connect UI to functions
        self.ui.txtBox_clip_name.textChanged.connect(self.format_clip_name)
        self.ui.btn_bg_toggle.clicked.connect(
            lambda: self.draggable_ui_toggle(not self.is_ui_draggable))
        self.ui.btn_record.clicked.connect(self.change_recording_state)
        self.ui.btn_pause.clicked.connect(lambda: self.pause_recording(self.is_paused))
        self.ui.btn_cancel.clicked.connect(self.cancel_operation)
        self.ui.btn_review_folder.clicked.connect(self.open_review_folder)
        self.ui.btn_help.clicked.connect(self.open_help)
        self.ui.btn_exit.clicked.connect(self.exit_app)
    
    # **************************************************************************
    # Enable / disable UI funtionality

    def get_border_widgets(self):
        """Collects border widgets of main UI window based on name.

        Returns:
            List of widget objects.
        """

        all_widgets = self.ui.central_widget.children()
        edge_widgets = [
            widget for widget in all_widgets
            if not widget.objectName().find('edge') == -1
        ]
        return edge_widgets

    def set_widget_colour(self, widgets, q_color, widget_opacity):
        """Changes appearance of widget objects.

        Args:
            widgets: List of widgets to be changed.
            q_color: QColor object for new RGB value, e.g. QColor(60, 60, 60).
            widget_opacity: Float value for new opacity value.
        """

        if not widgets:
            return
        for w in widgets:
            # Set opacity.
            widget_opacity_effect = QGraphicsOpacityEffect(w)
            widget_opacity_effect.setOpacity(widget_opacity)
            # Set colour.
            widget_palette = w.palette()
            widget_palette.setColor(w.backgroundRole(), q_color)
            # Apply settings.
            w.setPalette(widget_palette)
            w.setGraphicsEffect(widget_opacity_effect)
            w.setAutoFillBackground(True)
   
    def create_project_list(self):
        """Reads current projects in production from settings file.

        When recorded image files are created they are tagged with the project
        that they are from, if no prjects can be found a temporary 'testing'
        project name is used. These project names are used to populate the 
        drop down list in the UI for the user to select.

        Returns:
            List of strings.
        """
        CONFIG.clear()
        CONFIG.read(SETTINGS_FILE)
        try:
            project_names = get_config_values('current_projects', 'projects')
            if project_names:
                names_formatted = project_names.replace("'", "")
                project_list = names_formatted.split(", ")
        except KeyError:
            project_list = ['testing']

        project_list.sort()
        return project_list

    def format_clip_name(self, txt):
        """Checks the name of clip as the user is inputting the text.

        As the user inputs a name for the recording in the UI the text is 
        checked to make sure only ascii characters are being input to avoid 
        crashes during the image processing stage or when the image files are 
        being converted to a video in the archiving stage.

        Args:
            txt: String passed from the text input of main UI window.
        """

        current_text = self.ui.txtBox_clip_name.text()
        current_pos = self.ui.txtBox_clip_name.cursorPosition()

        for letter in txt:
            legal_txt = string.ascii_letters
            legal_txt += LEGAL_TXT_CHARACTERS
            if letter not in legal_txt:
                current_text = current_text[:-1]

        self.ui.txtBox_clip_name.setText(current_text)
        self.ui.txtBox_clip_name.setCursorPosition(current_pos)

        # Make sure to strip any extra whitespace.
        self.clip_name = current_text.strip()

    def set_ui_defaults(self):
        """Applies default settings to the UI on launch."""

        # Set corner grips for window resizing.
        self.grip_size = 20
        self.corner_grips = []
        for i in range(4):
            grip = QSizeGrip(self)
            grip.resize(self.grip_size, self.grip_size)
            self.corner_grips.append(grip)

        self.setMinimumSize(1400, 200)

        # Hide elements / progress bar text.
        self.set_idle_ui()
        # set main window attributes
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Populate projects list.
        current_projects = self.create_project_list()
        if current_projects:
            self.project_list.addItems(current_projects)

        # Temp relic icon
        relic_item = [
            x for x in range(self.project_list.count())
            if self.project_list.itemText(x) == 'Relic'
        ]
        if relic_item:
            hat_icon = u":/32x32/icons/32x32/icons8-cowboy-hat-32.png"
            icon = QIcon(hat_icon)
            self.project_list.setItemIcon(relic_item[0], icon)

        # Set drag widget defaults.
        drag_widget = [self.ui.w_drag]
        self.set_widget_colour(drag_widget, QColor(60, 60, 60), 0.4)

        # Set colour  of top widget around buttons.
        menu_widget = [self.ui.w_mask]
        self.set_widget_colour(menu_widget, QColor(30, 40, 50), 1.0)

    def lock_ui_toggle(self, is_recording):
        """Enables or disables UI elements to prevent any user input."""

        # Prevent the user from resizing UI window.
        if is_recording:
            self.setFixedSize(self.size())
        else:
            self.setMinimumSize(1000, 300)
            self.setMaximumSize(5000, 5000)

        self.update()

    def draggable_ui_toggle(self, is_draggable=False):
        """Enables or disables UI to stop recording window being moved."""

        on_icon = u":/48x48/icons/48x48/icons8-toggle-on-48.png"
        off_icon = u":/48x48/icons/48x48/icons8-toggle-off-48.png"

        new_icon = off_icon
        if is_draggable:
            new_icon = on_icon

        self.is_ui_draggable = is_draggable
        self.ui.w_drag.setAttribute(Qt.WA_NoSystemBackground, not is_draggable)
        self.ui.w_drag.setAttribute(Qt.WA_TranslucentBackground, not is_draggable)

        self.ui.btn_bg_toggle.setIcon(QIcon(new_icon))
        self.ui.btn_bg_toggle.setIconSize(QSize(34, 34))

        self.update()

    def cancel_operation(self):
        """Cancels any image capture or image processing operations."""

        if self.is_recording or self.is_paused:
            LOGGER.info('Canceling image capture')
            self.capture_canceled = True
            self.stop_recording()

        if self.processing_started:
            LOGGER.info('Canceling image processing')
            self.process_worker.cancel_processor()
            self.processing_started = False
            # self.image_process_threadpool.clear()

    def set_ui(self, recording_state, recording_enable, paused_state, widget_color,
               pause_enable, pause_btn_text, cancel_enable):
        """Changes state or appearance of UI elements.

        When the UI window changes from an idle to recording state certain UI
        elements need to be disabled to prevent any user input. The colour and 
        appearance of specific widgets also indicate to the user if recording
        or processing is currently in progress.

        Args:
            recording_state: Boolean for if the window is currently reading and
                saving frames.
            paused_state: Boolean for if the user has pressed the paused button
                to stop recording frames.
            widget_color: PyQt 'GlobalColor' for the updated appearance of the 
                border widgets of the window, e.g. 'Qt.green'
            pause_enable: Boolean for whether or not the pause button should be
                interactable for the user.
            pause_btn_text: String to be displayed on the pause button.
            cancel_enable: Boolean for whether or not the cancel button is
                interactable.
        """

        self.is_recording = recording_state
        self.is_paused = paused_state

        lock_resize = False
        if self.is_recording:
            lock_resize = True
        self.lock_ui_toggle(lock_resize)

        self.draggable_ui_toggle(not self.is_recording)
        self.set_widget_colour(self.border_widgets, widget_color, 0.6)
        self.ui.btn_record.setEnabled(recording_enable)
        self.ui.btn_pause.setEnabled(pause_enable)
        self.ui.btn_pause.setText(pause_btn_text)
        self.ui.btn_cancel.setEnabled(cancel_enable)
        self.ui.btn_bg_toggle.setEnabled(not self.is_recording)

        self.ui.ddl_project_list.setEnabled(not self.is_recording)
        self.ui.txtBox_clip_name.setEnabled(not self.is_recording)

        self.update()

    def set_idle_ui(self):
        """Default settings to change the UI to idle state."""

        self.set_ui(False, True, False, QColor(40, 125, 45), False, 'Pause', False)
        self.recording_timer('')
        self.remove_progress_bar()
    
    def set_recording_ui(self):
        """Default settings to change the UI to recording state."""

        self.set_ui(True, True, False, Qt.red, True, 'Pause', True)

    def set_paused_ui(self):
        """Default settings to change the UI to paused state."""

        self.set_ui(False, True, True, Qt.cyan, True, 'Resume', True)

    def set_processing_ui(self):
        """Default settings to change the UI to image processing state."""

        self.set_ui(False, False, False, Qt.green, False, 'Pause', True)

    def create_progress_bar(self):
        """Creates progress bar from imported custom QWidget."""

        if self.progress_bar:
            self.remove_progress_bar()

        self.progress_bar = ProgressBar(self)
        self.set_progress_bar_position()
        self.progress_bar.value = 0
        self.progress_bar.setMinimumSize(self.progress_bar.width(),
                                         self.progress_bar.height())
        self.progress_bar.show()

    def remove_progress_bar(self):
        """Removes progress bar from UI and destroys the object."""

        if self.progress_bar:
            self.progress_bar.hide()
            self.progress_bar.close()
            self.progress_bar.destroy()

    def set_progress_bar_position(self):
        """Updates the position of the progress bar.

        When the main UI is moved or resized the new position will be 
        calculated and applied to the progress bar object to keep it in the 
        middle of the window and visible to the used.
        """

        if not self.progress_bar:
            return

        window = self.progress_bar
        w, h, pos = self.get_window_position()
        x_pos = (w / 2 - window.width() / 2)
        y_pos = (h / 2 - window.height() / 2) + 60
        window.move(x_pos, y_pos)

    def set_progress_bar_perc(self, progress):
        """Sets the percentage on the progress bar.

        Args:
            progress: Float percentage for the current task.
        """

        rounded_progress = round(progress * 100)
        self.progress_bar.change_value(rounded_progress)
        sys.stdout.flush()
    
    def recording_timer(self, timer_txt):
        """Receives Signal from RecordingTimer and sets text on UI.

        The Qtimer in the RecordingTimer Class emits the current duration since
        the recording button was pressed, this is displayed to the user in the
        text of the 'Record' button.

        Args:
            timer_txt: String for the text to be displayed on the UI.
        """

        btn_txt = f'Stop Recording: {timer_txt}'
        if not self.is_recording:
            btn_txt = 'Record'
        self.ui.btn_record.setText(f'{btn_txt}')

    # **************************************************************************
    # Thread creation

    def create_thread(self, worker):
        """Creates a new QThread object to run a task.

        A Qthread object is created and the worker that is passed to the 
        method is connected so that once the task has completed it's execution
        both objects are started and stopped correctly.

        Args:
            worker: Class object to be executed when the thread starts.

        Returns:
            QThread object which has the worker correctly connected to it.
        """

        new_thread = QThread()
        worker.moveToThread(new_thread)
        new_thread.started.connect(worker.run)
        worker.signals.finished.connect(new_thread.quit)
        return new_thread    

    def create_recording_timer_thread(self):
        """Creates and starts a new QThread for the QTimer class.

        The current duration of the recording is kept track of by a PyQt Qtimer
        and every second the time is emit via a Signal back to the main UI to 
        be displayed to the user.
        """

        LOGGER.info('Creating timer thread')

        self.stopwatch_worker = RecordingTimer()
        self.stopwatch_thread = self.create_thread(self.stopwatch_worker)
        self.stopwatch_worker.signals.record_duration.connect(self.recording_timer)
        self.stopwatch_worker.signals.stop_capture.connect(self.stop_recording)
        self.stopwatch_thread.start()

    def create_capture_thread(self):
        """Creates and starts a new QThread for the image capturing class.

        Once the record button is pressed the position of the UI is read and
        passed to the ImageCapture class which saves frames of the screen to 
        Numpy binary files (.npy)
        """

        LOGGER.info('Creating capture thread')

        if self.capture_thead:
            self.capture_worker.cancel_capture()
            self.kill_active_threads(self.capture_thead)        

        w, h, pos = self.get_window_position()
        self.capture_worker = ImageCapture(w, h, pos, self.clip_name, self.fps)
        self.capture_thead = self.create_thread(self.capture_worker)
        self.capture_worker.signals.captured_frames.connect(self.start_image_processing)
        self.capture_worker.signals.canceled.connect(clean_cache_folder)
        self.capture_thead.start()

    def create_processing_thread(self):
        """Creates and starts a new QThread for the image processing class.

        To minimise the UI from hanging or freezing on the main thread a 
        separate thread is created to manage the processing of captured cache
        files.
        """

        self.processing_started = True
        self.process_worker = ImageProcessor(self.start_frame, self.captured_frames,
                                             self.output_path, self.project,
                                             SLATE_SWATCHES)

        self.process_thead = self.create_thread(self.process_worker)
        self.process_worker.signals.progress.connect(self.set_progress_bar_perc)
        self.process_worker.signals.finished.connect(self.image_processing_finished)
        self.process_thead.start()
    
    # **************************************************************************
    # Screen recording
    def get_window_position(self):
        """Reads the current position of the UI window in screen space.

        Returns:
            ui_width: Integer for the width of the window.
            ui_height: Integer for the height of the window.
            ui_position: QPoint Tuple read from top left of window.
        """

        ui_width = self.ui.w_drag.frameGeometry().width()
        ui_height = self.ui.w_drag.frameGeometry().height()
        ui_position = self.ui.w_drag.mapToGlobal(QPoint(0, 0))

        return ui_width, ui_height, ui_position

    def set_frame_rate(self):
        """Frames per second for recording is read from settings files."""

        # Use default fps incase settings file can't be read.
        self.fps = FRAME_RATE
        if os.path.exists(SETTINGS_FILE):
            CONFIG.clear()
            CONFIG.read(SETTINGS_FILE)
            try:
                self.fps = get_config_values('capture_frame_rate', 'frame_rate')
                self.fps = int(self.fps)
            except KeyError:
                self.fps = FRAME_RATE

    def start_recording(self):
        """Starts the recording process.

        Returns:
            False if correct information hasn't be input by the user for the 
            name of the clip or the current project.
        """

        LOGGER.info('Recorder is starting')

        # Check for clip name and start capturing.
        video_clip_name = self.ui.txtBox_clip_name.text()
        project_name = self.project_list.currentText()

        # Warning windows use ctypes so they are on top of all windows.
        if not video_clip_name:
            message_box('Set a name for your clip', 'Error', 0x1000)
            return
        if not project_name:
            message_box('Select a project', 'Error', 0x1000)
            return

        # Set UI for recording.
        self.set_recording_ui()

        # Create timer QThread for record button visual feedback.
        self.create_recording_timer_thread()
        self.is_recording = True

        self.set_frame_rate()

        # Create QThread for cature class to execute on.
        self.create_capture_thread()                

    def change_recording_state(self):
        """Changes state of UI when the 'Record' button is pressed.

        When the record button is pressed the main UI window will be in one of
        three different states, 'recording' / 'paused' / 'idle'. Depending on 
        which state it is currently in the recording process will either start, 
        stop or be paused.
        """

        LOGGER.info('Record button pressed')

        self.capture_canceled = False
        # If not recording then the recorder is idle or paused.
        if not self.is_recording:
            # If the recorder is paused then resume.
            if self.is_paused:
                self.stop_recording()
            else:
                self.start_recording()
        else:
            self.stop_recording()

    def pause_recording(self, is_paused):
        """Pauses or resumes the recording process. 

        It's possible to move the main UI window when the recording is paused
        so it's important to update the window position in the capture QThread
        so the correct part of the screen is recorded.

        Args:
            is_paused: Boolean for if the window state has been set to paused.
        """

        LOGGER.info('Pause button pressed')

        resume_icon = u":/48x48/icons/48x48/icons8-start-48.png"
        pause_icon = u":/48x48/icons/48x48/icons8-pause-squared-48.png"

        if is_paused:
            # If the ui was moved during pause send new position to worker.
            LOGGER.info('Resuming and sending updated widget position')
            new_icon = pause_icon
            w, h, pos = self.get_window_position()
            self.capture_worker.update_position([w, h, pos])

            # Set ui back to recording mode
            self.set_recording_ui()
        else:
            LOGGER.info('Pausing the recording')
            # Set ui to paused mode.
            new_icon = resume_icon            
            self.set_paused_ui()

        self.ui.btn_pause.setIcon(QIcon(new_icon))
        self.ui.btn_pause.setIconSize(QSize(34, 34))
        self.stopwatch_worker.timer_paused = not is_paused
        self.capture_worker.capturing_paused = not is_paused

    def stop_recording(self):
        """Stops the recording process.

        When the user pressed the 'Stop Recording' button the QTimer and 
        ImageCapture Qthreads will quit which starts the image processing. 
        """

        LOGGER.info('Recording stopped')

        self.stopwatch_worker.timer_running = False
        self.capture_worker.stop_capture()
        self.capture_thead.quit()
        self.is_recording = False
        self.set_processing_ui()
        self.recording_timer('')

        if self.capture_canceled:
            self.set_idle_ui()
            return

    # **************************************************************************
    # Captured image processing
    def start_image_processing(self, cache_folder):
        """Starts processing captured image files.

        Once the 'stop recording' button is pressed the QThread connected to 
        the ImageCapture class will emit a Signal back to the main UI to 
        indicate capturing is finished. That Signal is connected to this 
        method which creates a new QThred to process and convert all captured
        frames.

        Args:
            cache_folder: String for the folder path of the location where the 
            temporary cached image files were saved.

        Returns:
            False if capture was canceled and not stopped.
        """

        if self.capture_canceled:
            LOGGER.info('Capture was canceled')
            self.set_idle_ui()
            return

        LOGGER.info('Capture finished - ready for processing')

        # Add progress bar to UI.
        self.create_progress_bar()

        # Grab all recorded frames from temp folder.
        self.captured_frames = collect_files(cache_folder, CACHE_FORMAT)

        self.num_frames = len(self.captured_frames)
        if self.num_frames == 0:
            LOGGER.error('No frames captured')
            self.image_processing_finished()

        log_txt = f'{self.num_frames} frames have been captured'
        LOGGER.info(log_txt)

        # Read how much RAM was used, mainly for debugging.
        process = psutil.Process(os.getpid())
        bytes_size = process.memory_info().rss
        log_txt = f'Amount of memory used was {size(bytes_size)}'
        LOGGER.info(log_txt)

        LOGGER.info('Image processing started')
        self.start_t = time.perf_counter()
        
        self.project = self.project_list.currentText()
        self.date = get_next_workday()
        self.output_path = self.create_review_folder(self.date)
        log_txt = f'Output path is {self.output_path}'
        LOGGER.info(log_txt)

        # The recorded frames can still be processed even if the slate images
        # are not found, the start frame is adjusted based on this.
        if not os.path.exists(SLATE_BG):
            self.start_frame = 0
        else:
            self.start_frame = 1
            self.create_slate()

        self.create_processing_thread()

    def create_slate(self):
        """Creates slate image for the first frame of the image sequence."""

        img_slate = Image.open(SLATE_BG)
        draw = ImageDraw.Draw(img_slate)
        font = ImageFont.truetype('arial', 46)
        draw.text((910, 314), self.project, (255, 255, 255), font=font)
        draw.text((910, 393), self.clip_name, (255, 255, 255), font=font)
        draw.text((910, 474), self.user, (255, 255, 255), font=font)
        draw.text((910, 553), str(self.date), (255, 255, 255), font=font)
        write_image(img_slate, self.output_path, self.project)

    def image_processing_finished(self):
        """Sets variables and UI state back to idle once processing is done."""

        LOGGER.info('Image processing finished')

        end_t = time.perf_counter()
        duration = end_t - self.start_t
        num_frames = self.num_frames
        log_txt = f'Processing {num_frames} frames took {duration:.4f}s total'
        LOGGER.info(log_txt)

        self.set_idle_ui()

    # **************************************************************************
    # Manage external folders

    def create_review_folder(self, date_folder):
        """Creates a folder path using previous information collected.

        Once the necessary variables have been created a final folder path can
        be created for the destination of the converted image files.

        Args:
            date_folder: String for the date to be used in the folder path.

        Returns:
            String for the full folder path to be used. Returns False if there
            is an error when creating the path.
        """

        folder = (f'{self.review_folder}\\{self.date}\\'
                  f'{self.user}\\{self.clip_name}')
        new_folder = create_folder(folder)

        if not new_folder:
            error = 'Failed to create output folder. Please check the network'
            ctypes.windll.user32.MessageBoxW(0, error, 'Error', 0x1000)
            return
        file_out = f'{folder}\\{self.clip_name}'
        return file_out

    def open_help(self):
        """Reads web address to relevant wiki page from settings file."""

        if not os.path.exists(SETTINGS_FILE):
            return
        CONFIG.clear()
        CONFIG.read(SETTINGS_FILE)
        try:
            wiki = get_config_values('wiki_page', 'page')
        except KeyError:
            wiki = ''
        if not wiki:
            return
        os.startfile(wiki)

    def open_review_folder(self):
        """Opens review folder in windows expolorer."""

        review_folder = self.review_folder

        date = get_next_workday()
        date_folder = f'{review_folder}\\{date}'
        if os.path.exists(date_folder):
            review_folder = date_folder
        user_folder = f'{review_folder}\\{self.user}'
        if os.path.exists(user_folder):
            review_folder = user_folder

        if os.path.exists(review_folder):
            log_txt = f'Opening folder {review_folder}'
            LOGGER.info(log_txt)
            os.startfile(review_folder)
   
    # **************************************************************************
    # Window Events
    def resizeEvent(self, event):
        """PyQt event triggered when user changes size of UI window."""

        new_size = event.size()
        new_width = new_size.width()
        new_height = new_size.height()

        min_width = 1000
        min_height = 500

        if new_width < min_width:
            self.setMinimumSize(min_width, new_height)
        if new_height < min_height:
            self.setMinimumSize(new_width, min_height)

        QMainWindow.resizeEvent(self, event)
        rect = self.rect()
        # Top right
        self.corner_grips[1].move(rect.right() - self.grip_size, 0)
        # Bottom right
        self.corner_grips[2].move(
            rect.right() - self.grip_size, rect.bottom() - self.grip_size)
        # Bottom left
        self.corner_grips[3].move(0, rect.bottom() - self.grip_size)

        # If the progress bar is active then it will need to be moved.
        self.set_progress_bar_position()
    
    def mousePressEvent(self, event):
        """PyQt event triggered when user clicks on UI window.

        The event will filter out any input that isn't the left mouse button
        as well as checking to see if the UI has been locked using the 
        'is_ui_draggable' variable. The position of the mouse press is stored
        in the private class variable '__press_pos'.
        """

        if event.button() == Qt.LeftButton and self.is_ui_draggable is True:
            self.__press_pos = QPoint(event.position().x(), event.position().y())
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """PyQt event triggered when user attempts to drag the UI window.

        If the UI has not been locked and the private class variable 
        '__press_pos' can be read the window position will be moved to the 
        mouse cursor allowing the user to drag the UI around.
        """

        if not self.__press_pos.isNull() and self.is_ui_draggable is True:
            x_pos = event.scenePosition().x()
            y_pos = event.scenePosition().y()
            self.move(self.pos() + QPoint(x_pos, y_pos) - self.__press_pos)

    def mouseReleaseEvent(self, event):
        """PyQt event triggered when user releases the mouse button.

        On releasing the mouse button the position of the cursor will be stored
        in the private class variable '__press_pos'.
        """

        if event.button() == Qt.LeftButton and self.is_ui_draggable is True:
            self.__press_pos = QPoint()
            super().mouseReleaseEvent(event)
    
    # **************************************************************************
    # Exit app
    def kill_active_threads(self, thread_object):
        """Quits a QThread if it's found to be still running. 
        
        Args:
            thread_object: QThread object to test if active.
        """
        time.sleep(0.4)
        try:
            if thread_object.isRunning():
                log_txt = f'{thread_object} was still running'
                LOGGER.warning(log_txt)
                thread_object.quit()
        except AttributeError:
            log_txt = f'{thread_object} not found'
            LOGGER.error(log_txt)

    def exit_app(self):
        """Performs checks when user trys to exit the main UI.

        Once the user exits the tool any active QThread objects are shutdown or
        quit safely to avoid crashes. The cache folder is also cleaned.
        """

        try:
            if self.stopwatch_thread:
                self.stopwatch_worker.timer_running = False
                self.kill_active_threads(self.stopwatch_thread)
            if self.capture_thead:
                self.capture_worker.cancel_capture()
                self.kill_active_threads(self.capture_thead)

            clean_cache_folder()
        except AttributeError as e:
            log_txt = f'{e}'
            LOGGER.error(log_txt)

        QCoreApplication.instance().quit()


def open_window():
    """Performs neccessary steps to launch the program.

    Returns:
        False if launch checks fail.
    """

    # Output version file locally to be read by TNH listener.
    save_version_file()

    # Check to see if the review folder can be found on the network.
    lib_review_folder = ''
    if os.path.exists(SETTINGS_FILE):
        CONFIG.clear()
        CONFIG.read(SETTINGS_FILE)
        try:
            lib_review_folder = get_config_values('review_data_folder',
                                                  'folder_path')
        except KeyError as e:
            LOGGER.error(e)
            lib_review_folder = ''

    # The launch checks and show warnings to user before launch and also return
    # the final output folder for recordings.
    output_folder = launch_checks(lib_review_folder)

    # Stop launch if checks fail.
    if not output_folder:
        return

    log_txt = f'Output folder for recordings will be {output_folder}'
    LOGGER.info(log_txt)

    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    window = ScreenRecorderUI(output_folder)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # Enable console logger to show errors only.
    set_console_logger(level_input=20)
    enable_output_logger(level_input=20)

    # Launch program.
    open_window()

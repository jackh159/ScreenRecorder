#!/usr/bin/python3
"""This module reads and converts captured caches files to an image sequence."""

import os

import cv2
import numpy as np
from PIL import Image
from PySide6.QtCore import QThreadPool, QObject, QRunnable, Slot

from THNScreenRecorder.THN_PySideSignals import PySideSignals
from THNScreenRecorder.THN_FileManagement import IMAGE_RES, LOGGER, write_image


class ImageProcessor(QObject):
    """Manages the processing of captured frames using QRunnable / Qthreadpool.

    To reduce any lag of hanging in the main UI thread the processing of 
    captured frames are passed to a new QThread which off loads each frame in 
    to a queue managed by the global QThreadPool that picks up each frame when
    a thread becomes available.

    Args:
        start_num: Integer for what the number of the start frame should be.
        frames: List of the full paths to all recorded frame files.
        output: String for where the final images should be saved.
        project_name: String name of the current project selected by the user
            which will be used to tag the image files.
        swatch_file: String to the full file path of the swatch image.
    """

    # **************************************************************************
    # Init
    def __init__(self, start_num, frames, output, project_name, swatch_file=None):
        """Inits ImageProcessor with class attributes."""

        super().__init__()

        self.signals = PySideSignals()

        self.processing_images = False
        self.start_frame = start_num
        self.captured_frame_list = frames
        self.num_frames = len(self.captured_frame_list)
        self.output_path = output
        self.project = project_name
        self.swatch_path = swatch_file

        self.image_process_threadpool = QThreadPool.globalInstance()

    # **************************************************************************
    # Funtions
    def run(self):
        """This method is triggered once the QThread is started.

        Each image file is converted on it's own QThread, all of the necessary
        info is used when created the QRunnable object to keep track of the 
        naming and image order. This way frames can be created out of order 
        whenever new threads are available without breaking the recording.
        """

        # Loop over every cached file using the full file path and create a
        # QThread for each image that is added to the queue.
        num_threads = self.image_process_threadpool.maxThreadCount()
        log_txt = f'Multithreading with maximum {num_threads} threads'
        LOGGER.info(log_txt)

        # Reset the number of processed frames to keep track of new task.
        self.frames_saved = 0

        self.processing_images = True
        frame_number = 0
        frame_output_number = self.start_frame

        while self.processing_images:
            current_frame = self.captured_frame_list[frame_number]
            self.create_image_process_thread((frame_output_number, current_frame))

            frame_number += 1
            frame_output_number += 1

            if frame_number == self.num_frames:
                return

    def create_image_process_thread(self, frame):
        """Creates and starts a new QThread for the image capturing class.

        Once there is a list of file paths to process they are individually
        added to the threadpool and converted as soon as a thread becomes free.
        To keep the frames in order a number is passed along with the frame
        using enumerate.

        Args:
            frame: Tuple containing of the full file path to the .npy frame as
                well as the frame number, (number, file path).
        """

        log_txt = f'Creating image processing thread for frame {frame[0]}'
        LOGGER.info(log_txt)
        self.processing_worker = ImageConvertor(frame, self.output_path, self.project,
                                                self.swatch_path)
        self.processing_worker.signals.finished.connect(self.image_processing_monitor)
        self.image_process_threadpool.start(self.processing_worker)

    def image_processing_monitor(self):
        """Keeps track of the number of frames that have been processed.

        The QThread created to convert the .npy file to an image file will emit
        a PyQt Signal when it's finished which will keep increase the 
        'frames_saved' variable. Once the number of frames saved equals the 
        total number of frames recorded the 'finished' Signal will emit calling
        the 'image_processing_finished' method in the main UI.
        """

        self.frames_saved += 1
        prog = self.frames_saved / self.num_frames
        self.signals.progress.emit(prog)

        if prog == 1.0 or not self.processing_images:
            self.signals.finished.emit()

    def cancel_processor(self):
        """Cancels processing the list of captured frames."""

        self.processing_images = False
        self.image_process_threadpool.clear()
        self.signals.finished.emit()


class ImageConvertor(QRunnable):
    """Converts saved numpy binary file to image file.

    Args:
        captured_frame: Tuple containing the string file path of the saved .npy
            file as well as the integer frame number (frame number, path)
        out_path: String for the full file path of where the converted file 
            should be saved to.
        project_name: String name of the current project selected by the user
            which will be used to tag the image files.
        swatches: String to the full file path of the swatch image.
    """

    # **************************************************************************
    # Init
    def __init__(self, captured_frame, out_path, project_name, swatches=None):
        """Inits ImageConvertor with class attributes."""

        super().__init__()

        self.signals = PySideSignals()

        self.path = out_path
        self.frame = captured_frame
        self.project = project_name
        self.swatch_path = swatches

    # **************************************************************************
    # Funtions
    @Slot()
    def run(self):
        """This method is triggered once the QThread is started."""
        
        # Check if slate file can be found before processing.
        if os.path.exists(self.swatch_path):
            self.swatch = Image.open(self.swatch_path)
        else:
            self.swatch = None

        self.prepare_image()

    def prepare_image(self):
        """Performs checks and adjustments to file before saving to disk.

        Once the captured image is read the resolution is checked against the
        default settings to see if it needs to be scaled before overlaying with
        value swatches. Once image is written to disk the 'finished' Signal is 
        emitted back to the main UI to track the progress of entire sequence.
        """

        num, img = self.frame

        if type(img) == str:
            try:
                img = np.load(img)
            except FileNotFoundError as e:
                log_error = f'Error loading cached frame: {e}'
                LOGGER.error(log_error)
                return

        img_blank = Image.new('RGB', (IMAGE_RES[0], IMAGE_RES[1]))
        img_np = np.array(img, dtype=np.uint8)

        # Flip the numpy array to convert between BRG and RGB.
        img_capture_np = np.flip(img_np[:, :, :3], 2)

        # Use openCV to scale down the image, the third integer unpacked here
        # is the depth of the image which we don't need.
        im_height, im_width, _ = img_capture_np.shape

        # Standard HD resolution to scale down to unless specified in settings.
        w_out, h_out = IMAGE_RES

        # OpenCV pixel interp to use for shaper images.
        im_interp = cv2.INTER_LANCZOS4

        # Check frame size and see if it needs scaling down.
        if (im_width, im_height) > IMAGE_RES:
            log_txt = (f'Image {num} is being resized from '
                       f'({im_width}, {im_height}) to {IMAGE_RES}')
            LOGGER.info(log_txt)
            if im_width > w_out:
                ratio = w_out / im_width
            else:
                ratio = h_out / im_height
            new_w = int(im_width * ratio)
            new_h = int(im_height * ratio)
            im_resize_np = cv2.resize(img_capture_np,
                                      dsize=(new_w, new_h),
                                      interpolation=im_interp)
        else:
            im_resize_np = img_capture_np

        # Convert image back to PIL for combining with overlay images.
        image_resized = Image.fromarray(np.uint8(im_resize_np)).convert('RGB')

        # Grab the width / height once captured frame is conformed to HD.
        new_w, new_h = image_resized.size
        offset = ((IMAGE_RES[0] - new_w) // 2, (IMAGE_RES[1] - new_h) // 2)

        # The output frame is a PIL object.
        output_frame = img_blank
        output_frame.paste(image_resized, offset)

        # If swatches overlay image is found overlay with capture.
        if self.swatch is not None:
            output_frame.paste(self.swatch, (0, 0), mask=self.swatch)

        # Write final image to disk.
        write_image(output_frame, self.path, self.project, frame_number=num)
        self.signals.finished.emit()

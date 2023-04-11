#!/usr/bin/python3
"""This module contains all the shared constants and funtions."""

import os
import shutil
import logging
import datetime
import configparser

import holidays
from dateutil.relativedelta import relativedelta

import numpy as np
from tifffile import imwrite

LOCAL_CACHE = f"{os.getenv('APPDATA')}\\temp\\screen_recorder"
LIB_PATH = 'L:\\Library\\_tools\\THN_ReviewTools\\THN_screenRecorder2.0'
SETTINGS_FILE = f'{LIB_PATH}\\settings.ini'
IMAGE_FORMAT = '.tiff'
CACHE_FORMAT = '.npy'
IMAGE_RES = (1920, 1080)

LOGGER = logging.getLogger()
CONFIG = configparser.ConfigParser()


# **************************************************************************
# Config parser.
def get_config_sections():
    """Collects all sections from INI file with configparser.

    Returns:
        List of strings for sections that have been read.
    """

    return CONFIG.sections()


def get_config_keys(section):
    """Collects all keys in a specific section from INI file with configparser.

    Args:
        section: String for the name of the specific section.

    Returns:
        List of strings for the keys that have been read.
    """

    return list(CONFIG[section].keys())


def get_config_values(section, key):
    """Collects all values from a specific key in a INI file with configparser.

    Args:
        section: String for the name of the specific section.
        key: String for the name of the specific key.

    Returns:
        Strings for the value that has been read.
    """

    return CONFIG[section][key]


def save_config_file(main_section, key_values, output_path, overwrite=True):
    """Saves information in an INI file using configparser.

    Args:
        main_section: String for the name of the specific section.
        key_values: Dict containing the keys and values to be saved.
        output_path: String for the specified output path for INI file.
        overwrite: Boolean for whether or not information should be 
            overwritten, updated or appended to the INI file.

    Returns:
        False if information was unsuccessfully saved.
    """

    CONFIG.clear()
    CONFIG.read(output_path)
    CONFIG[main_section] = {}
    key = CONFIG[main_section]
    for k in key_values.items():
        key[k[0]] = k[1]
    try:
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except PermissionError:
                return
        if not overwrite:
            append = 'a'
        else:
            append = 'w'
        if not os.path.exists(output_path):
            with open(output_path, append) as configfile:
                CONFIG.write(configfile)
    except FileNotFoundError:
        return


# **************************************************************************
# Create files / folders.
def write_image(image, path, project, frame_number=0):
    """Saves catured and prepared PIL image to the specified folder on disk.

    Args:
        image: PIL image object to be saved to disk.
        path: String for the output path for the image.
        project: String which will be used for the image tag.
        num: An integer for the current frame number to be used in the output.
            name of the image file.

    Returns:
        False if information was unsuccessfully saved.
    """

    # convert PIL image to np array
    np_image = np.asarray(image)

    # save tiff files to folder
    path = f'{path}_{frame_number:04}{IMAGE_FORMAT}'
    imwrite(path, np_image, compression='deflate', description=project)
    return os.path.exists(path)


def create_folder(path):
    """Check if folder exists, if not creates a new empty folder.

    Args:
        path: String for the folder to be created.

    Returns:
        True if the folder already exists. Returns True if a new folder is 
        created successfully and False if not.
    """

    if (folder_exists := os.path.exists(path)):
        return folder_exists
    os.makedirs(path)
    return os.path.exists(path)


def clean_cache_folder():
    """Removes any files from the local cache folder."""

    cache_folders = next(os.walk(LOCAL_CACHE))[1]
    log_txt = f'Cleaning cache folder: {cache_folders}'
    LOGGER.info(log_txt)
    try:
        for folder in cache_folders:
            shutil.rmtree(f'{LOCAL_CACHE}\\{folder}')
    except OSError as e:
        log_txt = f'Error removing folder: {folder}, {e.strerror}'
        LOGGER.error(log_txt)


def collect_files(folder, file_ext):
    """Returns List of files from folder path provided.

    Args:
        folder: String of full folder path.
        file_ext: String for the file extension to use when searching for 
            files.

    Returns:
        List of full paths to any files that are found, if no files found
        an empty list will be returned.
    """
    log_txt = f'Collecting files in folder: {folder}'
    LOGGER.info(log_txt)

    if os.path.isdir(folder):
        all_files = next(os.walk(folder))[2]
        files_out = [f for f in all_files if (f.endswith(file_ext))]
        file_paths = [f'{folder}\\{file}' for file in files_out]
        return file_paths


# **************************************************************************
# Time and date helpers to filter workdays.
def string_to_date(date):
    """Returns datetime object from string.

    Args:
        date: String of date typically read from folder names.

    Returns:
        Datetime object, 'datetime.date'
    """

    if type(date) == str:
        return datetime.date.fromisoformat(date)


def get_date_range(start, end):
    """Collects all the dates inbetween a start and end date.

    Args:
        start: Datetime object for starting date.
        end: Datetime object for end date.

    Returns:
        List of Datetime date in format, [YYYY-MM-DD, YYYY-MM-DD]
    """

    delta = end-start
    days = [start+datetime.timedelta(days=i) for i in range(delta.days+1)]
    return days


def collect_days_to_skip():
    """Reads dates from settings file for days to skip.

    Specific dates can be put in the settings file for days to be skipped
    when trying to find the next available workday. This is used for times
    when the studio is closed.

    Returns:
        List of all the dates in between any dates that are found in the 
        settings file. Returns an empty list if nothing is found.
    """

    # Check for custom dates in settings file.
    dates_out = []
    if not os.path.exists(SETTINGS_FILE):
        return dates_out
    CONFIG.clear()
    CONFIG.read(SETTINGS_FILE)
    section_name = 'days_to_skip'
    try:
        dates = get_config_keys(section_name)
    except KeyError:
        dates = []
    if not dates:
        return []
    for d in dates:
        try:
            date_range = get_config_values(section_name, d)
        except KeyError:
            date_range = None
        if not date_range:
            continue
        dates_formatted = date_range.replace("'", "")
        date_list = dates_formatted.split(", ")
        if len(date_list) == 1:
            dates_out.append(string_to_date(date_list[0]))
        if 3 > len(date_list) > 1:
            start_date = string_to_date(date_list[0])
            end_date = string_to_date(date_list[1])
            all_dates = get_date_range(start_date, end_date)
            dates_out = [*dates_out, *all_dates]

    return dates_out


def collect_public_holidays():
    """Returns a list of all of the public holidays for the current year.

    Returns:
        List of dates for all the public holidays in format YYYY-MM-DD.
    """
    this_year = datetime.date.today().year
    public_holidays_hu = holidays.country_holidays('HU', years=this_year)
    # Only specifying the first index as second is the holiday name.
    holiday_dates = [date[0] for date in public_holidays_hu.items()]

    return holiday_dates


def collect_weekends(date_today, num_months=3):
    """Returns list of dates for all the weekends during specific period.

    Args:
        date_today: Datetime object for current date.
        num_months: Integer for the length of time to search for weekends
            in months, defaults to 3 months.

    Returns:
        List of all dates found, in format YYYY-MM-DD. Returns empty list 
        if no dates are found.
    """

    end = date_today + relativedelta(months=+num_months)
    date_range = get_date_range(date_today, end)

    # Filter out any weekdays, 0 = monday.
    weekend_days = [date for date in date_range if date.weekday() > 4]
    if weekend_days:
        return weekend_days
    return []


def get_next_workday():
    """Performs number of checks to find the next working day.

    Starting from the current date the next workday is found by skipping
    over public holidays, weekends and any custom dates found in the 
    settings file. If a recording is done before 10am the current day is 
    used.

    Returns:
        String of the date found to be the next working day, returns empty 
        string if search fails.

    """
    LOGGER.info('Finding correct date for image output')
    date_folder_out = ''

    # Cutoff time, currently 10:00 am.
    time_cutoff = datetime.time(10, 00)

    # Date and time objects.
    today = datetime.datetime.now()
    time_now = today.time()
    today_date = today.date()

    if time_cutoff > time_now:
        LOGGER.info('Recording is for the same day')
        date_folder_out = today_date.strftime('%Y-%m-%d')
        return date_folder_out

    # Collect all dates, not worrying about duplicates.
    holidays = collect_public_holidays()
    days_to_skip = collect_days_to_skip()
    weekend_days = collect_weekends(today_date)

    # Combine all the collections, filter out duplicates using a Set.
    non_workdays = [*days_to_skip, *holidays, *weekend_days]
    non_workdays = [*set(non_workdays)]
    non_workdays.sort()

    # Loop dates to find next work day.
    next_workday = today_date + datetime.timedelta(1)
    while True:
        if next_workday in non_workdays:
            log_txt = f'Trying next day {next_workday}'
            LOGGER.info(log_txt)
            next_workday = next_workday + datetime.timedelta(1)
            continue
        log_txt = f'Date found: {next_workday}'
        LOGGER.info(log_txt)
        return next_workday

    date_folder_out = next_workday.strftime('%Y-%m-%d')
    return date_folder_out

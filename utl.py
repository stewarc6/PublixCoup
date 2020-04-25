# ==============================================================================
# title           : utl.py
# author          : Camiren Stewart
# date            : 2020.02.17
# version         : v1.0
# version notes   :
# usage           :
# python_version  :
# dependencies    :
# Assumptions     :
# ==============================================================================

import constants
import logging, os, re, shutil
from glob import glob


def create_log(debug, verbose):
    ''' Creates logger for file (fh) and console (ch) '''
    # create logger with 'spam_application'
    logger = logging.getLogger('log_application')
    logger.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
    # create file handler which logs even debug messages
    if debug is False: 
        ''' if debug arg is passed, dont save a log file  '''
        fh = logging.FileHandler(constants.LOG_NAME)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    # create console handler with a higher log level
    if verbose is True: 
        ''' if verbose is passed, print to console '''
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)


def create_symlink(debug, source, root_destination, filename):
    ''' Creates symlink '''
    if os.path.islink(os.path.join(root_destination, filename)):
        verbose_print("Symlink already exists: {0}".format(os.path.join(root_destination, filename)),"warning")
        return 1
    else:
        verbose_print(".. Creating Symlink: [{0}] ==> [{1}{2}]".format(source, root_destination, filename),'message')
        if debug:
            pass
        else: 
            os.symlink(source, os.path.join(root_destination, filename))
    return 0


def verbose_print(line, msg_type):
    module_logger = logging.getLogger('log_application')

    if msg_type.lower() == 'debug':
        module_logger.debug(line)
    elif msg_type.lower() == 'message':
        module_logger.info(line)
    elif msg_type.lower() == 'warning':
        module_logger.warning(line.upper())
    elif msg_type.lower() == 'error':
        module_logger.error(line)

# ==============================================================================
# title           : constants.py
# author          : Camiren Stewart
# date            : 2020.04.25
# version         : v1.1
# version notes   : Credentials now arguments
# usage           : constants.py
# python_version  : 3.7.6
# ==============================================================================

import os
import time

USER = ''
PASS = ''

DATE = time.strftime("%Y-%m-%d", time.localtime())
LOG_DATE = time.strftime("%Y-%m-%d.%H%M%S", time.localtime())
LOG_PATH = 'logs'
LOG_NAME = os.path.join(LOG_PATH, 'PublixCoup_{0}.log'.format(LOG_DATE))

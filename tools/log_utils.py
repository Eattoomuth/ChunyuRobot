# -*- coding: utf-8 -*-
import hashlib
import logging
import datetime
import os
import random

__author__ = 'wgx'

logging.basicConfig(level=logging.INFO, filemode='a')

LOG_DIR_ROOT = '../assets/logs'

run_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
run_id = run_time + '_' + str(random.randint(0, 1000000))
time_log_path = os.path.join(LOG_DIR_ROOT, run_id + '.log')
time_logger = logging.getLogger('time_logger')
time_file_handler = logging.FileHandler(time_log_path)
formatter = logging.Formatter(fmt='%(asctime)s %(message)s',
                              datefmt='%a, %d %b %Y %H:%M:%S')
time_file_handler.setFormatter(formatter)
time_logger.addHandler(time_file_handler)


def log_by_run_time(text, level=logging.INFO):
    time_logger.log(msg=text, level=level)



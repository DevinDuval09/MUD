'''logger used by Users, UserCollection, UserStatus, and UserStatusCollection'''

import logging
import os
import datetime

if not os.path.isdir(".//logs"):
    os.mkdir(".//logs//")

def get_log_name():
    '''generate log name'''
    today = datetime.datetime.now()

    return f'log_{today.month:0>2}_{today.day:0>2}_{today.year}.log'


log_num = get_log_name()

LOG_FORMAT = '"%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"'
formatter = logging.Formatter(LOG_FORMAT)

file_handler = logging.FileHandler(f'.//logs//{log_num}', mode='a')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.CRITICAL)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

if __name__ == '__main__':
    log_num = get_log_name()
    print(log_num)

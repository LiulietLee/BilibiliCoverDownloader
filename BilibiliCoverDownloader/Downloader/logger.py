# -*- coding: utf-8 -*-
# @Author: Haut-Stone
# @Date:   2017-09-30 15:22:05
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2017-10-16 15:01:24

from functools import wraps
import time


class Logger():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def log_response(info, index):
        print('====>(test{})\n'.format(index) + Logger.OKGREEN + info + Logger.ENDC + '\n')

    @staticmethod
    def log_title(info):
        print('\n' + Logger.WARNING + info + Logger.ENDC + '\n')

    @staticmethod
    def log_(info):
        print('\n' + Logger.FAIL + info + Logger.ENDC + '\n')


def my_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total time running: %s seconds" % (str(t1 - t0)))
        return result

    return function_timer

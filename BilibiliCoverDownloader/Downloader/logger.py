# -*- coding: utf-8 -*-
# @Author: Haut-Stone
# @Date:   2017-09-30 15:22:05
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2017-09-30 16:01:30


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
	def log_(info, index):

		print('\n' + Logger.FAIL + info + Logger.ENDC + '\n')
# -*- coding: utf-8 -*-
# @Time    : 2019/08/24 01:24
# @Author  : Dong Qirui
# @FileName: logger_utils.py
# @Software: PyCharm

import logging
import sys
from logging import handlers

sys


def setLogger () :
    '''
    
    :return:
    '''
    LOGGER = logging.getLogger()
    LOGGER.setLevel( logging.INFO )
    TIME_HANDLER = logging.handlers.TimedRotatingFileHandler( filename='project.log', when='D', interval=1, backupCount=2, encoding='utf-8' )
    # 必须是这种格式才能自动删除
    TIME_HANDLER.suffix = '%Y-%m-%d.log'
    LOGGER.addHandler( TIME_HANDLER )
    LOGGER.addHandler( logging.StreamHandler() )


setLogger()

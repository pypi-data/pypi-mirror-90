# -*- coding: utf-8 -*-
# @Time    : 2019/11/19 20:19
# @Author  : Dong Qirui
# @Software: PyCharm

from datetime import datetime, timedelta
from enum import Enum


class DateTimeFormat( Enum ) :
    '''
    
    '''
    DATETIME_FULL = '%Y-%m-%d %H:%M:%S'
    DATETIME_SHORT = '%Y-%-m-%-d %-H:%-M:%-S'
    DATE_FULL = '%Y-%m-%d'
    DATE_SHORT = '%Y-%-m-%-d'
    DATE_DIGITAL = '%Y%m%d'
    MONTH_FULL = '%Y-%m'


def getDateTime ( delta: int = 0 ) -> datetime :
    '''
    获取日期，明天：1；昨天：-1
    :return: datetime.datetime(2020, 11, 2, 21, 28, 22, 772748)
    '''
    return datetime.today() + timedelta( days=+delta )


def parseDateTime ( datetime_str: str, format_str: str ) -> datetime :
    '''
    从时间字符串转换时间
    :return: datetime.datetime(2020, 11, 2, 21, 28, 22, 772748)
    '''
    return datetime.strptime( datetime_str, format_str )


def getDateStrFormatDigital ( delta: int = 0 ) -> str :
    '''
    
    :return: '20190508'
    '''
    
    return getDateTimeStrFormatFull( delta, DateTimeFormat.DATE_DIGITAL )


def getDateStrFormatFull ( delta: int = 0 ) -> str :
    '''
    
    :return: '2019-05-08'
    '''
    return getDateTimeStrFormatFull( delta, DateTimeFormat.DATE_FULL )


def getDateStrFormatShort ( delta: int = 0 ) -> str :
    '''
    
    :return: '2019-5-8'
    '''
    return getDateTimeStrFormatFull( delta, DateTimeFormat.DATE_SHORT )


def getDateTimeStrFormat ( delta: int = 0, format_str: str = DateTimeFormat.DATETIME_FULL.value ) -> str :
    '''
    based on format_enum
    :return: '2019-05-08 16:43:18'
    '''
    return getDateTime( delta ).strftime( format_str )


def getDateTimeStrFormatEnum ( delta: int = 0, format_enum: DateTimeFormat = DateTimeFormat.DATETIME_FULL ) -> str :
    '''
    based on format_enum
    :return: '2019-05-08 16:43:18'
    '''
    return getDateTime( delta ).strftime( format_enum.value )


def getDateTimeStrFormatFull ( delta: int = 0 ) -> str :
    '''
    based on format_enum
    :return: '2019-05-08 16:43:18'
    '''
    return getDateTimeStrFormatFull( delta, DateTimeFormat.DATETIME_FULL )


def getDateTimeStrFormatShort ( delta: int = 0 ) -> str :
    '''
    based on format_enum
    :return: '2019-5-8 16:43:18'
    '''
    return getDateTimeStrFormatFull( delta, DateTimeFormat.DATETIME_SHORT )


def getMonthStrFormat ( delta: int = 0 ) -> str :
    '''
    
    :return: '2019-05'
    '''
    return getDateTimeStrFormatFull( delta, DateTimeFormat.MONTH_FULL )

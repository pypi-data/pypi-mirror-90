# -*- coding: utf-8 -*-
# @Time    : 2020/11/05 2:10 PM
# @Author  : Dong Qirui
# @FileName: encode_utils.py
# @Software: PyCharm
# @Version : 0.10

# How-To-Use：
# In [3]: from QrCerUtils.utils.encode import util_encode_detect
#
# In [4]: str_a =  b'\xc8\xab\xb2\xbf\xb3\xc9\xbd\xbb'
#
# In [5]: util_encode_detect.fix_coding(str_a)
# Out[5]: '全部成交'
#
# In [6]: util_encode_detect.get_coding(str_a)
# Out[6]: 'gbk'

import chardet


def get_coding ( str_input ) :
    '''
    获取编码格式
    :param str_input:
    :return:
    '''
    encoding: str = None
    try :
        if isinstance( str_input, bytes ) :
            encoding = chardet.detect( str_input )['encoding']
        elif isinstance( str_input, str ) :
            str_encode = str_input.encode( 'latin1' )
            encoding = chardet.detect( str_encode )['encoding']
        encoding = 'gbk' if encoding.__contains__( 'GB' ) else encoding
    except :
        pass
    return encoding


def fix_coding ( str_input ) :
    '''
    转换为真实编码
    :param str_input:
    :return:
    '''
    encoding: str = get_coding( str_input )
    str_decode = str_input
    try :
        if None is encoding :
            str_decode = str( str_input )
        if isinstance( str_input, bytes ) :
            str_decode = str( str_input, encoding )
        elif isinstance( str_input, str ) :
            str_encode = str_input.encode( 'latin1' )
            str_decode = str_encode.decode( encoding )
    except :
        pass
    return str_decode

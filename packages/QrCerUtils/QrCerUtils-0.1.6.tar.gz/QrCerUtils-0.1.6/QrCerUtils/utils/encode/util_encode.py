# -*- coding: utf-8 -*-
# @Time    : 2018/11/12 4:12 PM
# @Author  : Dong Qirui
# @FileName: encode_utils.py
# @Software: PyCharm
# @Version  : 0.10
# 已经过时，建议使用util_encode_detect

def get_coding ( strInput ) :
    '''
    获取编码格式
    :param strInput:
    :return:
    '''
    import sys
    
    if sys.version_info.major == 3 :
        unicode = str
    if isinstance( strInput, unicode ) :
        return "unicode"
    try :
        strInput.decode( "utf8" )
        return 'utf8'
    except :
        pass
    try :
        strInput.decode( "gbk" )
        return 'gbk'
    except :
        pass


def trans_utf8 ( strInput ) :
    '''
    转化为utf8格式
    :param strInput:
    :return:
    '''
    strCodingFmt = get_coding( strInput )
    if strCodingFmt == "utf8" :
        return strInput
    elif strCodingFmt == "unicode" :
        return strInput.encode( "utf8" )
    elif strCodingFmt == "gbk" :
        return strInput.decode( "gbk" ).encode( "utf8" )


def trans_gbk ( strInput ) :
    '''
    转化为gbk格式
    :param strInput:
    :return:
    '''
    strCodingFmt = get_coding( strInput )
    if strCodingFmt == "gbk" :
        return strInput
    elif strCodingFmt == "unicode" :
        return strInput.encode( "gbk" )
    elif strCodingFmt == "utf8" :
        return strInput.decode( "utf8" ).encode( "gbk" )


def assert_utf8 ( strInput ) :
    '''
    保证不会是unicode, 否则容易引发错误, python3已经修复默认编码
    :param strInput:
    :return:
    '''
    return trans_utf8( strInput ) if None != get_coding( strInput ) else str( strInput )

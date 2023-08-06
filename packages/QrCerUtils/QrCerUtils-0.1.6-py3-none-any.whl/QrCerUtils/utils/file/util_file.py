# -*- coding: utf-8 -*-
# @Time    : 2020/10/21 05:03
# @Author  : Dong Qirui
# @Software: PyCharm


def tail_file ( thefile, interval=0.002 ) :
    '''
    监控文件改动
    :param thefile:
    :param interval: 监控间隔，默认值0.002 = 2ms
    :return:
    '''
    import time
    
    thefile.seek( 0, 2 )
    while True :
        line_str = thefile.readline()
        if not line_str :
            time.sleep( interval )
            continue
        yield line_str

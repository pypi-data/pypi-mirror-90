# -*- coding: utf-8 -*-
# @Time    : 2019/09/16 11:49
# @Author  : Dong Qirui
# @Software: PyCharm
# import logging


import sys

if sys.version_info > (3,) :
    pass
else :
    if sys.version_info >= (2, 7) :
        pass
    else :
        pass
    import imp, sys
    
    imp.reload( sys ) ;
    _encoding_str = 'Default encoding changed from {_encoding_from} to {_encoding_to}'.format( _encoding_from=sys.getdefaultencoding(), _encoding_to='{_encoding_to}' )
    sys.setdefaultencoding( "utf8" )
    print( _encoding_str.format( _encoding_to=sys.getdefaultencoding() ) )

# -*- coding: utf-8 -*-
# @Time    : 2019/11/21 16:04
# @Author  : Dong Qirui
# @Software: PyCharm


import logging
import sys

from QrCerUtils.decorators.timeout.decorator_timeout import timeout


@timeout( 30 )
def image_limit_size ( content: bytes, limit_size: int = 1600000 ) -> bytes :
    '''
    限制图像尺寸
    :param content:
    :return:
    '''
    try :
        from io import BytesIO
        from PIL import Image
        
        if not len( content ) > limit_size :
            pass
        im = Image.open( BytesIO( content ) )
        limit = len( content ) / limit_size
        image = im.resize( (int( im.width / limit ), int( im.height / limit )), Image.NEAREST )
        image_bytes = BytesIO()
        image.save( image_bytes, format='JPEG' )
        content_resized = image_bytes.getvalue()
        print( len( content_resized ) )
        return content_resized
    except :
        logging.error( sys._getframe().f_code.co_name, exc_info=True )
        return None

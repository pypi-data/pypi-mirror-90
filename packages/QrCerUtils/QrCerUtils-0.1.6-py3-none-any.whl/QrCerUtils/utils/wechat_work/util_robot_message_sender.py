# -*- coding: utf-8 -*-
# @Time    : 2019/11/21 14:43
# @Author  : Dong Qirui
# @Software: PyCharm
import json
import logging
import sys

from QrCerUtils.decorators.timeout.decorator_timeout import timeout
from QrCerUtils.utils.wechat_work.util_robot_message_builder import message_builder


class robot_message_sender :
    
    def __init__ ( self, url: str ) -> None :
        self.url = url
        super().__init__()
    
    @timeout( 30 )
    def notification_wechat_work ( payload: json, key: str ) -> json :
        '''
    
        :param payload:
        :param key:
        :return:
        '''
        try :
            import requests
            
            url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"
            querystring = {"key" : key}
            
            resp = requests.post( url, data=payload, headers=GLOBAL_HEADERS, params=querystring )
            logging.info( resp.text )
        except :
            logging.error( sys._getframe().f_code.co_name, exc_info=True )
    
    @timeout( 30 )
    def notification_wechat_work_markdown ( message: str, key: str ) -> json :
        '''
        
        :param message:
        :param key:
        :return:
        '''
        try :
            return notification_wechat_work( message_builder.markdown( message ), key )
        except :
            logging.error( sys._getframe().f_code.co_name, exc_info=True )

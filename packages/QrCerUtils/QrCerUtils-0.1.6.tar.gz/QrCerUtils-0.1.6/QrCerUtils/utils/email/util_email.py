# -*- coding: utf-8 -*-
# @Time    : 2019/11/21 14:52
# @Author  : Dong Qirui
# @Software: PyCharm

import logging

from QrCerUtils.decorators.timeout.decorator_timeout import timeout


@timeout( 30 )
def send_email ( subject: str, body: str, to_recipients: list = ['DongQiRui001@Ke.com'], cc_recipients: list = [] ) :
    '''
    发送邮件，有明文密码，代码不可泄漏
    :return:
    '''
    try :
        from exchangelib import DELEGATE, Account, Credentials, Configuration, NTLM, Message, Mailbox, HTMLBody
        from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
        
        BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
        cred = Credentials( r'LianJia\DongQiRui001', 'password' )
        config = Configuration( server='Mail.ke.com', credentials=cred, auth_type=NTLM )
        account = Account( primary_smtp_address='DongQiRui001@Ke.com', config=config, autodiscover=False, access_type=DELEGATE )
        message = Message(
                account=account,
                folder=account.sent,
                subject=subject,
                body=HTMLBody( body ),
                to_recipients=map( lambda x : Mailbox( email_address=x ), to_recipients ) if None is not to_recipients and len( to_recipients ) > 0 else [],
                cc_recipients=map( lambda x : Mailbox( email_address=x ), cc_recipients ) if None is not cc_recipients and len( cc_recipients ) > 0 else []
                )
        message.send_and_save()
    except :
        logging.error( sys._getframe().f_code.co_name, exc_info=True )
        return None

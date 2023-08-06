# -*- coding: utf-8 -*-
# @Time    : 2019/08/24 01:41
# @Author  : Dong Qirui
# @FileName: wechat_work_builder.py
# @Software: PyCharm
import json
import logging
from typing import List


class message_builder() :
    
    def __init__ ( self ) :
        pass
    
    class Constants() :
        MESSAGE_TYPE = 'msgtype'
        MESSAGE_TYPE_TEXT = 'text'
        MESSAGE_TYPE_MARKDOWN = 'markdown'
        MESSAGE_TYPE_IMAGE = 'image'
        MESSAGE_TYPE_NEWS = 'news'
        MESSAGE_CONTENT = 'content'
    
    @staticmethod
    def text ( message_text_content: str, message_text_mentioned_list: list = None, message_text_mentioned_mobile_list: list = None ) -> json :
        '''
        构建文本内容
        :param message_text_content:
        :param message_text_mentioned_list:
        :param message_text_mentioned_mobile_list:
        :return:
        '''
        if len( message_text_content ) > 2048 :
            logging.error( '文本内容，最长不超过2048个字节，必须是utf8编码' )
        message = json.dumps(
                {
                        message_builder.Constants.MESSAGE_TYPE      : message_builder.Constants.MESSAGE_TYPE_TEXT,
                        message_builder.Constants.MESSAGE_TYPE_TEXT : {
                                message_builder.Constants.MESSAGE_CONTENT : message_text_content, 'mentioned_list' : message_text_mentioned_list,
                                'mentioned_mobile_list'                   : message_text_mentioned_mobile_list
                                }
                        } )
        return message
    
    @staticmethod
    def markdown ( message_markdown_content: str ) -> json :
        '''
        构建MarkDown内容
        :param message_markdown_content: markdown内容，最长不超过4096个字节，必须是utf8编码
        :return:
        '''
        message = json.dumps( {
                message_builder.Constants.MESSAGE_TYPE          : message_builder.Constants.MESSAGE_TYPE_MARKDOWN,
                message_builder.Constants.MESSAGE_TYPE_MARKDOWN : {message_builder.Constants.MESSAGE_CONTENT : message_markdown_content}
                } )
        return message
    
    @staticmethod
    def image ( message_image_base64: str, message_image_md5: str ) -> json :
        '''
        构建图片内容
        :param message_image_base64: 图片内容的base64编码, 图片（base64编码前）最大不能超过2M，支持JPG,PNG格式
        :param message_image_md5: 图片内容（base64编码前）的md5值
        :return:
        '''
        message = json.dumps( {
                message_builder.Constants.MESSAGE_TYPE       : message_builder.Constants.MESSAGE_TYPE_IMAGE,
                message_builder.Constants.MESSAGE_TYPE_IMAGE : {'base64' : message_image_base64, 'md5' : message_image_md5}
                } )
        return message
    
    @staticmethod
    def news ( message_news_articles: List[dict] ) -> json :
        '''
        构建图文内容
        :param message_news_articles: 图文消息，一个图文消息支持1到8条图文
        :return:
        '''
        message = json.dumps(
                {message_builder.Constants.MESSAGE_TYPE : message_builder.Constants.MESSAGE_TYPE_NEWS, message_builder.Constants.MESSAGE_TYPE_NEWS : {'articles' : message_news_articles}} )
        return message
    
    @staticmethod
    def news_article ( title: str, url: str = '', description: str = None, picurl: str = None ) -> dict :
        '''
        构建图文新闻
        :param title: 标题，不超过128个字节，超过会自动截断
        :param url: 点击后跳转的链接。
        :param description: 描述，不超过512个字节，超过会自动截断
        :param picurl: 图文消息的图片链接，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150。
        :return:
        '''
        url = 'family.ke.com' if None is url or '' == url else url
        article = {'title' : title, 'url' : url, 'description' : description, 'picurl' : picurl}
        return article
    
    @staticmethod
    def markdown_merge ( request_json: str, applicationName: str ) -> json :
        '''
    
        :param request_json:
        :return:
        '''
        if 'merge_request' == request_json['object_kind'] :
            name_operator = request_json['user']['name']
            username_operator = request_json['user']['username']
            merge_status = request_json['object_attributes']['merge_status']
            state = request_json['object_attributes']['state']
            title = request_json['object_attributes']['title']
            description = request_json['object_attributes']['description']
            source_branch = request_json['object_attributes']['source_branch']
            target_branch = request_json['object_attributes']['target_branch']
            name_assignee = request_json['assignee']['name'] if 'assignee' in request_json and 'name' in request_json['assignee'] else '无'
            username_assignee = request_json['assignee']['username'] if 'assignee' in request_json and 'username' in request_json['assignee'] else None
            target_branch_translate = {
                    'dev'    : '<font color=\"info\">dev</font>',
                    'master' : '<font color=\"red\">master (请谨慎合入)</font>',
                    }.get( target_branch, target_branch )
            url = request_json['object_attributes']['url']
            action = request_json['object_attributes'].get( 'action', 'modify' )
            action_translate = {
                    'open'   : '<font color=\"info\">发起</font>',
                    'close'  : '<font color=\"warning\">关闭</font>',
                    'update' : '<font color=\"warning\">更新</font>',
                    'modify' : '<font color=\"warning\">操作</font>',
                    'merge'  : '<font color=\"red\">合入</font>'
                    }.get( action )
            str_markdown = '''
\r\n### **{name_operator}**{action_translate}了一个Code Review
\r\n##### <font color=\"comment\">主要描述: </font>{title}
\r\n###### <font color=\"comment\">详细内容: </font>{description}
\r\n###### <font color=\"comment\">来源分支: </font>{source_branch}
\r\n###### <font color=\"comment\">目标分支: </font>{target_branch_translate}
\r\n###### <font color=\"comment\">评审指派: </font>{name_assignee}
\r\n###### <font color=\"comment\">访问地址: </font>[点我访问]({url})
            '''.format( name_operator=name_operator, title=title, merge_status=merge_status, url=url, target_branch_translate=target_branch_translate, action=action,
                        action_translate=action_translate, description='\r\n' + description if description.__contains__( '-' ) or description.__contains__( '#' ) else description,
                        source_branch=source_branch, name_assignee=name_assignee )
            if (applicationName == 'Application_Layer') and (title.__contains__( '000' ) or description.__contains__( '000' )) :
                str_markdown += '\r\n###### 如果包含接口配置更新，请及时通知QA同学添加TestCase进行测试，并于封板前同步线上策略规则！'
            
            return message_builder.markdown( str_markdown )

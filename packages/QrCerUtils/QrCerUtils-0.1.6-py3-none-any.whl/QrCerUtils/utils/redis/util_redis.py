# -*- coding: utf-8 -*-
# @Time    : 2019/11/21 14:56
# @Author  : Dong Qirui
# @Software: PyCharm


from QrCerUtils.utils import getTodayDateStrftimeShort


class redis_instance() :
    
    def __init__ ( self ) :
        import redis
        
        # self.redis_instance = redis.StrictRedis( host='127.0.0.1', port=6379, password='', db=0 )
        self.redis_instance = redis.StrictRedis( host='127.0.0.1', port=6379, password='password', db=0 )
    
    def instance ( self ) :
        '''
        
        :return:
        '''
        return self.redis_instance
    
    def hash_get ( self, key: str, field: str ) -> str :
        '''
        
        :param key:
        :param field:
        :return:
        '''
        return self.redis_instance.hget( key, field )
    
    def hash_exists_robot ( self, field: str ) -> str :
        '''
        
        :param field:
        :return:
        '''
        return self.redis_instance.hexists( self.KEY_BASE, field )
    
    def hash_get_robot ( self, field: str ) -> str :
        '''
        
        :param key:
        :param field:
        :return:
        '''
        return self.redis_instance.hget( self.KEY_BASE, field )
    
    def hash_set_robot ( self, field: str, value: str ) -> str :
        '''
        
        :param key:
        :param field:
        :return:
        '''
        return self.redis_instance.hset( self.KEY_BASE, field, value )
    
    def redis_hash_get_robot_daily ( self, field: str ) -> str :
        '''
        
        :param key:
        :param field:
        :return:
        '''
        date_str = getTodayDateStrftimeShort()
        return self.redis_instance.hget( self.KEY_BASE, '{date}_{field}'.format( date=date_str, field=field ) )
    
    def hash_exists_robot_daily ( self, field: str ) -> str :
        '''
        
        :param key:
        :param field:
        :return:
        '''
        date_str = getTodayDateStrftimeShort()
        return self.redis_instance.hexists( self.KEY_BASE, '{date}_{field}'.format( date=date_str, field=field ) )

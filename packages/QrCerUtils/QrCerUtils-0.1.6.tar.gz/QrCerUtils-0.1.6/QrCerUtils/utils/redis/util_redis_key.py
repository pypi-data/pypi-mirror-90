# -*- coding: utf-8 -*-
# @Time    : 2019-01-03 16:29
# @Author  : Dong Qirui
# @FileName: keyscan.py.py
# @Software: PyCharm


import argparse
import optparse
import re
import sys

import redis


class Counter( object ) :
    
    def __init__ ( self, host, port, password=None, db=0, sample_rate=1.0 ) :
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.limit = 0
        self.sample_rate = min( max( sample_rate, 0.1 ), 1.0 )
        self._setup_()
        self._info_()
        self._run_()
        self.show()
    
    def _setup_ ( self ) :
        try :
            self.conn = redis.StrictRedis( host=self.host, port=self.port, password=self.password, db=self.db )
            self.db_size = self.conn.dbsize()
            self.limit = int( self.sample_rate * self.db_size )
            self.pipeline = self.conn.pipeline()
            self.iter_counts = 0
            self.result = dict()
            self.pattern = re.compile( '((\D+)((_\d*)+))' )
            if self.limit <= 0 :
                print( 'Count is zero, exit now.' )
        except Exception as e :
            print( repr( e ) )
            sys.exit( 0 )
    
    def _info_ ( self ) :
        print( 'INFO {0}:{1}'.format( 'host', self.host ) )
        print( 'INFO {0}:{1}'.format( 'port', self.port ) )
        print( 'INFO {0}:{1}'.format( 'password', self.password[:2] + '*' ) )
        print( 'INFO {0}:{1}'.format( 'db', self.db ) )
        print( 'INFO {0}:{1}'.format( 'sample_rate', self.sample_rate ) )
    
    def _run_ ( self ) :
        print( 'PROCESS start.' )
        for key in self.conn.scan_iter( match='*', count=100000 ) :
            self.iter_counts += 1
            if self.iter_counts % 10000 == 0 :
                print( '{0}%'.format( round( 100.0 * self.iter_counts / self.limit ) ) )
            if self.iter_counts >= self.limit :
                return
            try :
                grp = re.search( self.pattern, key )
                if None != grp :
                    prefix = re.search( self.pattern, key ).groups()[1]
                    if prefix in self.result :
                        self.result[prefix] += 1
                    else :
                        self.result[prefix] = 1
            except Exception as e :
                print( repr( e ) )
                sys.exit( 0 )
        print( 'PROCESS end.' )
    
    def show ( self ) :
        print( ''.join( map( lambda e : '{0}\t{1}\n'.format( e[0], e[1] ), self.result.items() ) ) )


def main () :
    usage = '''Usage: %prog [options] arg1 arg2 ...
    
    用于统计Redis中Key的计数
    count key in redis...
    
    EXAMPLE: python redis_key_util.py --host 10.33.108.52 --port 6379 -d 0 -a $password
    使用示例：python redis_key_util.py --host 10.33.108.52 --port 6379 -d 0 -a $password
    '''
    epilog = """

    """
    if sys.version_info > (2, 7) :
        parser = optparse.OptionParser( usage=usage, epilog=epilog, version='%prog 1.0' )
        parser.add_option( '--host', dest='host', help='host of the redis server' )
        parser.add_option( '--port', dest='port', type=int, help='port of the redis server' )
        parser.add_option( '-d', type=int, dest='db', help='the database, which default is 0' )
        parser.add_option( '-a', dest='password', help='the password, which default is None, if the redis server ask for authentication' )
        parser.add_option( '-s', dest='sample_rate', help='the sample size, which default is 1.0, means all of the db_size' )
        (options, args) = parser.parse_args()
        if None == options.host :
            parser.error( 'Parameter %s required' % 'host' )
        if None == options.port :
            parser.error( 'Parameter %s required' % 'port' )
    else :
        parser = argparse.ArgumentParser( usage='用于统计Redis中Key的计数', description='this script sample and analyze the key counts of the redis server, group by common key prefix', epilog=epilog,
                                          formatter_class=argparse.RawTextHelpFormatter, add_help=True )
        parser.add_argument( '--host', help='host of the redis server' )
        parser.add_argument( '--port', type=int, help='port of the redis server' )
        parser.add_argument( '-d', type=int, dest='db', help='the database, which default is 0' )
        parser.add_argument( '-a', dest='password', help='the password, which default is None, if the redis server ask for authentication' )
        parser.add_argument( '-s', type=float, dest='sample_rate', help='the sample size, which default is 1.0, means all of the db_size' )
        options = parser.parse_args()
        args = parser.parse_args()
    print( options.host, options.port, options.db, options.password, options.sample_rate )
    Counter( options.host, options.port, password=options.password, sample_rate=options.sample_rate, db=options.db )


if __name__ == '__main__' :
    main()

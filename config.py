import os

SECRET_KEY = os.urandom(24)

# PERMANENT_SESSION_LIFETIME =
# DEBUG = True

'''
下面是mysql数据库的相关配置参数
'''
DB_USERNAME = 'root'
DB_PASSWORD = 'password'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'bbs2'



DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CURRENT_USER_ID = 'asdfsa'

'''
下面是发送各种邮件时使用的发件邮箱的配置
'''
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = '25'
MAIL_USE_SSL = False
MAIL_USE_STL = False
MAIL_USERNAME = '15832217331@163.com'
MAIL_PASSWORD = 'python1023'
MAIL_DEFAULT_SENDER = '15832217331@163.com'

# memcached端口配置
MEMCACHED_PORT = ['127.0.0.1:11211']
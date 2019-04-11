import os

# SECRET_KEY = os.urandom(24)
SECRET_KEY = 'sdafadsfadsfdasfadsfasdf'
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

CURRENT_CMS_USER_ID = 'asdfsa'
CURRENT_FRONT_USER_ID = 'asdafdsfaa'

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

#短信发送端口配置
# 来源： 聚合数据
URL = "http://v.juhe.cn/sms/send"
TPL_ID = "139180"
APP_KEY = "2865efa1d531cb7d4d89ae01e35b5d22"


# 七牛配置参数
QINIU_ACCESS_KEY = '4HWxVDyK0vTnD0EqjT0FV4kk8dXz2Jy6GkTMfbCs'
QINIU_SECRET_KEY = 'qKAAwuZTpBUD7V56VQNBbi3eZDKQhnV5nOkDeSOq'
QINIU_BUCKET_NAME = 'bbs2'
QINIU_DOMAIN = 'http://podxcwazy.bkt.clouddn.com/'


# ueditor 配置参数
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = QINIU_ACCESS_KEY
UEDITOR_QINIU_SECRET_KEY = QINIU_SECRET_KEY
UEDITOR_QINIU_BUCKET_NAME = QINIU_BUCKET_NAME
UEDITOR_QINIU_DOMAIN = QINIU_DOMAIN

# flask-pagintation 分页配置
PER_PAGE = 10

# 默认头像七牛存储链接
DEFAULT_AVATAR = 'http://podxcwazy.bkt.clouddn.com/avatar_default.jpg'
'''
该文件为一些工具函数, 包括一些装饰器
'''
from .models import CMSUser, db
from .views import session, redirect, url_for, g
from functools import wraps
import config
from exts import Message
import random


def login_check(email, password):
    '''
    登录验证
    :param email: 用户邮箱
    :param password: 用户密码
    :return: 用户名和密码匹配则返回用户作为当前用户, 不一致则返回相应的错误信息
    '''
    user = db.session.query(CMSUser).filter_by(email=email).one_or_none()
    if user:
        if user.check_password(raw_password=password):
            return None, user
        else:
            return '密码错误！', None
    else:
        return '用户不存在！', None


def login_required(func):
    '''
    登录需求装饰器, 对于某些页面, 要求登录后才能访问, 则在视图函数前加上此装饰器
    实现原理为检查session中是否存在当前用户ID, 存在则返回当前函数, 不存在则返回登录页面, 并设置onlogin为true
    :param func:
    :return:
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get(config.CURRENT_CMS_USER_ID):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login', onlogin=True))

    return wrapper


def authority_required(authority):
    '''
     权限需求装饰器, 对于某些页面, 无相关权限禁止访问, 跳转回首页
     注意这是一个带参数的装饰器
    :param authority: 需求的权限
    :return:
    '''
    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if g.cuser.check_authority(authority):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.home', noauthority=True))
        return wrapper
    return outer


def search_user_by_id(id):
    user = db.session.query(CMSUser).filter_by(id=id).one()
    return user


def update_user(user, name=None, password=None, phone=None, email=None):
    '''
    更新用户信息, 用于修改密码\邮箱等
    :param user:
    :param name:
    :param password:
    :param phone:
    :param email:
    :return:
    '''
    if name:
        user.name = name
    if password:
        user.password = password
    if phone:
        user.phone = phone
    if email:
        user.email = email
    db.session.commit()


def create_captcha_email(*recipients):
    '''
    生成验证码与邮件内容
    验证码: 先生成0~9的数字列表, 转换为字符串, 然后随机取4个join在一起即可
    邮箱内容: 需要生成一个Message对象, 包括主题(subject), 内容(body), sender(发送者), recipients(接收者)
    :param recipients: 接收邮箱列表
    :return: 返回一个Message对象准备发送, 并返回一个验证码
    '''
    captcha = list(range(10))
    captcha = map(lambda x:str(x), captcha)
    captcha = ''.join(random.sample(list(captcha), 4))
    # captcha = ''.join(random.sample(list(map(lambda x:str(x), list(range(10)))), 4))
    subject = '豌豆论坛验证码'
    body = '您正在豌豆论坛注册邮箱，验证码为：\n' + captcha + '\n该验证码5分钟内有效！'
    sender = config.MAIL_USERNAME
    recipients = list(recipients)

    msg = Message(subject=subject, body=body, sender=sender, recipients=recipients)

    return msg, captcha




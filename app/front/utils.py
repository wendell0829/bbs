from .models import FrontUser, db
from functools import wraps
import config
from flask import session, redirect, url_for


def add_front_user(username, password, mobile):
    user = FrontUser(username=username, password=password, mobile=mobile)

    db.session.add(user)
    db.session.commit()

    print(user.id)
    return user


def check_mobile(mobile):
    user = FrontUser.query.filter_by(mobile=mobile).one_or_none()
    if user:
        return True
    else:
        return False


def login_required(func):
    '''
    登录需求装饰器, 对于某些页面, 要求登录后才能访问, 则在视图函数前加上此装饰器
    实现原理为检查session中是否存在当前用户ID, 存在则返回当前函数, 不存在则返回登录页面, 并设置onlogin为true
    :param func:
    :return:
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get(config.CURRENT_FRONT_USER_ID):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('front.signin', onlogin=True))

    return wrapper


def search_user_by_id(user_id):
    user = FrontUser.query.filter_by(id=user_id).one()
    return user
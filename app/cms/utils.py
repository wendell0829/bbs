from .models import CMSUser, db
from .views import session, redirect, url_for
from functools import wraps
import config
from exts import Message
import random


def login_check(phone, password):
    user = db.session.query(CMSUser).filter_by(phone=phone).one_or_none()
    if user:
        if user.check_password(raw_password=password):
            return None, user
        else:
            return '密码错误！', None
    else:
        return '用户不存在！', None


def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get(config.CURRENT_USER_ID):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login', onlogin=True))

    return wrapper


def search_user_of_id(id):
    user = db.session.query(CMSUser).filter_by(id=id).one()
    return user


def update_user(user, name=None, password=None, phone=None, email=None):
    if name:
        user.name = name
    if password:
        user.password = password
    if phone:
        user.phone = phone
    if email:
        user.email = email
    db.session.commit()


def create_captcha(*recipients):
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




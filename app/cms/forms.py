'''
该文件为cms界面的表单验证代码
'''
from ..forms import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length, Regexp, EqualTo, Email, ValidationError
from .views import g
from utils import cache


class LoginForm(BaseForm):
    '''

    '''
    email_rule = r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$'
    email = StringField(validators=[Regexp(regex=email_rule, message='请输入正确格式的邮箱!')])
    password = StringField(validators=[InputRequired(message='请输入密码！'),
                                       Length(min=6, max=16, message='密码格式有错误！')])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[InputRequired(message='请输入旧密码！'),
                                     Length(min=6, max=16, message='旧密码格式有错误！')])
    newpwd = StringField(validators=[InputRequired(message='请输入新密码！'),
                                     Length(min=6, max=16, message='新密码格式有错误！')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='两次输入的密码不一致！')])

    def validate_newpwd(self, field):
        if field.data == self.oldpwd.data:
            raise ValidationError(message='新旧密码相同！')


class ResetEmailForm(BaseForm):
    email = StringField(validators=[InputRequired(message='请输入新邮箱！'),
                                    Email(message='邮箱格式不正确！')])
    captcha = StringField(validators=[InputRequired(message='请输入验证码！')])

    def validate_email(self, field):
        email = field.data
        user = g.user
        if user.email == email:
            raise ValidationError('新邮箱不可以与现有邮箱相同！')


    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        if captcha != cache.get(email):
            raise ValidationError('验证码错误!')




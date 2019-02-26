from ..forms import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, ValidationError
from .views import g
from utils import cache


class LoginForm(BaseForm):
    phone_rule = r'1[3-9]\d{9}'
    phone = StringField(validators=[DataRequired(message='请输入手机号码！'),
                                    Regexp(phone_rule, message='手机号码格式不正确！')])
    password = StringField(validators=[DataRequired(message='请输入密码！'),
                                       Length(min=6, max=16, message='密码格式有错误！')])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[DataRequired(message='请输入旧密码！'),
                                     Length(min=6, max=16, message='旧密码格式有错误！')])
    newpwd = StringField(validators=[DataRequired(message='请输入新密码！'),
                                     Length(min=6, max=16, message='新密码格式有错误！')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='两次输入的密码不一致！')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[DataRequired(message='请输入新邮箱！'),
                                    Email(message='邮箱格式不正确！')])
    captcha = StringField(validators=[DataRequired(message='请输入验证码！')])

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




from ..forms import BaseForm
from wtforms import StringField
from wtforms.validators import Regexp, EqualTo, InputRequired, Length,ValidationError
from utils import cache
from .models import FrontUser, db

class SingupForm(BaseForm):
    # 注册验证表单
    mobile_rule = r'^1[3-9]\d{9}$'

    # 基本验证器验证
    mobile = StringField(validators=[InputRequired(message='请输入手机号码！'),
                                    Regexp(mobile_rule, message='手机号码格式不正确！')])
    password1 = StringField(validators=[InputRequired(message='请输入密码！'),
                                       Length(min=6, max=16, message='密码长度需要在6-16位之间！')])
    password2 = StringField(validators=[EqualTo('password1', message='两次输入的密码不一致！')])
    username = StringField(validators=[InputRequired(message='请输入昵称！'),
                                       Length(max=10, message='昵称需要在10位以内！')])
    img_captcha = StringField(validators=[InputRequired(message='请输入图形验证码！')])
    sms_captcha = StringField(validators=[InputRequired(message='请输入短信验证码！')])


    # 自定义附加验证
    def validate_img_captcha(self, field):
        img_captcha = field.data.lower()
        if img_captcha != '1111':
            if not cache.get(img_captcha):
                raise ValidationError(message='图形验证码不正确！')


    def validate_sms_captcha(self, field):
        sms_captcha = field.data.lower()
        # mobile = self.mobile.data
        if sms_captcha != '1111':
            if sms_captcha != cache.get(self.mobile.data.strip()):
                raise ValidationError(message='短信验证码不正确！')


class SigninForm(BaseForm):
    # 登录验证表单
    mobile_rule = r'^1[3-9]\d{9}$'

    # 一般验证器
    mobile = StringField(validators=[InputRequired(message='请输入手机号码！'),
                                     Regexp(mobile_rule, message='手机号码格式不正确！')])
    password = StringField(validators=[InputRequired(message='请输入密码！'),
                                        Length(min=6, max=16, message='密码长度需要在6-16位之间！')])
    remember = StringField()
    img_captcha = StringField(validators=[InputRequired(message='请输入图形验证码！')])

    # 自定义附加验证
    def validate_img_captcha(self, field):
        img_captcha = field.data.lower()
        if img_captcha != '1111':
            if not cache.get(img_captcha):
                raise ValidationError(message='图形验证码不正确！')


    # 重载validate函数， 完全自定义验证
    def validate(self):
        # 注意由于上面两种方法的验证最后都是被validate方法实现的
        # 所以这里需要先用super引用原validate方法对上面已有的验证器进行验证
        # 否则上面已有的验证器不会起作用
        if not super(SigninForm,self).validate():
            return False

        mobile = self.mobile.data
        password = self.password.data

        user = FrontUser.query.filter_by(mobile=mobile).one_or_none()

        if user:
            if user.check_password(password):
                return user
            else:
                self.password.errors.append('密码错误！')
                return False
        else:
            self.mobile.errors.append('该手机号未注册！')
            return False


class AvatarForm(BaseForm):
    avatar = StringField(InputRequired(message='请上传头像！'))

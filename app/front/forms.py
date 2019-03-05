from ..forms import BaseForm
from wtforms import StringField
from wtforms.validators import Regexp, EqualTo, DataRequired, Length,ValidationError
from utils import cache

class SingupForm(BaseForm):
    mobile_rule = r'^1[3-9]\d{9}$'
    mobile = StringField(validators=[DataRequired(message='请输入手机号码！'),
                                    Regexp(mobile_rule, message='手机号码格式不正确！')])
    password1 = StringField(validators=[DataRequired(message='请输入密码！'),
                                       Length(min=6, max=16, message='密码长度需要在6-16位之间！')])
    password2 = StringField(validators=[EqualTo('password1', message='两次输入的密码不一致！')])
    username = StringField(validators=[DataRequired(message='请输入昵称！'),
                                       Length(max=10, message='昵称需要在10位以内！')])
    img_captcha = StringField(validators=[DataRequired(message='请输入图形验证码！')])
    sms_captcha = StringField(validators=[DataRequired(message='请输入短信验证码！')])


    def validate_img_captcha(self, field):
        img_captcha = field.data.lower()
        if not cache.get(img_captcha):
            raise ValidationError(message='图形验证码不正确！')


    def validate_sms_captcha(self, field):
        sms_captcha = field.data.lower()
        # mobile = self.mobile.data
        print(self.mobile.data)
        if sms_captcha != cache.get(self.mobile.data.strip()):
            raise ValidationError(message='短信验证码不正确！')



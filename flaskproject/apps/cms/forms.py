from wtforms import StringField,IntegerField,ValidationError
from wtforms.validators import Email,InputRequired,Length,equal_to
from apps.forms import BaseForm
from utils import zlcache
from flask import g

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='邮箱格式不正确')])
    password = StringField(validators=[Length(6,20,message='请输入6-20位密码')])
    remember = IntegerField()


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message='请输入6-20位密码')])
    newpwd = StringField(validators=[Length(6,20,message='请输入6-20位密码')])
    newpwd2 = StringField(validators=[equal_to('newpwd', message='两次密码不相等')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式邮箱！ ')])
    captcha = StringField(validators=[Length(max=6,min=6, message='请输入正确长度验证码！ ')])
    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_cache = zlcache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('验证码错误！ ')

    def validate_email(self,field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('不能修改为相同的邮箱! ')
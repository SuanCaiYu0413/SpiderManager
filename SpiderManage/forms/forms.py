#encoding: utf-8

from wtforms import StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo,DataRequired
from base_forms import BaseForm


class AddForm(BaseForm):
    host_name = StringField(validators=[DataRequired(message='请输入主机')])
    ip_address = StringField(validators=[DataRequired(message='请输入IP')])
    port_num = StringField(validators=[DataRequired(message='请输入端口号')])

class UpdateForm(BaseForm):
    host_name = StringField(validators=[DataRequired(message='请输入主机')])
    ip_address = StringField(validators=[DataRequired(message='请输入IP')])
    port_num = StringField(validators=[DataRequired(message='请输入端口号')])
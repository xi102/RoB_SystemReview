"""
表单类
"""

from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required
from flask_wtf import FlaskForm


# 登录表单
class Login_Form(FlaskForm):
    username = StringField('用户名:', validators=[Required()])
    password = PasswordField('密码:', validators=[Required()])
    submit = SubmitField('登录')


# 注册表单
class Register_Form(FlaskForm):
    username = StringField('用户名:', validators=[Required()])
    password = PasswordField('密码:', validators=[Required()])
    phone=StringField('电话：',validators=[Required()])
    email=StringField('Email:',validators=[Required()])
    name=StringField('姓名：',validators=[Required()])
    organization=StringField('所属单位：',validators=[Required()])
    submit = SubmitField('注册')

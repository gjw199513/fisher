# -*- coding:utf-8 -*-
from wtforms import Form, PasswordField, StringField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

from app.models.user import User

__author__ = 'gjw'
__date__ = '2018/5/13 20:50'


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])


class RegisterForm(EmailForm):
    nickname = StringField('昵称', validators=[
        DataRequired(), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])

    password = PasswordField('密码', validators=[
        DataRequired(message='密码不可以为空，请输入你的密码')])

    def validate_email(self, field):
        # db.session()
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("电子邮件已被注册")

    def validate_nickname(self, field):
        # db.session()
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError("昵称已存在")


class LoginForm(EmailForm):
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不可以为空，请输入你的密码')])



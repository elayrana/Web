from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     ValidationError)
from wtforms.validators import Email, EqualTo, Length, Regexp, Required

from ..models import Users


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[
        Required(), Length(3, 64), Regexp('^[A-Za-z][A-Za-z0-9._]*$', 0,
                                          'Username must have only letters'
                                          'numbers dot and underscore and '
                                          'must start with a letter')],
        render_kw={"placeholder": "Username"})
    name = StringField('Name', validators=[Required(), Regexp('^[A-Za-z]')],
                       render_kw={"placeholder": "Name"})
    surname = StringField('Surname', validators=[Required(),
                          Regexp('^[A-Za-z]')],
                          render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[Required(), Email()],
                        render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[
        Required(), EqualTo('confirm', message='Passwords must match')],
        render_kw={"placeholder": "Password"})
    confirm = PasswordField('Confirm password', validators=[Required()],
                            render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exist')

    def validate_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exist')


class LogInForm(FlaskForm):
    username = StringField('Type your username/email', validators=[Required()])
    password = PasswordField('Type your password', validators=[Required()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import Required, Email, EqualTo, Regexp, Length
from ..models import Users
from flask_login import current_user


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[
        Required(), Length(3, 64), Regexp('^[A-Za-z][A-Za-z0-9._]*$', 0,
                                          'Username must have only letters'
                                          'numbers dot and underscore and '
                                          'must start with a letter')])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Type your password', validators=[
        Required(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm your password', validators=[Required()])
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
    submit = SubmitField('Submit')


class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[Required()])
    new_password = PasswordField('New password', validators=[
        Required(), EqualTo('confirm', message='Password must match')])
    confirm = PasswordField('New password', validators=[Required()]) 
    submit = SubmitField('Submit')

    def validate_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('This is not ypur password')

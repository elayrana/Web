from ..models import Roles, Users
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (StringField, PasswordField, SubmitField,
                     ValidationError, TextAreaField, BooleanField, SelectField)
from wtforms.validators import DataRequired, EqualTo, Length


class ChangePassForm(FlaskForm):
    current_pass = PasswordField('Current Password', validators=[
        DataRequired], render_kw={"placeholder": "Current Password"})
    new_password = PasswordField('New Password', validators=[
        DataRequired, EqualTo('confirm', message='Passwords must match')],
        render_kw={"placeholder": "New Password"})
    confirm = PasswordField('Confirm password', validators=[DataRequired],
                            render_kw={"placeholder": "Confirm New Password"})
    submit = SubmitField('Change Password')

    @staticmethod
    def validate_current_pass(field):
        if not current_user or not \
         current_user.verify_password(field.data):
                raise ValidationError('The current password is incorrect')


class ChangeProfileForm(FlaskForm):
    name = StringField('Name', validators=[Length(0, 64)],
                       render_kw={"placeholder": "Nombre"})
    surname = StringField('Surname', validators=[Length(0, 64)],
                          render_kw={"placeholder": "Apellidos"})
    location = StringField("Location", validators=[Length(0, 64)],
                           render_kw={"placeholder": "Location"})
    about_me = TextAreaField('About_ me', render_kw={"placeholder": "About me"})
    submit = SubmitField('Update profile')


class AdminChangeProfile(FlaskForm):
    username = StringField('Username, validators')
    name = StringField('Name', validators=[Length(0, 64)],
                       render_kw={"placeholder": "Nombre"})
    surname = StringField('Surname', validators=[Length(0, 64)],
                          render_kw={"placeholder": "Apellidos"})
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    location = StringField("Location", validators=[Length(0, 64)],
                           render_kw={"placeholder": "Location"})
    about_me = TextAreaField('About_ me', render_kw={"placeholder": "About me"})

    submit = SubmitField('Update profile')

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Roles.query.order_by(Roles.name).all()]

    @staticmethod
    def validate_email(field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exist')

    @staticmethod
    def validate_username(field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exist')

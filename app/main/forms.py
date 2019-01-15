
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import Required, EqualTo, Length


class ChangePassForm(FlaskForm):
    current_pass = PasswordField('Current Password', validators=[
        Required()], render_kw={"placeholder": "Current Password"})
    new_password = PasswordField('New Password', validators=[
        Required(), EqualTo('confirm', message='Passwords must match')],
        render_kw={"placeholder": "New Password"})
    confirm = PasswordField('Confirm password', validators=[Required()],
                            render_kw={"placeholder": "Confirm New Password"})
    submit = SubmitField('Change Password')

    def validate_current_pass(self, field):
        if not current_user or not \
         current_user.verify_password(field.data):
                raise ValidationError('The current password is incorrect')


class ChangeProfileForm(FlaskForm):
    name = StringField('Name', validators=[Length(0, 64)],
                       render_kw={"placeholder": "Nombre"})
    surname = StringField('Surname', validators=[Length(0, 64)],
                           render_kw={"placeholder": "Apellidos"})
    location = StringField("Location", validators=[Length(0,64)],
                           render_kw={"placeholder": "Location"})
    about_me = TextAreaField('About_ me', render_kw={"placeholder": "About me"})
    submit = SubmitField('Update profile')

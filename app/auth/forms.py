from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Required, Email, EqualTo


class SignUpForm(FlaskForm):
    username = StringField('Type the username', validators=[Required()])
    email = StringField('Type your email', validators=[Required(), Email()])
    password = PasswordField('Type your password',
                             validators=[Required()])
    confirmed = PasswordField('Confirm your password',
                              validators=[Required(), EqualTo(password)])

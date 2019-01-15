from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user

from app import db
from app.decorators import admin_required, permission_required
from app.main import main
from app.auth.forms import SignUpForm
from app.email import send_mail
from app.models import Users, Permissions
from app.main.forms import ChangePassForm, ChangeProfileForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = SignUpForm()
    if form.validate_on_submit():
        print("Hola")
        user = Users(username=form.username.data,
                     name=form.name.data,
                     surname=form.name.data,
                     email=form.email.data,
                     password=form.password.data)

        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(user.email, 'Confirm Your Account',
                  'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form)


@main.route('/user/<username>')
@login_required
def user_profile(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    if user.username != current_user.username:
        abort(403)
    return render_template('user_profile.html', user=user)


@main.route('/user/<username>/password', methods=['GET', 'POST'])
@login_required
def change_password(username):

    form = ChangePassForm()
    if form.validate_on_submit():
        return redirect(url_for('main.index'))
    return render_template('change_password.html', form=form)


@main.route('/user/<username>/profile', methods=['GET', 'POST'])
@login_required
def change_profile(username):

    form = ChangeProfileForm()
    
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        user = current_user._get_current_object
        print('user')
        return redirect(url_for('main.index'))
    form.name.data = current_user.name
    form.surname.data = current_user.surname
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('change_profile.html', form=form)


@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return "For administrators"


@main.route('/moderator')
@login_required
@permission_required(permission=Permissions.MODERATE_COMENTS)
def for_moderator_only():
    return "For moderators"

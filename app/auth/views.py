from flask import render_template, redirect, url_for, flash
from . import auth
from .forms import SignUpForm, LogInForm
from ..models import Users
from .. import db
from flask_login import login_user, logout_user, login_required


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data,
                     email=form.email.data,
                     password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Yocan now log In', 'information')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.username.data).first() or\
               Users.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me)
            return redirect(url_for('main.index'))
        flash('User or password incorrect', 'error')
    return render_template('/auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been log out', 'information')
    return redirect(url_for('main.index'))

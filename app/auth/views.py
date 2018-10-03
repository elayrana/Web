from flask import render_template, flash
from . import auth
from .forms import SignUpForm
from .. import db
from sqlalchemy import exc


@auth.route('/singup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            pass
        except exc.IntegrityError:
            pass


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('/auth/login.html')

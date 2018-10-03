from flask import render_template
from . import auth
from .forms import SignUp


@auth.route('/singup', methods=['GET', 'POST'])
def signup():
    pass


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('/auth/login.html')

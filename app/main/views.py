from flask import render_template, abort
from flask_login import login_required, current_user

from app.decorators import admin_required, permission_required
from app.main import main
from app.models import Users, Permissions


@main.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


@main.route('/user/<username>')
def user_profile(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    if user.username != current_user.username:
        abort(403)
    return render_template('user_profile.html', user=user)


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

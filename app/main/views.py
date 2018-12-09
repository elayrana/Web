from flask import render_template
from app.main import main
from flask_login import login_required
from app.models import Permissions
from app.decorators import admin_required, permission_required
@main.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


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

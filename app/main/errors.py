from flask import render_template

from app.main import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@main.app_errorhandler(500)
def internar_server_error(e):
    return render_template('errors/500.html'), 500


@main.app_errorhandler(403)
def page_forbidden(e):
    return render_template('errors/403.html'), 403

from app import create_app


app = create_app('default')


@app.shell_context_processor
def make_shell_context():
    return dict(app=app)

from app import create_app
from app import db
from flask_migrate import Migrate
from app.models import Users, Roles


app = create_app('default')
mograte = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Users=Users, Roles=Roles)

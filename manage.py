import sys

from flask.cli import FlaskGroup

from src import create_app, db
from src.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('seed_db')
def seed_db():
    db.session.add(User(
        username='redninja',
        email='redninja@dojo.com'
    ))
    db.session.add(User(
        username='blueninja',
        email='blueninja@dojo.com'
    ))
    db.session.commit()

if __name__ == '__main__':
    cli()
    



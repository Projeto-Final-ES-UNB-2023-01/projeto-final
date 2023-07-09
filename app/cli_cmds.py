from flask.cli import AppGroup
from .webapp import db
from .models.user import User
from .seed import users

seed_cli = AppGroup('seed')


@seed_cli.command('users')
def seed_users():
    for user in users:
        print(user)
        db.session.add(User(**user))

    db.session.commit()

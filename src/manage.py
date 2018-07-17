import config
from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import logging
from models import db
from tasks.update_from_sirene import update_from_sirene
from tasks.update_from_bce import update_from_bce
from tasks.seed_database_bridge import seed_database_bridge


server = Flask(__name__)
server.debug = config.DEBUG
server.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
db.init_app(server)


migrate = Migrate(server, db)
manager = Manager(server)
manager.add_command('db', MigrateCommand)


@manager.command
def script_update_from_bce():
    update_from_bce()


@manager.command
def script_update_from_sirene():
    update_from_sirene()


@manager.command
def seed():
    seed_database_bridge()


if __name__ == '__main__':
    manager.run()

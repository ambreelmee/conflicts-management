import config
from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import logging
from models import db
from tasks import update_from_bce


server = Flask(__name__)
server.debug = config.DEBUG
server.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
db.init_app(server)

migrate = Migrate(server, db)
manager = Manager(server)
manager.add_command('db', MigrateCommand)


@manager.command
def script_update_from_bce():
    logging.getLogger(__name__)
    update_from_bce()


if __name__ == '__main__':
    manager.run()

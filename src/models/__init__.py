from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from .institution import Institution
from .conflict import Conflict

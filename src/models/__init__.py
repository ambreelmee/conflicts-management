from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from .conflict import Conflict
from .institution import Institution
from .institutionSnapshot import InstitutionSnapshot

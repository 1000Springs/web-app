from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy, Pagination

app = Flask('hotspringsapp')

db = SQLAlchemy(app)

app.config.from_pyfile('hotsprings.cfg')

import hotspringsapp.views
import hotspringsapp.models
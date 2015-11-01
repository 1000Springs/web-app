from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy, Pagination
from flask.ext.cache import Cache 

app = Flask('hotspringsapp')

db = SQLAlchemy(app)

app.config.from_pyfile('hotsprings.cfg')

# Cache for storing data that changes infrequently
# Store objects for a year by default(60 * 60 * 24 * 365 seconds)
app.cache = Cache(app,config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24 * 365})
app.initTaxonomyCacheThreads=0

import hotspringsapp.views
import hotspringsapp.models
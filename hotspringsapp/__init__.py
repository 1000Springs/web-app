from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy, Pagination
from flask.ext.cache import Cache 

app = Flask('hotspringsapp')

db = SQLAlchemy(app)

app.config.from_pyfile('hotsprings.cfg')

# Cache for storing slow to retrieve taxonomy data
# Store objects for a year by default(60 * 60 * 24 * 365 seconds)
cacheBase = '/opt/local/flask-cache/'
app.taxonSummaryCache = Cache(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': cacheBase + 'taxon-summary', 'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24 * 365, 'CACHE_THRESHOLD': 2000})
app.taxonOverviewCache = Cache(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR':  cacheBase + 'taxon-overview', 'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24 * 365})

import hotspringsapp.views
import hotspringsapp.models
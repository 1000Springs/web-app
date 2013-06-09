from flask import Flask


app = Flask('hotspringsapp')

app.config.from_pyfile('hotsprings.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/geothermaldb'

import hotspringsapp.views
import hotspringsapp.models




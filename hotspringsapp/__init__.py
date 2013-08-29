from flask import Flask

app = Flask('hotspringsapp')

app.config.from_pyfile('hotsprings.cfg')

import hotspringsapp.views
import hotspringsapp.models
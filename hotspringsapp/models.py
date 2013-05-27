from flask_sqlalchemy import SQLAlchemy
from hotspringsapp import app

db = SQLAlchemy(app)

class Sample(db.Model):
	SAMPLE_ID = db.Column(db.Integer, primary_key=True)
	date_gathered = db.Column(db.DateTime)
	LOCATION_FEATURE_NC = db.Column(db.String)

	def __init__(self,id,date,location):
		self.SAMPLE_ID = id
		self.date_gathered = date
		self.LOCATION_FEATURE_NC = location
	
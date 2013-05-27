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


class Physical_data(db.Model):
	SAMPLE_ID = db.Column(db.Integer, primary_key=True)
	Phys_ID = db.Column(db.Integer, primary_key=True)
	Temperature = db.Column(db.Float)
	ph_level = db.Column(db.Float)
	redox = db.Column(db.Float)
	dissolved_oxygen = db.Column(db.Float)
	conductivity = db.Column(db.Float)
	date_gathered = db.Column(db.Float)

	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		
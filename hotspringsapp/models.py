from flask_sqlalchemy import SQLAlchemy
from hotspringsapp import app

db = SQLAlchemy(app)

class Sample(db.Model):

	SAMPLE_ID = db.Column(db.Integer, primary_key=True)
	date_gathered = db.Column(db.DateTime)
	LOCATION_FEATURE_NC = db.Column(db.String, db.ForeignKey("location.feature_nc"))
	feature_nc = db.relationship("location",backref="Sample",lazy="select")

	def __init__(self,id,date,location):
		self.SAMPLE_ID = id
		self.date_gathered = date
		self.LOCATION_FEATURE_NC = location


class Physical_data(db.Model):

	Phys_ID = db.Column(db.Integer, primary_key=True)
	SAMPLE_ID = db.Column(db.Integer, db.ForeignKey('sample.sample_id'))
	sample = db.relationship("Sample",backref="Physical_data",lazy='select')

	Temperature = db.Column(db.Float)
	ph_level = db.Column(db.Float)
	redox = db.Column(db.Float)
	dissolved_oxygen = db.Column(db.Float)
	conductivity = db.Column(db.Float)
	date_gathered = db.Column(db.Float)

	def __init__(self, pid,sid,temp,ph,red,dis_ox,cond,date):
		self.Phys_ID          = pid
		self.SAMPLE_ID        = sid
		self.Temperature      = temp
		self.ph_level         = ph
		self.redox            = red
		self.dissolved_oxygen = dis_ox
		self.conductivity     = cond
		self.date_gathered    = date

class Location(db.Model):

	Feature_nc = db.Column(db.String, primary_key=True)
	common_feature_name = db.Column(db.String)
	eastings = db.Column(db.Numeric)
	northings = db.Column(db.Numeric)
	feature_system = db.Column(db.String)
	description = db.Column(db.String)
	toilet = db.Column(db.Boolean)
	parkbench = db.Column(db.Boolean)
	track = db.Column(db.Boolean)
	private = db.Column(db.Boolean)

 	def __init__(self,feature_nc,fName,e,n,fSystem,desc,toilet,pbench,track,private):

	 	self.Feature_nc = feature_nc
	 	self.common_feature_name = fName
	 	self.eastings = e
	 	self.northings = n
	 	self.feature_system = fSystem
	 	self.description = desc
	 	self.toilet = toilet
	 	self.parkbench = pbench
	 	self.track = track
	 	self.private = private

		
		

class User(db.Model):

	username = db.Column(db.String)
	password = db.Column(db.String)

	def __init__(self, uName,pWord):
		username = uname
		password = pWord
		
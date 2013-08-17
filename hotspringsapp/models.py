from flask.ext.sqlalchemy import SQLAlchemy
from hotspringsapp import app
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy(app)


class Location(db.Model):

	id = db.Column(db.String, primary_key=True)
	feature_name = db.Column(db.String)
	eastings = db.Column(db.Numeric)
	northings = db.Column(db.Numeric)
	feature_system = db.Column(db.String)
	description = db.Column(db.String)
	toilet = db.Column(db.Boolean)
	parkbench = db.Column(db.Boolean)
	track = db.Column(db.Boolean)
	private = db.Column(db.Boolean)
	colour = db.Column(db.String)



 	def __init__(self,location_id,fName,e,n,fSystem,desc,toilet,pbench,track,private,colour):

	 	self.id = location_id
	 	self.feature_name = fName
	 	self.eastings = e
	 	self.northings = n
	 	self.feature_system = fSystem
	 	self.description = desc
	 	self.toilet = toilet
	 	self.parkbench = pbench
	 	self.track = track
	 	self.private = private
	 	self.colour = colour
	



class Physical_data(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	initialTemp = db.Column(db.Numeric)
	pH = db.Column(db.Numeric)
	redox = db.Column(db.Numeric)
	dO = db.Column(db.Numeric)
	conductivity = db.Column(db.Numeric)
	date_gathered = db.Column(db.Float)
	sampleTemp = db.Column(db.Numeric)

	def __init__(self, phys_id,iTemp,ph,red,dis_ox,cond,date,sTemp):
		self.id               = phys_id
		self.initialTemp      = iTemp
		self.pH               = ph
		self.redox            = red
		self.dO               = dis_ox
		self.conductivity     = cond
		self.date_gathered    = date
		self.sampleTemp		  = sTemp

class Sample(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	date_gathered = db.Column(db.DateTime)
	location_id = db.Column(db.String, db.ForeignKey("location.id"))
	phys_id = db.Column(db.Integer, db.ForeignKey("physical_data.id"))

	location = db.relationship("Location",backref="Sample",lazy="select")
	phys = db.relationship("Physical_data",backref="Sample",lazy="select")
	image = db.relationship("Images",backref="Sample",lazy="select" , uselist=True)

	def __init__(self,id,date,location,physID):
		self.id = id
		self.date_gathered = date
		self.location_id = location
		self.phys_id = physID

	def __repr__(self):
		return '<Sample {0} {1} {2}>'.format(self.id,self.location_id,self.date_gathered)


class Images(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	sample_id = db.Column(db.Integer, db.ForeignKey("sample.id"))
	image_path = db.Column(db.String (150))
	image_name = db.Column(db.String (150))



	def __init__(self,id,sid,iPath,iName):
		self.id = id
		self.sample_id = sid
		self.image_path = iPath
		self.image_name = iName


		
		

class User(db.Model):

	username = db.Column(db.String(100), primary_key=True)
	password = db.Column(db.String(100))

	def __init__(self,username,password):
		self.username = username
		self.password = password

	def check_password(self, password):
		return check_password_hash(self.password,password)




db.create_all()
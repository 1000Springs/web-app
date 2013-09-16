from hotspringsapp import app,db
from werkzeug.security import generate_password_hash, check_password_hash





class Location(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	feature_name = db.Column(db.String(50))
	feature_system = db.Column(db.String(50))
	lat = db.Column(db.Float)
	lng = db.Column(db.Float)	
	description = db.Column(db.String(200))
	toilet = db.Column(db.Boolean)
	parkbench = db.Column(db.Boolean)
	track = db.Column(db.Boolean)
	private = db.Column(db.Boolean)
	colour = db.Column(db.String(50))



 	# def __init__(self,location_id,fName,latPos,lngPos,fSystem,desc,toilet,pbench,track,private,colour):

	 # 	self.id = location_id
	 # 	self.feature_name = fName
	 # 	self.lat = latPos
	 # 	self.lng = lngPos
	 # 	self.feature_system = fSystem
	 # 	self.description = desc
	 # 	self.toilet = toilet
	 # 	self.parkbench = pbench
	 # 	self.track = track
	 # 	self.private = private
	 # 	self.colour = colour
	



class Physical_data(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	initialTemp = db.Column(db.Float)
	sampleTemp = db.Column(db.Float)
	pH = db.Column(db.Float)
	redox = db.Column(db.Float)
	dO = db.Column(db.Float)
	conductivity = db.Column(db.Float)
	date_gathered = db.Column(db.DateTime)
	size = db.Column(db.String(20))
	colour = db.Column(db.String(7))
	ebullition = db.Column(db.String(50))
	turbidity = db.Column(db.Float)
	dnaVolume = db.Column(db.Float)
	ferrousIronAbs = db.Column(db.Float)

	

	# def __init__(self, phys_id,iTemp,sTemp,ph,red,dis_ox,cond,date):
	# 	self.id               = phys_id
	# 	self.initialTemp      = iTemp
	# 	self.pH               = ph
	# 	self.redox            = red
	# 	self.dO               = dis_ox
	# 	self.conductivity     = cond
	# 	self.date_gathered    = date
	# 	self.sampleTemp		  = sTemp

class Sample(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	date_gathered = db.Column(db.DateTime, nullable=False)
	sampler = db.Column(db.String(50), nullable=False)
	location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
	phys_id = db.Column(db.Integer, db.ForeignKey("physical_data.id"))
	chem_id = db.Column(db.Integer, db.ForeignKey("chemical_data.id"))

	location = db.relationship("Location",backref="Sample",lazy="select")
	phys = db.relationship("Physical_data",backref="Sample",lazy="select")
	image = db.relationship("Images",backref="Sample",lazy="select" , uselist=True)
	chem = db.relationship("Chemical_data",backref="Sample",lazy="select")

	# def __init__(self,id,date,location,physID):
	# 	self.id = id
	# 	self.date_gathered = date
	# 	self.location_id = location
	# 	self.phys_id = physID

	def __repr__(self):
		return '<Sample {0} {1} {2}>'.format(self.id,self.location_id,self.date_gathered)


class Images(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	sample_id = db.Column(db.Integer, db.ForeignKey("sample.id"), nullable=False)
	image_path = db.Column(db.String (150), nullable = False)
	image_name = db.Column(db.String (150))



	# def __init__(self,id,sid,iPath,iName):
	# 	self.id = id
	# 	self.sample_id = sid
	# 	self.image_path = iPath
	# 	self.image_name = iName


class User(db.Model):

	username = db.Column(db.String(100), primary_key=True)
	password = db.Column(db.String(100))

	def __init__(self,username,password):
		self.username = username
		self.password = password

	def check_password(self, password):
		return check_password_hash(self.password,password)


class Chemical_data(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	Li    = db.Column(db.Float)
	B     = db.Column(db.Float)
	N     = db.Column(db.Float)
	Na    = db.Column(db.Float)
	P     = db.Column(db.Float)
	Cl    = db.Column(db.Float)
	C     = db.Column(db.Float)
	Al    = db.Column(db.Float)
	Si    = db.Column(db.Float)
	K     = db.Column(db.Float)
	Ca    = db.Column(db.Float)
	V     = db.Column(db.Float)
	Cr    = db.Column(db.Float)
	Fe    = db.Column(db.Float)
	Mn    = db.Column(db.Float)
	cobalt    = db.Column(db.Float)
	Ni    = db.Column(db.Float)
	Cu    = db.Column(db.Float)
	Zn    = db.Column(db.Float)
	Mg    = db.Column(db.Float)
	As    = db.Column(db.Float)
	Se    = db.Column(db.Float)
	Br    = db.Column(db.Float)
	Sr    = db.Column(db.Float)
	Mo    = db.Column(db.Float)
	Ag    = db.Column(db.Float)
	Cd    = db.Column(db.Float)
	In    = db.Column(db.Float)
	Ba    = db.Column(db.Float)
	La    = db.Column(db.Float)
	Ti    = db.Column(db.Float)
	Pb    = db.Column(db.Float)
	Bi    = db.Column(db.Float)
	U     = db.Column(db.Float)
	CH4   = db.Column(db.Float)
	H2S   = db.Column(db.Float)
	H2    = db.Column(db.Float)
	CO    = db.Column(db.Float)
	nitrate  = db.Column(db.Float)
	nitrite  = db.Column(db.Float)
	ammonium  = db.Column(db.Float)
	sulfate = db.Column(db.Float)
	chloride   = db.Column(db.Float)
	phosphate = db.Column(db.Float)
	iron2  = db.Column(db.Float)
	bicarbonate = db.Column(db.Float)

	def returnElements(self):
		elements = []
		elements.append(["Li",self.Li])
		elements.append(["B",self.B])
		elements.append(["N",self.N])
		elements.append(["Na",self.Na])
		elements.append(["P",self.P])
		elements.append(["Cl",self.Cl])
		elements.append(["C",self.C])
		elements.append(["Al",self.Al])
		elements.append(["Si",self.Si])
		elements.append(["K",self.K])
		elements.append(["Ca",self.Ca])
		elements.append(["V ",self.V])
		elements.append(["Cr",self.Cr])
		elements.append(["Fe",self.Fe])
		elements.append(["Mn",self.Mn])
		elements.append(["cobalt",self.cobalt])
		elements.append(["Ni",self.Ni])
		elements.append(["Cu",self.Cu])
		elements.append(["Zn",self.Zn])
		elements.append(["Mg",self.Mg])
		elements.append(["As",self.As])
		elements.append(["Se",self.Se])
		elements.append(["Br",self.Br])
		elements.append(["Sr",self.Sr])
		elements.append(["Mo",self.Mo])
		elements.append(["Ag",self.Ag])
		elements.append(["Cd",self.Cd])
		elements.append(["In",self.In])
		elements.append(["Ba",self.Ba])
		elements.append(["La",self.La])
		elements.append(["Ti",self.Ti])
		elements.append(["Pb",self.Pb])
		elements.append(["Bi",self.Bi])
		elements.append(["U",self.U])
		return elements

	def returnGases(self):
		gases = []
		gases.append(["CH4",self.CH4])
		gases.append(["H2S",self.H2S])
		gases.append(["H2",self.H2])
		gases.append(["CO",self.CO])
		return gases

	def returnCompounds(self):
		compounds = []
		compounds.append(["nitrate",self.nitrate])
		compounds.append(["nitrite",self.nitrite])
		compounds.append(["ammonium",self.ammonium])
		compounds.append(["sulfate",self.sulfate])
		compounds.append(["chloride",self.chloride])
		compounds.append(["phosphate",self.phosphate])
		compounds.append(["iron2",self.iron2])
		compounds.append(["bicarbonate",self.bicarbonate])
		return compounds



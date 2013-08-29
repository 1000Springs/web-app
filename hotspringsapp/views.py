import MySQLdb
import datetime
import time
from hotspringsapp import app
from hotspringsapp.database import db_session

from flask import Flask, url_for, render_template, request, g, session, flash, redirect
from models import *
from forms import *




def get_user_name():
    """ Fetch the logged in User"""
    return session['logged_in'] if session.has_key('logged_in') else None

@app.route('/attemptLogin', methods=['POST','GET'])
def attemptLogin():

	user = User.query.filter_by(username=request.form['username']).first()
	error = None
	if request.method == 'POST':
		if user is None:
			error = 'Invalid Username'
		elif request.form['password'] != user.password:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			
			return redirect(url_for('samplesite',site_id=request.form['site_id']))

	return render_template('login.html', error=error, site_id=request.form['site_id'])

@app.route('/login', methods=['POST','GET'])
def login():
	error = None
	return render_template('login.html', error=None,site_id=None)



@app.route('/about')
def about():
	return render_template('about.html');

@app.route('/browseby')
def browseby():
	return render_template('browseby.html');


#Old database Connection
@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()
	
def connect_db():
	return MySQLdb.connect(host="localhost",user="root",passwd="admin",db="geothermaldb")
#	
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search')
def search():

	
	return redirect(url_for('login')) 

	return render_template('search.html')
	
@app.route('/simplesearch')
def simplesearch():


	form = SearchForm()	

	return render_template('simplesearch.html',form=form)
	
@app.route('/results')
def results():
	
	

	cur = g.db.cursor()
	
	#e.g. [u'temperature,=,50', u'redox,=,60', u'dissolved_oxygen,=,90']
	conditions = request.args.getlist("conditions")

	#e.g. [[u'temperature', u'=', u'50'], [u'redox', u'=', u'60'], [u'dissolved_oxygen', u'=', u'90']]
	conditions = [x.split(',') for x in conditions]

	#e.g. [u'temperature = 50', u'redox = 60', u'dissolved_oxygen = 90']
	conditions = [" ".join(x) for x in conditions]

	query = "Select * FROM physical_data where "

	#adds conditions onto end of query e.g. "temperature = 50 and"
	for cond in conditions[:-1]:
		query += (cond + " and ")

	#for the last item so that another "and" does not get added
	query += conditions[-1]

	cur.execute(query);	
	
	entries = [dict(sample_id=row[0], phys_id=row[1], temperature=row[2], ph_level=row[3], redox=row[4], dissolved_oxygen=row[5], conductivity=row[6] ) for row in cur.fetchall()]
	
	cur.close()
	
	return render_template('results.html', entries=entries)

@app.route('/mapresults')
def mapResults():

	cur = g.db.cursor()

	sampleSites = request.args.getlist('sampleSite');
	
	sampleSites = "(" + ','.join(["'"+x+"'" for x in sampleSites]) + ")"

	query = """Select p.sample_id,p.phys_id,p.initialTemp,p.ph_level,p.redox,p.dissolved_oxygen,p.conductivity 
			   from physical_data p, location l, sample s 
			   where s.sample_id = p.sample_id 
			   and s.location_feature_nc = l.feature_nc 
			   and l.feature_nc in {selectedSites}""".format(selectedSites=sampleSites)

	cur.execute(query)

	entries = [dict(sample_id=row[0], phys_id=row[1], temperature=row[2], ph_level=row[3], redox=row[4], dissolved_oxygen=row[5], conductivity=row[6] ) for row in cur.fetchall()] 

	cur.close();

	return render_template('results.html',entries=entries)
	
@app.route('/mapsearch')
def mapsearch():

	cur = g.db.cursor()
	
	cur.execute("""select s.location_feature_nc,l.common_feature_name,l.feature_system,l.description,p.initialTemp, l.eastings,l.northings
				from sample s, physical_data p, location l 
				where l.FEATURE_NC = s.location_feature_nc
				and p.sample_id = s.sample_id
				and s.sample_id in
					(select sample_id 
					from sample group 
					by location_feature_nc
					having max(date_gathered))""")
	
	positions = [dict(eastings=float(row[5]),northings=row[6],city=row[2],  desc=row[3], feature_name=row[1],id=row[0]) for row in cur.fetchall()]
	
	app.logger.debug(positions)
	
	cur.close()

	return render_template('mapsearch.html',positions=positions)

	
@app.route('/simpleresults')
def simpleresults():
	
	cur = g.db.cursor()	

	minTemp = request.args.get('minTemp')
	maxTemp = request.args.get('maxTemp')


	sampleSites = Sample.query.filter(Physical_data.id == Sample.phys_id,
									  Physical_data.initialTemp>= minTemp,
									  Physical_data.initialTemp < maxTemp).order_by(Sample.location_id,Sample.date_gathered.desc()).all()

	

	

	latestSamples = []	
	prev = sampleSites[0].location_id
	tempSamples = []
	for s in sampleSites:
		
		if(s.location_id != prev):
			latestSamples.append(tempSamples[0])
			tempSamples = []

		tempSamples.append(s)
		prev = s.location_id
		
	
	latestSamples = Pagination(None,1,5,4,latestSamples).items

	app.logger.debug(len(latestSamples))
	# for s in sampleSites:		
	# 	print s.location_id,s.date_gathered


	# app.logger.debug(sampleSites.count())
	# app.logger.debug(dir(sampleSites[0]))
	# session['filter'] = filter
	

	# tempMin = 0

	# tempMax = 100
	
	# query = """select s.location_feature_nc,l.common_feature_name,l.feature_system,l.description,p.initialTemp, l.eastings,l.northings,l.toilet, l.parkbench,l.track, l.private, i.image_path
	# 				from sample s, physical_data p, location l, images i
	# 				where l.FEATURE_NC = s.location_feature_nc
	# 				and p.sample_id = s.sample_id
	# 				and i.sample_id = s.sample_id
	# 				and s.sample_id =
 #       								( SELECT sample_id
 #           							FROM sample
	# 								where location_feature_nc = s.location_feature_nc
	# 								order by date_gathered desc
	# 								limit 1
 #   									)"""

	# if filter == "city":
	# 	queryCity = request.args.get('city')
	# 	query += "and l.feature_system = '{city}'".format(city=queryCity);
				

		
	# 	filter = queryCity
	# 	session['filter'] = queryCity
	# elif filter.lower() == "safe":
		
	# 	tempMax = 60
	# 	query += "and p.initialTemp <= {tempMax}".format(tempMax=tempMax)
		
						
	# elif filter.lower() == "unsafe":
	
	# 	tempMin =60

	# 	query += "and p.initialTemp >= {tempMin}".format(tempMin=tempMin)
		
		
	
	# elif filter.lower() == "hottest":
	# 	tempMin = 90
	# 	query += "and p.initialTemp >= {tempMin}".format(tempMin=tempMin)
		
	
	# elif filter.lower() == "unique":
	# 	site_id = "WAI_TPU"
	# 	query += "and l.feature_nc = '{site_id}'".format(site_id=site_id)
		
		
	# else:
	# 	if request.args.get('tempMin') is not None:
	# 		tempMin = request.args.get('tempMin')
		
	# 	if request.args.get('tempMax') is not None:
	# 		tempMax = request.args.get('tempMax')

		
	# 	query += """and p.initialTemp >= {tempMin}
	# 				and p.initialTemp <= {tempMax}""".format(tempMin=tempMin,tempMax=tempMax)
		
	
	# temp = ""
	# springAtt = request.args.getlist("items");
	
	# for att in springAtt:
	# 	temp += "and " + att + "= true ";
	
	# query += temp
	# app.logger.debug (app.config['SQLALCHEMY_DATABASE_URI'])
	# cur.execute(query)

	entries = [dict(location_id=s.location_id,
					feature_name=s.location.feature_name, 
					city=s.location.feature_system, 
					desc=s.location.description, 
					temp=s.phys.initialTemp,
					eastings=s.location.eastings,
					northings=s.location.northings,
					toilet=s.location.toilet, 
					parkbench=s.location.parkbench, 
					track=s.location.track, 
					private=s.location.private,
					imagepath=s.image[0].image_path) for s in latestSamples]	


	form = SearchForm()	

	phys_data = Physical_data.query.order_by(Physical_data.initialTemp).all()

	count = {'1-25':0,'26-50':0,'51-75':0,'76-100':0}
	pieChart = []
	for t in phys_data:
		if t.initialTemp >= 1 and t.initialTemp <= 25:
			count["1-25"] +=1
		if t.initialTemp >= 26 and t.initialTemp <= 50:
			count["26-50"] +=1
		if t.initialTemp >= 51 and t.initialTemp <= 75:
			count["51-75"] +=1
		if t.initialTemp >= 76 and t.initialTemp <= 100:
			count["76-100"] +=1
	
	


	pieChart = [dict(range=k,count=v) for k,v in zip(count.keys(),count.values())]




	return render_template('simpleresults.html',entries=entries,
												form=form,
												minTemp=minTemp,
												maxTemp=maxTemp,
												
												 pieChart=pieChart
												)


	# return render_template('about.html')
@app.route('/searchbyimage')
@app.route('/searchbyimage/<int:page>')
def searchbyimage(page = 1):

	imageList = Images.query.filter(Images.sample_id == Sample.id).group_by(Sample.location_id)

	imageList = imageList.paginate(page,app.config['IMAGES_PER_PAGE'],False)
	
	return render_template('searchbyimage.html',images=imageList)




@app.route('/samplesite/<site_id>')
def samplesite(site_id):	


	
	locationSamples = Sample.query.filter(Location.id == Sample.location_id, Location.id == site_id)

	latestSample = locationSamples.order_by(Sample.date_gathered.desc()).first()
	

	siteInfo = dict(location_id=latestSample.location_id,
					feature_name=latestSample.location.feature_name,
					city=latestSample.location.feature_system, 
					desc=latestSample.location.description, 
					temp=latestSample.phys.initialTemp, 
					eastings=latestSample.location.eastings,
					northings=latestSample.location.northings, 
					toilet=latestSample.location.toilet, 
					parkbench=latestSample.location.toilet, 
					track=latestSample.location.toilet, 
					private=latestSample.location.toilet)
					



	images = [dict(imagepath=s.image_path,
				   imagename=s.image_name) for s in latestSample.image]	

	
	return render_template('samplesite.html',sample_site=siteInfo,
											 images=images)
	 


@app.route("/sotd")
def sotd():
	sotdTup = GetSOTD()
	

	return render_template('sotd.html',sotdimg = sotdTup[0],
										sotdsite_id = sotdTup[1])
@app.route("/channel")
def channel():
	return render_template('channel.html')


@app.route("/searchbycategory")
def searchbycat():
	return render_template('searchbycategory.html')

def GetSOTD():
	g.db = connect_db()

	cur = g.db.cursor()

	f = open('SOTD.ini','r')

	

	date = f.readline().rstrip()
	springIndex = f.readline().rstrip()
	springIndex = int(springIndex)
	currentDate = datetime.datetime.strptime(date,"%d/%m/%Y")

	now = datetime.datetime.now()

	#now = now.strftime("%d/%m/%Y")

	if (now - currentDate) > datetime.timedelta(days=1):
		springIndex+=1

	query = """select image_path
				from images"""

	cur.execute(query)
	results = cur.fetchall()
	f.close()
	f = open('SOTD.ini','w+')	
	f.write(datetime.datetime.now().strftime("%d/%m/%Y") + "\n")
	f.write(str(springIndex))
	
	f.close()
	return results[springIndex]  


	
if __name__ == "__main__":
	app.run()
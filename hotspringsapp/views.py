import MySQLdb
import datetime
import time
from xlwt import Workbook, XFStyle, Alignment, easyxf
import os
import StringIO
import mimetypes
from hotspringsapp import app
from sqlalchemy.sql import func
from werkzeug.datastructures import Headers

from flask import Flask, url_for, render_template, request, g, session, flash, redirect, Response, abort, jsonify
from models import *
from forms import *



@app.errorhandler(404)
def page_not_found(e):
   
    title = " 404 Error - Uh oh!"
    errorMessage = "The page you were looking for could not be found."
    return render_template('error.html',title=title,message=errorMessage), 404

@app.errorhandler(500)
def page_not_found(e):
   
    title = "500 Error - Oh dear, something's not working!"
    errorMessage = "Something's gone wrong, sorry about that, but we are working as hard as we can to fix it."
    return render_template('error.html',title=title,message=errorMessage), 500


def get_user_name():
    """ Fetch the logged in User"""
    return session['logged_in'] if session.has_key('logged_in') else None

@app.route('/attemptLogin', methods=['POST','GET'])
def attemptLogin():

	user = User.query.filter_by(username=request.form['username']).first()
	error = None
	if request.method == 'POST':		
		if user is not None and request.form['password'] == user.password:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('index'))
		else:
			error = "Incorrect username or password"			
		
	return render_template('login.html', error=error, site_id=request.form['site_id'])

@app.route('/login', methods=['POST','GET'])
def login():
	error = None
	return render_template('login.html', error=None,site_id=None)

@app.route('/logout', methods=['POST','GET'])
def logout():
	
	app.logger.debug(request.url_rule)
	session.pop('logged_in',None)
	return redirect(url_for('index'))

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/licence')
def licence():
	return render_template('licence.html')

@app.route('/')
def index():

	locations = Sample.query.count()

	return render_template('index.html',springs=locations)

@app.route('/search', methods=['GET'])
def search():	

	if session.get('logged_in') != None:
		return render_template('search.html')
	else:
		return redirect(url_for('login'))
	
@app.route('/simplesearch')
def simplesearch():

	#finds max temp in database	
	maxTemp = db.session.query(func.max(Physical_data.initialTemp).label("max_Temp")).all()[0].max_Temp

	tempRanges = dict(minTemp = 0,maxTemp = maxTemp)
	form = SearchForm(filters = 'all')
	locations = Location.query.with_entities(Location.district).group_by(Location.district)

	locations = [i[0] for i in locations if i[0] != None]


	return render_template('simplesearch.html',form=form, tempRanges=tempRanges,locations=locations)

@app.route('/getLocationTier', methods =['POST'])
def getLocationTier():
	location = request.form['location']
	tier = int(request.form['tier'])



	
	if tier == 1:		
		results = Location.query.with_entities(Location.feature_system).filter_by(district = location).group_by(Location.feature_system)

	
	if tier == 2:
		results = Location.query.with_entities(Location.location).filter_by(feature_system = location).group_by(Location.location)
		
	

	app.logger.debug(results.all())

	results = [i[0] for i in results if i[0] != None]

	

	

	return jsonify({'results':results,'tier':tier})
	
# @app.route('/results')
# def results():
	
	

# 	cur = g.db.cursor()
	
# 	#e.g. [u'temperature,=,50', u'redox,=,60', u'dissolved_oxygen,=,90']
# 	conditions = request.args.getlist("conditions")

# 	#e.g. [[u'temperature', u'=', u'50'], [u'redox', u'=', u'60'], [u'dissolved_oxygen', u'=', u'90']]
# 	conditions = [x.split(',') for x in conditions]

# 	#e.g. [u'temperature = 50', u'redox = 60', u'dissolved_oxygen = 90']
# 	conditions = [" ".join(x) for x in conditions]

# 	query = "Select * FROM physical_data where "

# 	#adds conditions onto end of query e.g. "temperature = 50 and"
# 	for cond in conditions[:-1]:
# 		query += (cond + " and ")

# 	#for the last item so that another "and" does not get added
# 	query += conditions[-1]

# 	cur.execute(query);	
	
# 	entries = [dict(sample_id=row[0], phys_id=row[1], temperature=row[2], ph_level=row[3], redox=row[4], dissolved_oxygen=row[5], conductivity=row[6] ) for row in cur.fetchall()]
	
# 	cur.close()
	
# 	return render_template('results.html', entries=entries)

@app.route('/mapresults')
def mapResults():

# 	cur = g.db.cursor()

# 	sampleSites = request.args.getlist('sampleSite');
	
# 	sampleSites = "(" + ','.join(["'"+x+"'" for x in sampleSites]) + ")"

# 	query = """Select p.sample_id,p.phys_id,p.initialTemp,p.ph_level,p.redox,p.dissolved_oxygen,p.conductivity 
# 			   from physical_data p, location l, sample s 
# 			   where s.sample_id = p.sample_id 
# 			   and s.location_feature_nc = l.feature_nc 
# 			   and l.feature_nc in {selectedSites}""".format(selectedSites=sampleSites)

# 	cur.execute(query)

# 	entries = [dict(sample_id=row[0], phys_id=row[1], temperature=row[2], ph_level=row[3], redox=row[4], dissolved_oxygen=row[5], conductivity=row[6] ) for row in cur.fetchall()] 

# 	cur.close();

	return "Not working yet"
	
@app.route('/mapsearch')
def mapsearch():

# 	cur = g.db.cursor()
	
# 	cur.execute("""select s.location_feature_nc,l.common_feature_name,l.feature_system,l.description,p.initialTemp, l.lat,l.lng
# 				from sample s, physical_data p, location l 
# 				where l.FEATURE_NC = s.location_feature_nc
# 				and p.sample_id = s.sample_id
# 				and s.sample_id in
# 					(select sample_id 
# 					from sample group 
# 					by location_feature_nc
# 					having max(date_gathered))""")
	
	# positions = [dict(lat=float(row[5]),lng=row[6],city=row[2],  desc=row[3], feature_name=row[1],id=row[0]) for row in cur.fetchall()]
	
	locations = Location.query.filter(Sample.location_id == Location.id)
	
# 	cur.close()

	return render_template('mapsearch.html',positions=locations)
	# return "Coming Soon"


def url_for_other_page(page = 1,showAll=None):
   
	args = request.args.copy()	

	return url_for(request.endpoint,page=page,showAll = showAll, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page

@app.route('/simpleresults', defaults={'page':1}, methods=['GET'])	
@app.route('/simpleresults/<int:page>',methods=['GET'])
@app.route('/simpleresults/<int:page>/<showAll>',methods=['GET'])

def simpleresults(page = 1, showAll = None):	



	args = request.args.copy()
	

	minTemp = args.get('minTemp')
	maxTemp = args.get('maxTemp')
	district = args.get('dist')
	feature_system = args.get('fsys')
	location = args.get('loc')
	minPH = args.get('minPH')
	maxPH = args.get('maxPH')
	minTurb = args.get('minTurb')
	maxTurb = args.get('maxTurb')
	minCond = args.get('minCond')
	maxCond = args.get('maxCond')


	
	

		

	listOfAllLocations = Location.query.filter(Sample.location_id == Location.id).order_by(Location.id).all()
	latestSampleIds = []



	for l in listOfAllLocations:		
		latestSampleIds.append(l.latestSample().id)

	latestFilteredSamples = Sample.query.filter(Physical_data.id == Sample.phys_id,
												Physical_data.initialTemp>= minTemp,
												Physical_data.initialTemp < maxTemp,
												Physical_data.pH >= minPH,
												Physical_data.pH < maxPH,
												Physical_data.conductivity >= minCond,
												Physical_data.conductivity < maxCond,
												Physical_data.turbidity >= minTurb,
												Physical_data.turbidity < maxTurb,
												Sample.location_id == Location.id,																																											
												Sample.id.in_(latestSampleIds)
												)	

	if district != "":
		latestFilteredSamples = latestFilteredSamples.filter(Location.district == district)

	if feature_system != "":		
		latestFilteredSamples = latestFilteredSamples.filter(Location.feature_system == feature_system)

	if location != "":
		latestFilteredSamples = latestFilteredSamples.filter(Location.location == location)

	
	if showAll == "all":
		resultsPerPage = latestFilteredSamples.count()
	else:
		resultsPerPage = app.config["RESULTS_PER_PAGE"]



	paginatedSamples = latestFilteredSamples.paginate(page,resultsPerPage,False)

	
	
	form = SearchForm()

	phys_data = Physical_data.query.order_by(Physical_data.initialTemp).all()

	count = {'1-25':0,'26-50':0,'51-75':0,'76-100':0}
	pieChart = []
	for s in latestFilteredSamples:
		if s.phys.initialTemp >= 1 and s.phys.initialTemp <= 25:
			count["1-25"] +=1
		if s.phys.initialTemp >= 26 and s.phys.initialTemp <= 50:
			count["26-50"] +=1
		if s.phys.initialTemp >= 51 and s.phys.initialTemp <= 75:
			count["51-75"] +=1
		if s.phys.initialTemp >= 76 and s.phys.initialTemp <= 100:
			count["76-100"] +=1

	pieChart = [dict(range=k,count=v) for k,v in zip(count.keys(),count.values())]

	return render_template('simpleresults.html',entries=paginatedSamples,
												form=form,
												minTemp=minTemp,
												maxTemp=maxTemp,												
												pieChart=pieChart
												)


@app.route('/searchbyimage')
@app.route('/searchbyimage/<int:page>')
@app.route('/searchbyimage/<showAll>')
def searchbyimage(page = 1,showAll = None):

	#The reason this query isn't returning the correct number of results is because the "Location.access" field is null on lots of samples
	imageList = Image.query.filter(Image.sample_id == Sample.id, Image.image_type == "BESTPHOTO",Location.id==Sample.location_id).group_by(Sample.location_id)

	imagesPerPage = app.config['IMAGES_PER_PAGE']

	if showAll == "all":
		imagesPerPage = imageList.count()
	
	imageList = imageList.paginate(page,imagesPerPage,False)
	
	return render_template('searchbyimage.html',images=imageList)


@app.route('/ourscience')
def ourscience():

	return render_template('ourscience.html')

@app.route('/samplesite/<int:site_id>')
def samplesite(site_id):	
	
	gatheredInfoCount = 0

	locationSamples = Location.query.filter(Location.id == Sample.location_id, Location.id == site_id)

	if locationSamples.count() == 0:
		abort(404)

	latestSample = locationSamples.first().latestSample()
	
	
	chemJson = {"name":"", "children":[{"name":"", "children":[]}]};	


	if latestSample.phys is not None:
		gatheredInfoCount+= 1

	


	if latestSample.chem is not None:
		gatheredInfoCount+= 1	
 		for e in latestSample.chem.returnElements(): 			
 			if e[1] != None and e[1] > 0:
				chemJson["children"][0]["children"].append({"name":e[0],"size":e[1]})

		for e in latestSample.chem.returnGases():
			if e[1] != None and e[1] > 0:
				chemJson["children"][0]["children"].append({"name":e[0],"size":e[1]})

		for e in latestSample.chem.returnCompounds():
			if e[1] != None and e[1] > 0:
				chemJson["children"][0]["children"].append({"name":e[0],"size":e[1]})
	else:
		chemJson = None;
	
	#Position of statusGraph starts at zero
	gatheredInfoCount -= 1;

	taxJson = None;

	
	return render_template('samplesite.html',sample_site=latestSample,											 
											 chemJson=chemJson,
											 statusPos = gatheredInfoCount,
											 taxJson=taxJson)	 

@app.route('/download/<int:site_id>')
def download(site_id):

	# locationSamples = Sample.query.filter(Location.id == Sample.location_id, Location.id == site_id)

	# latestSample = locationSamples.order_by(Sample.date_gathered.desc()).first()



	# response = Response()
	# response.status_code = 200

	
	# alignment = Alignment()
	# # alignment.wrap = True	

	# style = XFStyle()
	# style.alignment = alignment

	# book = Workbook()
	# sheet1 = book.add_sheet('Sheet 1')

	# headings = sheet1.row(0)
	# headings.write(0, 'Feature Name', easyxf('font: bold True;'))
	# headings.write(1, 'Feature System', easyxf('font: bold True;'))
	# headings.write(2, 'Description', easyxf('font: bold True;'))
	# headings.write(3, 'Lat/Lng', easyxf('font: bold True;'))
	# headings.write(4, 'Temperature', easyxf('font: bold True;'))
	# headings.write(5, 'pH', easyxf('font: bold True;'))
	# headings.write(6, 'Redox', easyxf('font: bold True;'))
	# headings.write(7, 'Dissolved Oxygen', easyxf('font: bold True;'))
	# headings.write(8, 'Conductivity', easyxf('font: bold True;'))
	# headings.write(9, 'Ebullition', easyxf('font: bold True;'))
	# headings.write(10, 'Turbidity', easyxf('font: bold True;'))
	# headings.write(11, 'DNA Volume', easyxf('font: bold True;'))
	# headings.write(12, 'Ferrous Iron', easyxf('font: bold True;'))



	# locationValues = sheet1.row(1)
	# locationValues.write(0, latestSample.location.feature_name, style)
	# locationValues.write(1, latestSample.location.feature_system, style)
	# locationValues.write(2, latestSample.location.description, style)
	# locationValues.write(3, str(latestSample.location.lat) + "," + str(latestSample.location.lng), style)
	# locationValues.write(4, latestSample.phys.initialTemp, style)
	# locationValues.write(5, latestSample.phys.pH, style)
	# locationValues.write(6, latestSample.phys.redox, style)
	# locationValues.write(7, latestSample.phys.dO, style)
	# locationValues.write(8, latestSample.phys.conductivity, style)
	# locationValues.write(9, latestSample.phys.ebullition, style)
	# locationValues.write(10, latestSample.phys.turbidity, style)
	# locationValues.write(11, latestSample.phys.dnaVolume, style)
	# locationValues.write(12, latestSample.phys.ferrousIronAbs, style)


	# for i in range(9):
	# 	sheet1.col(i).width = 5000

	# sheet1.col(2).width = 10000


	# book.save('samplesite_'+str(site_id)+'.xls')

	# output = StringIO.StringIO()
	# book.save(output)
	# response.data = output.getvalue()

	# filename = 'samplesite_'+str(site_id)+'.xls'
	# mimetype_tuple = mimetypes.guess_type(filename)

	# #HTTP headers for forcing file download
	# response_headers = Headers({
	#         'Pragma': "public",  # required,
	#         'Expires': '0',
	#         'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
	#         'Cache-Control': 'private',  # required for certain browsers,
	#         'Content-Type': mimetype_tuple[0],
	#         'Content-Disposition': 'attachment; filename=\"%s\";' % filename,
	#         'Content-Transfer-Encoding': 'binary',
	#         'Content-Length': len(response.data)
	#     })

	# if not mimetype_tuple[1] is None:
	#     response.update({
	#             'Content-Encoding': mimetype_tuple[1]
	#         })

	# response.headers = response_headers

	# #as per jquery.fileDownload.js requirements
	# response.set_cookie('fileDownload', 'true', path='/')

	# ################################
	# # Return the response
	# #################################
	# os.remove('samplesite_'+str(site_id)+'.xls')

	return "Under construction"






@app.route("/sotd")
def sotd():
	# sotdTup = GetSOTD()
	

	springOfTheDay = Image.query.filter(Image.sample_id == Sample.id, Image.image_type == "LARGE",Location.id==Sample.location_id).group_by(Sample.location_id)
	

	#modulo is to make sure it doesn't index out of bounds
	springOfTheDay = springOfTheDay[GetSOTD() % springOfTheDay.count()]


	app.logger.debug(springOfTheDay.image_path)

	return render_template('sotd.html',location = springOfTheDay)

@app.route("/searchbycategory")
def searchbycat():
	return render_template('searchbycategory.html')

def GetSOTD():
	
	path = app.config['DEFAULT_PATH']

	f = open(path +'sotd.cfg','r')
	index = int(f.readline().strip())
		

	return index

def d(o):
	app.logger.debug(o)
	
if __name__ == "__main__":
	app.run()
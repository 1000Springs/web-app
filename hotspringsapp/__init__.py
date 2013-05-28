import MySQLdb
import datetime
import time
from flask import Flask, url_for, render_template, request, g, session, flash, redirect


app = Flask(__name__)
app.config.from_pyfile('hotsprings.cfg')




from models import *

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            
            return redirect(url_for('samplesite',site_id=request.form['site_id']))

    return render_template('login.html', error=error)






@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()
	
def connect_db():
	return MySQLdb.connect(host="localhost",user="root",passwd="admin",db="geothermaldb")
	
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search')
def search():
	return render_template('search.html')
	
@app.route('/simplesearch')
def simplesearch():
	return render_template('simplesearch.html')
	
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

	query = """Select p.sample_id,p.phys_id,p.temperature,p.ph_level,p.redox,p.dissolved_oxygen,p.conductivity 
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
	
	cur.execute("""select s.location_feature_nc,l.common_feature_name,l.feature_system,l.description,p.temperature, l.eastings,l.northings
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

	
@app.route('/simpleresults/<filter>')
def simpleresults(filter):
	
	cur = g.db.cursor()
	
	
	
	session['filter'] = filter
	

	tempMin = 0

	tempMax = 100
	
	query = """select DISTINCT s.location_feature_nc,l.common_feature_name,l.feature_system,l.description,p.temperature, l.eastings,l.northings,l.toilet, l.parkbench,l.track, l.private, i.image_path
					from sample s, physical_data p, location l, images i
					where l.FEATURE_NC = s.location_feature_nc
					and p.sample_id = s.sample_id
					and i.sample_id = s.sample_id
					and s.sample_id in
						(select sample_id 
						from sample group 
						by location_feature_nc
						having max(date_gathered)) 
					and i.image_id in
						(select image_id 
						from images
						group by sample_id)"""

	if filter == "city":
		queryCity = request.args.get('city')
		query += "and l.feature_system = '{city}'".format(city=queryCity);
				

		
		filter = queryCity
		session['filter'] = queryCity
	elif filter.lower() == "safe":
		
		tempMax = 60
		query += "and p.temperature <= {tempMax}".format(tempMax=tempMax)
		
						
	elif filter.lower() == "unsafe":
	
		tempMin =60

		query += "and p.temperature >= {tempMin}".format(tempMin=tempMin)
		
		
	
	elif filter.lower() == "hottest":
		tempMin = 90
		query += "and p.temperature >= {tempMin}".format(tempMin=tempMin)
		
	
	elif filter.lower() == "unique":
		site_id = "WAI_TPU"
		query += "and l.feature_nc = '{site_id}'".format(site_id=site_id)
		
		
	else:
		if request.args.get('tempMin') is not None:
			tempMin = request.args.get('tempMin')
		
		if request.args.get('tempMax') is not None:
			tempMax = request.args.get('tempMax')

		
		query += """and p.temperature >= {tempMin}
					and p.temperature <= {tempMax}""".format(tempMin=tempMin,tempMax=tempMax)
		
	
	temp = ""
	springAtt = request.args.getlist("items");
	
	for att in springAtt:
		temp += "and " + att + "= true ";
	
	query += temp

	cur.execute(query)
	entries = [dict(location_id=row[0],
					feature_name=row[1], 
					city=row[2], 
					desc=row[3], 
					temp=row[4],
					eastings=row[5],
					northings=row[6],
					toilet=row[7], 
					parkbench=row[8], 
					track=row[9], 
					private=row[10],
					imagepath=row[11]) for row in cur.fetchall()]

	
	
	query = """
		select t.range as "Range", count(*) as "Occurances"
	from (
	  select case  
	    when temperature between 50 and 59 then ' 50- 59'
	    when temperature between 60 and 69 then ' 60- 69'
		when temperature between 60 and 79 then ' 70- 79'
		when temperature between 80 and 89 then ' 80- 89'
	    else '90-' end as "range"
	  from physical_data) t
	group by t.range"""

	cur.execute(query)


	pieChart = [dict(range=row[0],count=row[1]) for row in cur.fetchall()]



	slices = [["90-100",10],["0-89",12],["blah",12],["test",50]]

	cur.close()	
	return render_template('simpleresults.html',entries=entries,
												filtertype=filter,
												tempMin=tempMin,
												tempMax=tempMax,
												slices=slices,
												pieChart=pieChart
												)

@app.route('/searchbyimage')
def searchbyimage():

	cur = g.db.cursor()

	cur.execute("""select i.image_path, i.image_name, i.sample_id,s.location_feature_nc
					from images i, sample s
					where i.sample_id = s.sample_id;
					""")

	images = [dict(imagepath=row[0],
				   imagename=row[1],
				   site_id=row[3]) for row in cur.fetchall()]

	cur.close()

	return render_template('searchbyimage.html',images=images)

@app.route('/samplesite/<site_id>')
def samplesite(site_id):	

	cur = g.db.cursor()

	id = site_id
	cur.execute("""select s.location_feature_nc,l.common_feature_name,l.feature_system,l.description,p.temperature,l.eastings,l.northings,l.toilet, l.parkbench,l.track, l.private  
				from sample s, physical_data p, location l 
				where l.FEATURE_NC = s.location_feature_nc
				and p.sample_id = s.sample_id 
				and feature_NC=%s
				order by s.date_gathered Desc
				limit 1""",id)
	

	imageLocation = "img/hotsprings1.jpg"

	imageLocation2 = "img/hotsprings2.jpg"
	

	

	entries = [dict(location_id=row[0],
					feature_name=row[1],
					city=row[2], 
					desc=row[3], 
					temp=row[4], 
					eastings=row[5],
					northings=row[6], 
					toilet=row[7], 
					parkbench=row[8], 
					track=row[9], 
					private=row[10], 
					img=imageLocation,
					img2 = imageLocation2) for row in cur.fetchmany(1)]

	cur.execute("""select s.location_feature_nc,l.common_feature_name,l.feature_system,l.description,p.temperature,l.eastings,l.northings,l.toilet, l.parkbench,l.track, l.private  
				from sample s, physical_data p, location l 
				where l.FEATURE_NC = s.location_feature_nc
				and p.sample_id = s.sample_id 
				and feature_NC=%s
				order by s.date_gathered Desc
				limit 1""",id)
	siteData = cur.fetchone()

	siteInfo = dict(location_id=siteData[0],
					feature_name=siteData[1],
					city=siteData[2], 
					desc=siteData[3], 
					temp=siteData[4], 
					eastings=siteData[5],
					northings=siteData[6], 
					toilet=siteData[7], 
					parkbench=siteData[8], 
					track=siteData[9], 
					private=siteData[10], 
					img=imageLocation,
					img2 = imageLocation2)
	app.logger.debug (siteInfo)

	query = """select i.image_path, i.image_name
				   from images i, sample s
				   where s.sample_id = i.sample_id
				   and s.location_feature_nc = '{id}'""".format(id=id)

	

	cur.execute(query)


	images = [dict(imagepath=row[0],
				   imagename=row[1]) for row in cur.fetchall()]
	

	
	
	
	cur.close()
	
	
	
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


@app.route("/searchbycatergory")
def searchbycat():
	return render_template('searchbycatergory.html')

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
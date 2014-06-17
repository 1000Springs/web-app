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
import json
import urllib2

from flask import Flask, url_for, render_template, request, g, session, flash, redirect, Response, abort, jsonify, make_response, send_from_directory
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

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


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

@app.route('/getLocationTier/<location>/<int:tier>', methods =['GET'])
def getLocationTier(location, tier):

    if tier == 1:
        results = Location.query.with_entities(Location.feature_system).filter_by(district = location).group_by(Location.feature_system)

    if tier == 2:
        results = Location.query.with_entities(Location.location).filter_by(feature_system = location).group_by(Location.location)

    results = [i[0] for i in results if i[0] != None]
    return jsonify({'results':results,'tier':tier})



def findMinAndMax(name,field):
  
    min = {"name":"Min","value":db.session.query(func.min(field)).first()[0]}
    max = {"name":"Max","value":db.session.query(func.max(field)).first()[0]}

    array = {"name":name,"values":[min,max]}
    return array


# @app.route('/results')
# def results():



#     cur = g.db.cursor()

#     #e.g. [u'temperature,=,50', u'redox,=,60', u'dissolved_oxygen,=,90']
#     conditions = request.args.getlist("conditions")

#     #e.g. [[u'temperature', u'=', u'50'], [u'redox', u'=', u'60'], [u'dissolved_oxygen', u'=', u'90']]
#     conditions = [x.split(',') for x in conditions]

#     #e.g. [u'temperature = 50', u'redox = 60', u'dissolved_oxygen = 90']
#     conditions = [" ".join(x) for x in conditions]

#     query = "Select * FROM physical_data where "

#     #adds conditions onto end of query e.g. "temperature = 50 and"
#     for cond in conditions[:-1]:
#         query += (cond + " and ")

#     #for the last item so that another "and" does not get added
#     query += conditions[-1]

#     cur.execute(query);

#     entries = [dict(sample_id=row[0], phys_id=row[1], temperature=row[2], ph_level=row[3], redox=row[4], dissolved_oxygen=row[5], conductivity=row[6] ) for row in cur.fetchall()]

#     cur.close()

#     return render_template('results.html', entries=entries)

@app.route('/mapresults')
def mapResults():

#     cur = g.db.cursor()

#     sampleSites = request.args.getlist('sampleSite');

#     sampleSites = "(" + ','.join(["'"+x+"'" for x in sampleSites]) + ")"

#     query = """Select p.sample_id,p.phys_id,p.initialTemp,p.ph_level,p.redox,p.dissolved_oxygen,p.conductivity
#                from physical_data p, location l, sample s
#                where s.sample_id = p.sample_id
#                and s.location_feature_nc = l.feature_nc
#                and l.feature_nc in {selectedSites}""".format(selectedSites=sampleSites)

#     cur.execute(query)

#     entries = [dict(sample_id=row[0], phys_id=row[1], temperature=row[2], ph_level=row[3], redox=row[4], dissolved_oxygen=row[5], conductivity=row[6] ) for row in cur.fetchall()]

#     cur.close();

    return "Not working yet"

@app.route('/mapsearch')
def mapsearch():

#     cur = g.db.cursor()

#     cur.execute("""select s.location_feature_nc,l.common_feature_name,l.feature_system,l.description,p.initialTemp, l.lat,l.lng
#                 from sample s, physical_data p, location l
#                 where l.FEATURE_NC = s.location_feature_nc
#                 and p.sample_id = s.sample_id
#                 and s.sample_id in
#                     (select sample_id
#                     from sample group
#                     by location_feature_nc
#                     having max(date_gathered))""")

    # positions = [dict(lat=float(row[5]),lng=row[6],city=row[2],  desc=row[3], feature_name=row[1],id=row[0]) for row in cur.fetchall()]

    locations = Location.query.filter(Sample.location_id == Location.id)

#     cur.close()

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

    
    
   

    if district != "" and district != None:        
        latestFilteredSamples = latestFilteredSamples.filter(Location.district == district)

    if feature_system != "" and feature_system != None:        
        latestFilteredSamples = latestFilteredSamples.filter(Location.feature_system == feature_system)

    if location != "" and location != None:        
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


@app.route('/publications')
def publications():

    return render_template('publications.html')

@app.route('/methodologies')
def methodologies():

    return render_template('methodologies.html')

@app.route('/dataoverview')
def dataoverview():
    
    maxAndMin = [] 

    maxAndMin.append(findMinAndMax("Temperature",Physical_data.initialTemp))
    maxAndMin.append(findMinAndMax("pH",Physical_data.pH))
    maxAndMin.append(findMinAndMax("Oxidation Reduction Potential",Physical_data.redox))
    maxAndMin.append(findMinAndMax("Dissolved Oxygen",Physical_data.dO))
    maxAndMin.append(findMinAndMax("Conductivity",Physical_data.conductivity))

    scatterData = Physical_data.query.with_entities(Physical_data.initialTemp,Physical_data.pH).filter(Sample.phys_id == Physical_data.id,Sample.location_id== Location.id).all()

    formattedScatterData = [list(x) for x in scatterData]
    formattedScatterData = [["",""]] + formattedScatterData

    return render_template('dataoverview.html',values=maxAndMin,scatterData=formattedScatterData)

@app.route('/samplesite/<int:site_id>')
def samplesite(site_id):

    gatheredInfoCount = 0

    locationSamples = Location.query.filter(Location.id == Sample.location_id, Location.id == site_id)

    if locationSamples.count() == 0:
        abort(404)

    latestSample = locationSamples.first().latestSample()

    if latestSample.chem is not None:
        gatheredInfoCount+= 1

    if latestSample.phys is not None:
        gatheredInfoCount+= 1

    if len(latestSample.getTaxonomy()) > 0:
        gatheredInfoCount+= 1 
            
    gatheredInfoCount -= 1

    return render_template('samplesite.html',sample_site=latestSample,
                                             statusPos = gatheredInfoCount)
    
def __getChemistryData(sample):
    chemJson = {"name":"", "children":[{"name":"", "children":[]}]};
    if sample.chem is not None:
        for e in sample.chem.returnElements():
            if e[1] != None and e[1] > 0:
                chemJson["children"][0]["children"].append({"name":e[0],"size":e[1]})

        for e in sample.chem.returnGases():
            if e[1] != None and e[1] > 0:
                chemJson["children"][0]["children"].append({"name":e[0],"size":e[1]})

        for e in sample.chem.returnCompounds():
            if e[1] != None and e[1] > 0:
                chemJson["children"][0]["children"].append({"name":e[0],"size":e[1]})
    else:
        chemJson = None
                
    return chemJson
    
def __getTaxonomyData(sample):
    taxonomy = sample.getTaxonomy()
    taxJson = None
    if len(taxonomy) > 0:
        taxaNames = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
        currentTaxa = {}
        for taxaName in taxaNames:
            currentTaxa[taxaName] = None 
        data = {"name": "root", "children": []}
        for sampleTaxonomy in taxonomy:
            fullClassification = True
            for i in range(0, len(taxaNames)):
                taxaName = taxaNames[i]
                if sampleTaxonomy[taxaName] is not None:
                    if currentTaxa[taxaName] is None or currentTaxa[taxaName]["name"] != sampleTaxonomy[taxaName]:
                        currentTaxa[taxaName] = {"taxa": taxaName, "name": str(sampleTaxonomy[taxaName])}
                        if i == 0:
                            data["children"].append(currentTaxa[taxaName])
                        else:
                            parentTaxon = taxaNames[i - 1]
                            if "children" not in currentTaxa[parentTaxon]:
                                currentTaxa[parentTaxon]["children"] = []
                            currentTaxa[parentTaxon]["children"].append(currentTaxa[taxaName])
                else:
                    currentTaxa[taxaNames[i - 1]]["size"] = int(sampleTaxonomy['read_count'])
                    fullClassification = False
                    break
                
            if fullClassification:
                currentTaxa['species']["size"] = int(sampleTaxonomy['read_count'])               
                
        taxJson = data

    return taxJson
           

@app.route('/download/<int:site_id>')
def download(site_id):

    locationSamples = Sample.query.filter(Location.id == Sample.location_id, Location.id == site_id)

    latestSample = locationSamples.order_by(Sample.date_gathered.desc()).first()

    response = Response()
    response.status_code = 200

    book = Workbook()
    sheet1 = book.add_sheet('Sheet 1')

    headingStyle = easyxf('align: vertical center, horizontal center;font: height 250;')
    

    subHeadingStyle = easyxf('font: bold True;')
    dataStyle = easyxf('align: vertical center, horizontal right;')

    startCol = 0;
    sheet1.write_merge(0,0,startCol,startCol+1,'Location',headingStyle)

    latLng = ""
    if latestSample.location.access == "PRIVATE":
        latLng = "Private Property"
    else:
        latLng = str(latestSample.location.lat) + "," + str(latestSample.location.lng)

    locationTuples = [('Feature Name',latestSample.location.feature_name),
                      ('District',latestSample.location.district),
                      ('Feature System',latestSample.location.feature_system),
                      ('Feature Location',latestSample.location.location),
                      ('Description',latestSample.location.description),
                      ('Lat/Lng',latLng),
                      ('Access',str(latestSample.location.access))]
    i=1
    for d in locationTuples:
        sheet1.row(i).write(startCol,d[0],subHeadingStyle)
        sheet1.row(i).write(startCol+1,d[1],dataStyle)
        i+=1

    startCol+=2

    sheet1.write_merge(0,0,startCol,startCol+1,'Physical Measurements',headingStyle)     

    physDataTuples = [('Initial Temp',latestSample.phys.initialTemp),
              ('Sample Temp',latestSample.phys.sampleTemp),
              ('pH',latestSample.phys.pH),
              ('Redox',latestSample.phys.redox),
              ('Dissolved Oxygen',latestSample.phys.dO),
              ('Conductivity', latestSample.phys.conductivity), 
              ('Size',latestSample.phys.size),
              ('Colour',"#"+latestSample.phys.colour),
              ('Ebullition', latestSample.phys.ebullition), 
              ('Turbidity', latestSample.phys.turbidity),
              ('DNA Volume', latestSample.phys.dnaVolume), 
              ('Ferrous Iron',latestSample.phys.ferrousIronAbs)]

    i=1
    for d in physDataTuples:
        sheet1.row(i).write(startCol,d[0],subHeadingStyle)
        sheet1.row(i).write(startCol+1,d[1],dataStyle)
        i+=1   

    startCol+=2 

    sheet1.write_merge(0,0,startCol,startCol+1,'Image',headingStyle)

    imageTuples = [("Image",latestSample.image[1].image_path)]

    i=1
    for d in imageTuples:
        sheet1.row(i).write(startCol,d[0],subHeadingStyle)
        sheet1.row(i).write(startCol+1,d[1],dataStyle)
        i+=1 


    sheet1.col(0).width = 5000
    sheet1.col(1).width = 5000
    sheet1.col(2).width = 5000
    sheet1.col(3).width = 5000



    

    output = StringIO.StringIO()
    book.save(output)
    response.data = output.getvalue()

    filename = 'samplesite_'+str(site_id)+'.xls'
    mimetype_tuple = mimetypes.guess_type(filename)

    #HTTP headers for forcing file download
    response_headers = Headers({
            'Pragma': "public",  # required,
            'Expires': '0',
            'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
            'Cache-Control': 'private',  # required for certain browsers,
            'Content-Type': mimetype_tuple[0],
            'Content-Disposition': 'attachment; filename=\"%s\";' % filename,
            'Content-Transfer-Encoding': 'binary',
            'Content-Length': len(response.data)
        })

    if not mimetype_tuple[1] is None:
        response.update({
                'Content-Encoding': mimetype_tuple[1]
            })

    response.headers = response_headers

    #as per jquery.fileDownload.js requirements
    response.set_cookie('fileDownload', 'true', path='/')

    ################################
    # Return the response
    #################################
 
    return response

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

@app.route('/chemistryJson/<sampleNumber>')
def getChemistryJson(sampleNumber):
    sample = Sample.query.filter(Sample.sample_number == sampleNumber).first()
    chemJson = __getChemistryData(sample)
    if chemJson is None:
        return "No chemistry data for "+sampleNumber, 404
    
    return __cacheableResponse(jsonify(chemJson), 1)

@app.route('/taxonomyJson/<sampleNumber>')
def getTaxonomyJson(sampleNumber):
    sample = Sample.query.filter(Sample.sample_number == sampleNumber).first()
    taxJson = __getTaxonomyData(sample)
    if taxJson is None:
        return "No taxonomy data for "+sampleNumber, 404
    
    return __cacheableResponse(jsonify(taxJson), 1)
    

@app.route('/taxon/<name>')
def getTaxonDetails(name):
    try:
        data = json.load(urllib2.urlopen('https://www.googleapis.com/freebase/v1/topic/en/'+name.lower()))
        description = data['property']['/common/topic/description']['values'][0]['value']
        try:
            rank = data['property']['/biology/organism_classification/rank']['values'][0]['text']
        except KeyError:
            rank = None
        try:
            imageId =  data['property']['/common/topic/image']['values'][0]['id']
            imageUrl = 'https://usercontent.googleapis.com/freebase/v1/image' + imageId
        except KeyError:
            imageUrl=None     
        try:
            wikiUrl = data['property']['/common/topic/description']['values'][0]['citation']['uri'];
        except KeyError: 
            wikiUrl=None
        
        response = render_template('taxonDetails.html', taxon=name, rank=rank, description=description, imageUrl=imageUrl, wikiUrl=wikiUrl)
        return __cacheableResponse(response, 7)
            
    except:
        return render_template('taxonDetails.html', error=True)
    
     
def __cacheableResponse(response, expiryDays):
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=expiryDays)
    response = make_response(response)    
    response.headers["Expires"] = expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    response.headers['Cache-Control'] = 'max-age='+str(expiryDays*24*60*60)
    return response

def d(o):
    app.logger.debug(o)

if __name__ == "__main__":
    app.run()
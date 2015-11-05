import MySQLdb
import datetime
import time
from xlwt import Workbook, XFStyle, Alignment, easyxf
import os
import StringIO
import mimetypes
from hotspringsapp import app
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from flask.ext.sqlalchemy import get_debug_queries
from werkzeug.datastructures import Headers
import json
import urllib2,urllib
from collections import OrderedDict
import re
import traceback
import httplib

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


@app.route('/mapresults')
def mapResults():

    return "Not working yet"

@app.route('/mapsearch')
def mapsearch():

    locations = Location.query.filter(Sample.location_id == Location.id)
    return render_template('mapsearch.html',positions=locations)


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

    latestSampleIds = Location.latestSampleIdsAllLocations()

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

    count = {'1-25':0,'26-50':0,'51-75':0,'76-100':0}
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

    locations = Location.query.with_entities(Location.district).group_by(Location.district)
    locations = [i[0] for i in locations if i[0] != None]

    return render_template('simpleresults.html',entries=paginatedSamples,
                                                form=form,
                                                minTemp=minTemp,
                                                maxTemp=maxTemp,
                                                pieChart=pieChart,
                                                locations=locations
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

    #"Chemical_data.<elementname>" -> "<elementname>"| we don't want to show ID or elements not actually tested for
    # Remove 'cobolt' and replace it with 'Co'
    skippedCols = ['id', 'N', 'P', 'Cl', 'C', 'In', 'Ti', 'Bi', 'La']
    digitRegex = re.compile('[0-9]{1}')
    chemMap = getChemMap()
    chemCols = {}
    for x in Chemical_data.__table__.columns:
        chem = str(x).split('.')[1]
        if chem not in skippedCols:
            if chem in chemMap:
                chemCols[chem] = chemMap[chem]
            else:
                chemName = chem.capitalize() if len(chem) > 3 else chem
                chemCols[chem] = digitRegex.sub(subscriptDigit, chemName)
            
    chemNames = OrderedDict(sorted(chemCols.items(), key=lambda item: item[1].lower()))
    taxLvls = ["domain","phylum"]
    query = db.session.query(Taxonomy.domain.distinct().label("domain"))

    taxNames = [row.domain for row in query.all()]

    return render_template('dataoverview.html',
                           chemColumns=chemNames,
                           taxColumns=sorted(taxNames, key=lambda s: s.lower()),
                           taxLevels=sorted(taxLvls, key=lambda s: s.lower()))

def subscriptDigit(match):
    return unichr(8320 + int(match.group()))

def getChemMap():
    chemMap = {
            'Al': 'Aluminium',
            'NH4': 'Ammonium',
            'As': 'Arsenic',
            'Ba': 'Barium',
            'HCO3': 'Bicarbonate',
            'B': 'Boron',
            'Br': 'Bromine',
            'Cd': 'Cadmium',
            'Cs': 'Caesium',
            'Ca': 'Calcium',
            'CO': 'Carbon Monoxide',
            'Cl': 'Chloride',
            'Cr': 'Chromium',
            'Co': 'Cobalt',
            'Cu': 'Copper',
            'iron2': 'Ferrous Iron',
            'H2': 'Hydrogen',
            'H2S': 'Hydrogen Sulphide',
            'Fe': 'Iron',
            'Pb': 'Lead',
            'Li': 'Lithium',
            'Mg': 'Magnesium',
            'Mn': 'Manganese',
            'Hg': 'Mercury',
            'CH4': 'Methane',
            'Mo': 'Molybdenum',
            'Ni': 'Nickel',
            'NO3': 'Nitrate',
            'NO2': 'Nitrite',
            'PO4': 'Phosphate',
            'K': 'Potassium',
            'Rb': 'Rudibium',
            'Se': 'Selenium',
            'Si': 'Silicon',
            'Ag': 'Silver',
            'Na': 'Sodium',
            'Sr': 'Strontium',
            'SO4': 'Sulphate',
            'S': 'Sulpur',
            'Tl': 'Thallium',
            'U': 'Uranium',
            'V': 'Vanadium',
            'Zn': 'Zinc'  
        }
    return chemMap
    
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

    if latestSample.hasTaxonomy():
        gatheredInfoCount+= 1

    gatheredInfoCount -= 1

    largeImage = None
    bestPhotoImage = None
    for image in latestSample.image:
        if image.image_type == 'BESTPHOTO':
            bestPhotoImage = image
        elif image.image_type == 'LARGE':
            largeImage = image

    return render_template('samplesite.html',sample_site=latestSample, statusPos = gatheredInfoCount,largeImage=largeImage, bestPhotoImage=bestPhotoImage)

def __getChemistryData(sample):
    chemJson = {"name":"", "children":[{"name":"", "children":[]}]};
    if sample.chem is not None:
        chemMap = getChemMap()
        allSpecies = sample.chem.returnElements() + sample.chem.returnGases() + sample.chem.returnCompounds()
        for e in allSpecies:
            if e[1] != None and e[1] > 0:
                name = chemMap[e[0]] if e[0] in chemMap else e[0]
                chemJson["children"][0]["children"].append({"name":name.lower(),"size":e[1]})

    else:
        chemJson = None

    return chemJson

def __getTaxonomyData(sample):
    # The sample.getTaxonomy() query is very slow even if there is no
    # taxonomy data (since it queries a view), so we do the fast
    # hasTaxonomy() query first to avoid a slow response for
    # samples that don't have any taxonomy data.
    taxonomy = sample.getTaxonomy() if sample.hasTaxonomy() else []
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
    taxJson = __getCachedTaxononyJson(sample)  
    if taxJson is None:
        return "No taxonomy data for "+sampleNumber, 404

    return __cacheableResponse(jsonify(taxJson), 1)

@app.route('/clearTaxonomyCache')
def clearTaxonomyCache():
    return "Taxonomy cache cleared"
        
def __getCachedTaxononyJson(sample):
    cacheKey = 'taxonomy_' + sample.sample_number
    taxJson = app.taxonSummaryCache.get(cacheKey)
    if (taxJson is None):
        app.logger.debug('Taxonomy cache miss: '+sample.sample_number)
        taxJson = __getTaxonomyData(sample)  
        app.taxonSummaryCache.set(cacheKey, taxJson) # cache indefinitely
    else:
        app.logger.debug('Taxonomy cache hit: '+sample.sample_number)
        
    return taxJson  
    

@app.route('/overviewGraphJson/<element>')
def getOverviewGraphJson(element):

    latestSampleIds = Location.latestSampleIdsAllLocations()

    sample = Sample.query.with_entities(Physical_data.initialTemp,Physical_data.pH,Sample.id,getattr(Chemical_data,element),Location.id).filter(Sample.phys_id == Physical_data.id,Chemical_data.id == Sample.chem_id,Sample.id.in_(latestSampleIds),Sample.location_id == Location.id).order_by(getattr(Chemical_data,element))

    data = {"plots":[]}
    graphResults = sample.all()
    counter = 0
    for x in graphResults:
        data["plots"].append({'temperature':x[0],'pH':x[1],'id':x[4],'value':x[3],'index':counter})
        counter += 1


    return __cacheableResponse(jsonify(data), 1)

@app.route('/overviewTaxonTypes/<taxonLvl>')
def getOverviewTaxonLvl(taxonLvl):
    return __cacheableResponse(jsonify(__getOverviewTaxonLvl(taxonLvl)), 1)


def __getOverviewTaxonLvl(taxonLvl):
    query = db.session.query(getattr(Taxonomy,taxonLvl).distinct().label(taxonLvl)).all()
    data = [x[0] for x in query]
    return {"types": sorted(data, key=lambda s: s.lower())}    


@app.route('/overviewTaxonGraphJson/<buglevel>/<bugtype>')
def getOverviewGraphTaxonJson(buglevel, bugtype):
    # prevent SQL injection
    if not (buglevel == 'domain' or buglevel =='phylum'):
        raise Exception("Invalid taxonomy level("+buglevel+"), must be domain or phylum")
    taxJson = __getCachedOverviewGraphTaxonJson(buglevel, bugtype)
    return __cacheableResponse(jsonify(taxJson), 1)


@app.route('/clearTaxonomyOverviewCache')
def clearTaxonomyOverviewCache():
    app.taxonOverviewCache.clear()
    return "Taxonomy cache cleared"
           
        
def __getCachedOverviewGraphTaxonJson(buglevel, bugtype):
    cacheKey = 'taxonomyOverview_' + buglevel + '_' + bugtype
    taxJson = app.taxonOverviewCache.get(cacheKey)
    if (taxJson is None):
        app.logger.debug('Taxonomy overview cache miss: '+buglevel+', '+bugtype)
        taxJson = __getOverviewGraphTaxonJson(buglevel, bugtype)  
        app.taxonOverviewCache.set(cacheKey, taxJson)
    else:
        app.logger.debug('Taxonomy overview cache hit: '+buglevel+', '+bugtype)
        
    return taxJson 

    
def __getOverviewGraphTaxonJson(buglevel, bugtype):    

    query = text(
        """select s.id, s.location_id, p.pH, p.initialTemp,
            sum(st.read_count) as total_count,
            sum( if(t."""+buglevel+""" = :bugtype, st.read_count, 0)) as subset_count
        from public_sample s
        join physical_data p on s.phys_id = p.id
        join sample_taxonomy st on s.id=st.sample_id
        join taxonomy t on st.taxonomy_id = t.id 
        group by s.id, s.location_id, p.pH, p.initialTemp
        order by s.id"""
    )
    
    results = db.engine.execute(query, bugtype=bugtype).fetchall()

    mapping = ["id","location_id","pH","temp","total_count","subset_count"]
    data = {"plots":[]}

    for index, r in enumerate(results):
        row = dict(zip(mapping,r))
        percent = row['subset_count']/row['total_count']
        data["plots"].append({'temperature':row["temp"],'pH':row["pH"],'id':row["location_id"],'value':int(percent*100),'index':index})

    return data


@app.route('/taxon/<name>')
def getTaxonDetails(name):
    googleUrl='https://www.google.co.nz/search?ie=UTF-8&q='+name;
    wikiUrl=None
    try:
        try:
            conn = httplib.HTTPSConnection("en.wikipedia.org")
            conn.request("HEAD", "/wiki/"+name)
            wikiResponse = conn.getresponse()
            if (wikiResponse.status == 200):
                wikiUrl='https://en.wikipedia.org/wiki/'+name
        except:
            traceback.print_exc()
                      
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
            
        if wikiUrl is None:    
            try:
                wikiUrl = data['property']['/common/topic/description']['values'][0]['citation']['uri']
            except KeyError:
                try:
                    for values in data['property']['/common/topic/topic_equivalent_webpage']['values']:
                        if values['value'].startswith('http://en.wikipedia.org'):
                            wikiUrl = values['value']
                except KeyError:    
                    wikiUrl=None

        response = render_template('taxonDetails.html', taxon=name, rank=rank, description=description, imageUrl=imageUrl, wikiUrl=wikiUrl, googleUrl=googleUrl)
        return __cacheableResponse(response, 7)

    except:        
        return render_template('taxonDetails.html', error=True, wikiUrl=wikiUrl, googleUrl=googleUrl)


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

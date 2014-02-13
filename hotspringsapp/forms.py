from wtforms import TextField, BooleanField, IntegerField, HiddenField, RadioField
from flask.ext.wtf import Form

class SearchForm(Form):
	city = TextField('City')
	minTemp = IntegerField('minTemp')
	maxTemp = IntegerField('maxTemp')
	minPH = IntegerField('minPH')
	maxPH = IntegerField('maxPH')
	minTurb = IntegerField('minTurb')
	maxTurb = IntegerField('maxTurb')
	minCond = IntegerField('minCond')
	maxCond = IntegerField('maxCond')




	
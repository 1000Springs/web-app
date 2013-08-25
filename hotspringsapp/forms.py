from wtforms import TextField, BooleanField, IntegerField, HiddenField
from flask.ext.wtf import Required, Form

class SearchForm(Form):
	city = TextField('City')
	minTemp = IntegerField('minTemp')
	maxTemp = IntegerField('maxTemp')
	toilet = BooleanField('toilet', default = False)
	bench = BooleanField('bench', default = False)
	
	track = BooleanField('track', default = False)
	private = BooleanField('private', default = False)



	
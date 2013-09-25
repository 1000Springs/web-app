from wtforms import TextField, BooleanField, IntegerField, HiddenField, RadioField
from flask.ext.wtf import Form

class SearchForm(Form):
	city = TextField('City')
	minTemp = IntegerField('minTemp')
	maxTemp = IntegerField('maxTemp')
	filters = RadioField('Filters', choices=[('all', 'All'), ('PUBLIC_FREE', 'Free'), ('PUBLIC_PAID', 'Paid')])



	
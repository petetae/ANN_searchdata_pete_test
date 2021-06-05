from ANN_pete_webdata import app

import json, plotly
from flask import render_template, request, Response, jsonify
from .scripts.data_file import return_figures


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():

	# List of countries for filter
	searchText = ''
	# Parse the POST request countries list
	
	if (request.method == 'POST') and request.form:
		print('POST request - ', request.form)
		searchText = request.form.get('searchName')
		figures = return_figures(searchText)
		
	# GET request returns all countries for initial page load
	else:
		print('Other request - ', request.form)
		# print('Other request 2- ', request.form['searchText'])

		figures = return_figures()
	print('xxx --- ', request.form.get('searchName'))
	# plot ids for the html id tag
	ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

	# Convert the plotly figures to JSON for javascript in html template
	figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

	return render_template('index.html', ids=ids,
		figuresJSON=figuresJSON,
		search_text=searchText
        )
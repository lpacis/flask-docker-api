from flask import render_template, request, url_for,jsonify
from app import app

#home endpoint
@app.route('/')
def home():
	return "Hello World!"


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

#sitemap endpoint
@app.route('/site-map')
def site_map():
	links = []

	#go over all of the rules
	for rule in app.url_map.iter_rules():
		if "GET" in rule.methods and has_no_empty_params(rule):
			url = rule.rule
			links.append(rule.endpoint)
	
	return jsonify({'endpoints':str(links)})

	
@app.route('/template')
def template():
	return render_template('home.html')


#example endpoint w/ get and post requests
@app.route('/example/endpoint', methods = ['POST', 'GET'])
def example_api_endpoint():
	if request.method == 'POST':
		return "You've made a POST request"
	else:
		return "You've made a GET request"
	return "some data."
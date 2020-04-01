from flask import render_template, request, url_for,jsonify, flash, send_from_directory, redirect
from random import randint
from time import strftime
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from app import app
import settings
import stripe
import datetime
from flask_mail import Mail, Message
from worker import celery
import os

#home endpoint
@app.route('/', methods=['GET', 'POST'])
def home():
	#example of logging to a file
	now = datetime.datetime.utcnow()
	form = request.form
	if request.method == 'POST':
		message = form['loggingText']
		#call the logger with the info level and logg a message.
		
		app.logger.info('Logging request to home at - ' + str(now) +' message - ' + str(message))
		
		flash('Check the log_file.log hot reload the project directory for your message!')
		
	return render_template('logs.html', form = form)

@app.route("/coupon", methods=['GET', 'POST'])
def coupon_page():
	form = request.form

	#if the method was a post request, then process the coupon creation.
	if request.method == 'POST':

		percent_off = form['percentOff']
		
		duration_in_months = form['durationInMonths']
		coupon_name = form['name']
		amount_off = form['amountOff']
		max_redemptions = form['maxRedemptions']
		duration = form['durationSelect']
		#default to US region?
		stripe.api_key = settings.STRIPE_API_KEYS['US']

		payload = {
			"name":coupon_name,
			"duration":duration
		}

		#create the coupon in stripe
		response = stripe.Coupon.create(
			name = coupon_name,
			duration = duration,
			duration_in_months = duration_in_months if duration_in_months else None,
			amount_off = amount_off if amount_off else None,
			percent_off = percent_off if percent_off else None,
			max_redemptions = max_redemptions if max_redemptions else None,
			currency = 'USD' #default for now since we are using the US API key for POC

		)

		flash(str(response))
	return render_template('coupon_form.html', form=form)

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

@app.route('/logs')
def get_logs():
	app.logger.info('Made it to the logging route')
	return send_from_directory('..', 'log_file.log', as_attachment = True)

#example endpoint w/ get and post requests
@app.route('/example/endpoint', methods = ['POST', 'GET'])
def example_api_endpoint():
	if request.method == 'POST':
		return "You've made a POST request"
	else:
		return "You've made a GET request"
	return "some data."

mail = Mail(app)
def send_mail(data):

	with app.app_context():
        
		msg = Message(subject="Hello",
		sender=app.config.get("MAIL_USERNAME"),
		recipients=[data['email']],
		body=data['message'])
		mail.send(msg)



@app.route('/background-task', methods =['GET', 'POST'])
def background_task():
	form = request.form
	if request.method == 'GET':
		return render_template('background.html', form = form)

	if request.method == 'POST':
		data = {}
		data['email'] = request.form['email']
		data['message'] = request.form['message']
		

		#add some numbers together and then send an email on the callback.
		task = celery.send_task('tasks.add', args=[1, 2], kwargs={}, link=send_mail(data))
		# send_mail.apply_async((data,), countdown=0)
		flash("Email will be sent to the address that is " + str(data['email']) + " in 2 minutes.")

		flash("Check the worker for the job - " + str(task))
		return redirect(url_for('background_task'))


		

from flask import Flask
import logging
import settings

logging.basicConfig(filename='log_file.log', level=settings.LOGGING_LEVELS['debug'])
app = Flask(__name__)
#some secret key generated from os.random
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['DEBUG'] = True
app.config.update(settings.MAIL_SETTINGS)
import views


import sys
import config

from flask import Flask
sys.path.append('../')

app = Flask(__name__, template_folder='./Templates')
app.config.from_object('config.DevelopmentConfig')

from . import models, views

app.run()
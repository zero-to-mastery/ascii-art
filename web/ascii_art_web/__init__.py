import sys

from flask import Flask
sys.path.append('../')

app = Flask(__name__, template_folder='./templates')
app.config.from_object('config.DevelopmentConfig')

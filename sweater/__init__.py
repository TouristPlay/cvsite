from flask import Flask, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__, static_url_path='/static')

UPLOAD_FOLDER = 'sweater\\static\\uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '5+d!_o-35o3(_t^dy$hraf!3hiz)(9)=irawqfgqu@5t-n3ym7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:root@localhost:5432/abrams'
app.debug = True


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from sweater import model, routes

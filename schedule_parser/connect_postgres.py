from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:mysecretpassword@localhost:5433/RTUSchedule"
db = SQLAlchemy(app)

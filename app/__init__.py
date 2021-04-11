from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
from os import environ 
from flasgger import Swagger, swag_from

template = {
  "swagger": "2.0",
  "info": {
    "title": "SCHEDULE-RTU",
    "description": "API for getting schedule for RTU MIREA",
    "version": "0.1.1",
    "contact": {
      "name": "Olya",
      "url": "https://vk.com/id196529353",
    }
  },
  "securityDefinitions": {
    "Bearer": {
      "type": "apiKey",
      "name": "Authorization",
      "in": "header",
      "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
    }
  },
  "security": [
    {
      "Bearer": [ ]
    }
  ]

}

app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'SHEDULE API',
    'uiversion': 3,
    "specs_route": "/api/schedule/swagger/"
}
swagger = Swagger(app, template= template)
app.config.from_object(config.Config)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('CONNECTION_STRING')
db = SQLAlchemy(app)

from app import views


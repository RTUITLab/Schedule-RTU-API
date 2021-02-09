from app import app
from flask import Flask, flash, request, redirect, url_for, session, jsonify, render_template, make_response
import requests
from os import environ  
import datetime
from schedule import today_sch, tomorrow_sch, week_sch
import sys

sys.path.append('..')
from schedule_parser.main import parse_schedule

####
@app.route('/<string:group>/today', methods=["GET"])
def today(group):
    """Today's schedule for requested group
    ---

    responses:
      200:
        description: Return string with today\'s schedule, split by \\n
        schema:
          type: object
          properties:
            schedule:
              type: string
        examples:
          rgb: ['red', 'green', 'blue']
    """

    sch = today_sch(group)
    if len(sch.split(" "))<2:
        sch = "Такой группы не существует"
    res = {'schedule': sch}
    response = jsonify(res)
    # return "today for{} is {}".format(group, res)
    return make_response(response)

#############
@app.route('/<string:group>/tomorrow', methods=["GET"])
def tomorrow(group):
    """Tomorrow's schedule for requested group
    ---

    responses:
      200:
        description: Return string with tomorrow\'s schedule, split by \\n
        schema:
          type: object
          properties:
            schedule:
              type: string
    """
    res = {'schedule': tomorrow_sch(group)}
    response = jsonify(res)
    # return "tomorrow for{} is {}".format(group, res)
    return make_response(response)

@app.route('/<string:group>/week', methods=["GET"])
def week(group):
    """Week's schedule for requested group
    ---

    responses:
      200:
        description: Return \'ok\' after updating
        schema:
          type: object
          properties:
            schedule:
              type: string
    """
    res = {'schedule': week_sch(group)}
    response = jsonify(res)
    # return "week for{} is {}".format(group, res)
    return make_response(response)

@app.route('/refresh', methods=["POST"])
def refresh():
    """Refresh shedule
    ---

    responses:
      200:
        description: String with Week\'s schedule, split by \\n
        schema:
          type: object
          properties:
            status:
              type: string
    """
    parse_schedule()
    return make_response({"status": 'ok'})
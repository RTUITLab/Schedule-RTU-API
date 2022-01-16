from app import app
from flask import Flask, flash, request, redirect, url_for, session, jsonify, render_template, make_response, Response
import requests
from os import environ
import datetime

from schedule import get_full_schedule_by_weeks, get_schedule_by_week, get_teachers, teacher_next_week_sch, teacher_today_sch, teacher_tomorrow_sch, teacher_week_sch, today_sch, tomorrow_sch, week_sch, next_week_sch, get_groups, full_sched, form_csv_new

import sys

sys.path.append('..')
from schedule_parser.main import parse_schedule

@app.route('/api/schedule/<string:group>/today', methods=["GET"])
def today(group):
    """Today's schedule for requested group
    ---
    tags:
      - OLD Groups
    parameters:
      - name: group
        in: path
        type: string
        required: true
      
    definitions:
      Lesson:
        type: object
        nullable: true
        properties:
          lesson:
            type: object
            properties:
              classRoom: 
                type: string
              name: 
                type: string
              teacher: 
                type: string
              type: 
                type: string
            
          time:
            type: object
            properties:
              start: 
                type: string
              end: 
                type: string

      TeacherLesson:
        type: object
        nullable: true
        properties:
          lesson:
            type: object
            properties:
              classRoom: 
                type: string
              name: 
                type: string
              type: 
                type: string
            
          time:
            type: object
            properties:
              start: 
                type: string
              end: 
                type: string
                
      Week: 
        type: object
        properties:
          monday:
            type: array
            items:
              $ref: '#/definitions/Lesson'
          tuesday:
            type: array
            items:
              $ref: '#/definitions/Lesson'
          wednesday: 
            type: array
            items:
              $ref: '#/definitions/Lesson'
          thursday:
            type: array
            items:
              $ref: '#/definitions/Lesson'
          friday: 
            type: array
            items:
              $ref: '#/definitions/Lesson'
          saturday:
            type: array
            items:
              $ref: '#/definitions/Lesson'

      FullSchedule:
        type: object
        nullable: true
        properties:
          first:
            $ref: '#/definitions/Week'
          second:
            $ref: '#/definitions/Week'


      TeacherWeek: 
        type: object
        properties:
          monday:
            type: array
            items:
              $ref: '#/definitions/TeacherLesson'
          tuesday:
            type: array
            items:
              $ref: '#/definitions/TeacherLesson'
          wednesday: 
            type: array
            items:
              $ref: '#/definitions/TeacherLesson'
          thursday:
            type: array
            items:
              $ref: '#/definitions/TeacherLesson'
          friday: 
            type: array
            items:
              $ref: '#/definitions/TeacherLesson'
          saturday:
            type: array
            items:
              $ref: '#/definitions/TeacherLesson'

      TeacherFullSchedule:
        type: object
        nullable: true
        properties:
          first:
            $ref: '#/definitions/TeacherWeek'
          second:
            $ref: '#/definitions/TeacherWeek'

            
      AllWeeks:
        type: array
        items:
          $ref: '#/definitions/Week'

      TeacherAllWeeks:
        type: array
        items:
          $ref: '#/definitions/TeacherWeek'

      Number: 
        type: object
        properties:
          number:
            type: integer
          group:
            type: string


      Direction:
        type: object
        properties:
          name: 
            type: string
          numbers:
            type: array
            items:
              $ref: '#/definitions/Number'
                      
      LiteDirection:
        type: object
        properties:
          name: 
            type: string
          numbers:
            type: array
            items:
              type: string

      Groups:
        type: object
        properties:
          bachelor:
            type: object
            properties:
              first:
                type: array
                items:
                  $ref: '#/definitions/LiteDirection'
              second:
                type: array
                items:
                  $ref: '#/definitions/LiteDirection'
              third:
                type: array
                items:
                  $ref: '#/definitions/LiteDirection'
              fourth:
                type: array
                items:
                  $ref: '#/definitions/LiteDirection'
          master:
            type: object
            properties:
              first:
                type: array
                items:
                  $ref: '#/definitions/LiteDirection'
              second:
                type: array
                items:
                  $ref: '#/definitions/LiteDirection'                    


    responses:
      200:
        description: Return today\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair 
        schema:
          type: array
          items:
            $ref: '#/definitions/Lesson'
          minItems: 8
          maxItems: 8
            
      503:
          description: Retry-After:100
    """

    sch = today_sch(group)
    if sch:
      response = jsonify(sch)
      # return "today for{} is {}".format(group, res)
      return make_response(response)
    res = Response(headers={'Retry-After':200}, status=503)
    return res

@app.route('/api/schedule/<string:group>/tomorrow', methods=["GET"])
def tomorrow(group):
    """Tomorrow's schedule for requested group
    ---
    tags:
      - OLD Groups
    parameters:
      - name: group
        in: path
        type: string
        required: true

    responses:
      200:
        description: Return tomorrow\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair 
        schema:
          type: array
          items:
            $ref: '#/definitions/Lesson'
          minItems: 8
          maxItems: 8
            
      503:
          description: Retry-After:100
    """
    res = tomorrow_sch(group)
    if res:
      response = jsonify(res)
      # return "tomorrow for{} is {}".format(group, res)
      return make_response(response)
    res = Response(headers={'Retry-After':200}, status=503)
    return res

@app.route('/api/schedule/<string:group>/week', methods=["GET"])
def week(group):
    """Current week's schedule for requested group
    ---
    tags:
      - OLD Groups
    parameters:
      - name: group
        in: path
        type: string
        required: true
      
    responses:
      200:
        description: Return week\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair.
        schema:
          $ref: '#/definitions/Week'
            
      503:
          description: Retry-After:100
    """
    res =  week_sch(group)
    if res:
      response = jsonify(res)
      # return "tomorrow for{} is {}".format(group, res)
      return make_response(response)
    res = Response(headers={'Retry-After':200}, status=503)
    return res


@app.route('/api/schedule/get_groups', methods=["GET"])
def groups():
  """List of groups in IIT
    ---
    tags:
      - OLD Groups
    responses:
      200:
        description: Return all groups in IIT.
        schema:
          $ref: '#/definitions/Groups'

            
      503:
          description: Retry-After:100
  """
  res =  get_groups()
  if res:
    response = jsonify(res)
    print(res)
    # return "tomorrow for{} is {}".format(group, res)
    return make_response(response)
  res = Response(headers={'Retry-After':200}, status=503)
  return res


@app.route('/api/schedule/<string:group>/next_week', methods=["GET"])
def next_week(group):
    """Next week's schedule for requested group
    ---
    tags:
      - OLD Groups
    parameters:
      - name: group
        in: path
        type: string
        required: true
      
    responses:
      200:
        description: Return week\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair.
        schema:
          $ref: '#/definitions/Week'
            
      503:
          description: Retry-After:100
    """
    res =  next_week_sch(group)
    if res:
      response = jsonify(res)
      # return "tomorrow for{} is {}".format(group, res)
      return make_response(response)
    res = Response(headers={'Retry-After':200}, status=503)
    return res

@app.route('/refresh', methods=["POST"])
def refresh():
    """Refresh shedule
    ---
    tags:
      - Refresh
    responses:
      200:
        description: Return \'ok\' after updating
        schema:
          type: object
          properties:
            status:
              type: string
    """
    parse_schedule()
    return make_response({"status": 'ok'})

@app.route('/api/schedule/secret_refresh', methods=["POST"])
def secret_refresh():
    """Refresh shedule
    ---
    tags:
      - Refresh
    parameters:
        - in: header
          name: X-Auth-Token
          type: string
          required: true

    responses:
      200:
        description: Return \'ok\' after updating
        schema:
          type: object
          properties:
            status:
              type: string
    """
    try:
      secret = request.headers.get('X-Auth-Token')
      SECRET_FOR_REFRESH = environ.get('SECRET_FOR_REFRESH')
      if secret == SECRET_FOR_REFRESH:
        parse_schedule()
        return make_response({"status": 'ok'})
      return make_response({"status": 'wrong_password'}, 401)
    except:
      return make_response({"status": 'need_password'})

@app.route('/api/schedule/<string:group>/full_schedule', methods=["GET"])
def full_schedule(group):
  """Current week's schedule for requested group
    ---
    tags:
      - OLD Groups
    parameters:
      - name: group
        in: path
        type: string
        required: true
      
    responses:
      200:
        description: Return full schedule of one group. 
        schema:
          $ref: '#/definitions/FullSchedule'
            
      503:
          description: Retry-After:100
  """
  sch = full_sched(group)
  if sch:
    response = jsonify(sch)
    # return "today for{} is {}".format(group, res)
    return make_response(response)
  res = Response(headers={'Retry-After':200}, status=503)
  return res

@app.route('/api/schedule/<string:group>/<int:max_weeks>/all_weeks', methods=["GET"])
def get_all_weeks_schedule(group, max_weeks):
  """Returns all weeks up to max_weeks
    ---
    tags:
      - OLD Groups
    parameters:
      - name: group
        in: path
        type: string
        required: true
      - name: max_weeks
        in: path
        type: integer
        required: true
        description: The number of consecutive weeks returned
      
    responses:
      200:
        description: Return full schedule of one group. 
        schema:
          $ref: '#/definitions/AllWeeks'
            
      503:
          description: Retry-After:100
  """
  sch = get_full_schedule_by_weeks(group, max_weeks)
  if sch:
    response = jsonify(sch)
    return make_response(response)
  res = Response(headers={'Retry-After': 200}, status=503)
  return res

@app.route('/api/schedule/<string:group>/<int:week>/week_num', methods=["GET"])
def get_week_schedule_by_week_num(group, week):
  """Returns week schedule by week number
    ---
    tags:
      - OLD Groups
    parameters:
      - name: group
        in: path
        type: string
        required: true
      - name: week
        in: path
        type: integer
        required: true
      
    responses:
      200:
        description: Return full schedule of one group. 
        schema:
          $ref: '#/definitions/Week'
            
      503:
          description: Retry-After:100
  """
  sch = get_schedule_by_week(group, week)
  if sch:
    response = jsonify(sch)
    return make_response(response)
  res = Response(headers={'Retry-After': 200}, status=503)
  return res


# @app.route('/api/schedule/schedule_for_cache', methods=["GET"])
# def schedule_for_cache():

#   sch = for_cache()
#   if sch:
#     response = jsonify(sch)
#     # return "today for{} is {}".format(group, res)
#     return make_response(response)
#   res = Response(headers={'Retry-After':200}, status=503)
#   return res


@app.route('/api/schedule/teachers/get_teachers', methods=["GET"])
def teachers():
  """List of teachers in IIT
    ---
    tags:
        - OLD Teachers 
    responses:
      200:
        description: Return all teachers in IIT.
        schema:
          type: array
          items: 
            type: string
      503:
          description: Retry-After:100
  """
  res = get_teachers()
  if res:
    response = jsonify(res)
    print(res)
    return make_response(response)
  res = Response(headers={'Retry-After':200}, status=503)
  return res


@app.route('/api/schedule/teachers/<string:teacher>/today', methods=["GET"])
def teacher_today(teacher):
    """Today's schedule for requested teacher
    ---
    tags:
      - OLD Teachers
    parameters:
      - name: teacher
        in: path
        type: string
        required: true

    responses:
      200:
        description: Return today\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair 
        schema:
          type: array
          items:
            $ref: '#/definitions/TeacherLesson'
          minItems: 8
          maxItems: 8
            
      503:
          description: Retry-After:100
    """
    sch = teacher_today_sch(teacher)
    if sch:
      response = jsonify(sch)
      # return "today for{} is {}".format(group, res)
      return make_response(response)
    res = Response(headers={'Retry-After':200}, status=503)
    return res

@app.route('/api/schedule/teachers/<string:teacher>/tomorrow', methods=["GET"])
def teacher_tomorrow(teacher):
    """Tomorrow's schedule for requested teacher
    ---
    tags:
      - OLD Teachers
    parameters:
      - name: teacher
        in: path
        type: string
        required: true

    responses:
      200:
        description: Return tomorrow\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair 
        schema:
          type: array
          items:
            $ref: '#/definitions/TeacherLesson'
          minItems: 8
          maxItems: 8
            
      503:
          description: Retry-After:100
    """
    res = teacher_tomorrow_sch(teacher)
    if res:
      response = jsonify(res)
      # return "tomorrow for{} is {}".format(group, res)
      return make_response(response)
    res = Response(headers={'Retry-After':200}, status=503)
    return res

@app.route('/api/schedule/teachers/<string:teacher>/week', methods=["GET"])
def teacher_week(teacher):
    """Current week's schedule for requested teacher
    ---
    tags:
      - OLD Teachers
    parameters:
      - name: teacher
        in: path
        type: string
        required: true
      
    responses:
      200:
        description: Return week\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair.
        schema:
          $ref: '#/definitions/TeacherWeek'
            
      503:
          description: Retry-After:100
    """
    res = teacher_week_sch(teacher)
    if res:
      response = jsonify(res)
      # return "tomorrow for{} is {}".format(group, res)
      return make_response(response)
    res = Response(headers={'Retry-After':200}, status=503)
    return res


@app.route('/api/schedule/teachers/<string:teacher>/next_week', methods=["GET"])
def teacher_next_week(teacher):
    """Next week's schedule for requested teacher
    ---
    tags:
      - OLD Teachers
    parameters:
      - name: teacher
        in: path
        type: string
        required: true
      
    responses:
      200:
        description: Return week\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair.
        schema:
          $ref: '#/definitions/TeacherWeek'
            
      503:
          description: Retry-After:100
    """
    res = teacher_next_week_sch(teacher)
    if res:
      response = jsonify(res)
      # return "tomorrow for{} is {}".format(group, res)
      return make_response(response)
    res = Response(headers={'Retry-After':200}, status=503)
    return res


@app.route('/form_csv', methods=["POST"])
def csv():
    """Refresh shedule
    ---
    responses:
      200:
        description: Return \'ok\' after updating
        schema:
          type: object
          properties:
            status:
              type: string
    """
    form_csv_new()
    return make_response({"status": 'ok'})
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.jjjjs import Jjjj

jjjj_api = Blueprint('jjjj_api', __name__,
                   url_prefix='/api/jjjjs')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(jjjj_api)

class JjjjAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            # validate uid
            score = body.get('score')
            if score is None or len(score) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Jjjj(name=name, 
                      score=score)
            
            ''' Additional garbage error checking '''
            # set password if provided
            ''' #2: Key Code block to add user to database '''
            # create user in database
            jjjj = uo.create()
            # success returns json of user
            if jjjj:
                return jsonify(jjjj.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {score} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            jjjjs = Jjjj.query.all()    # read/extract all users from database
            json_ready = [jjjj.read() for jjjj in jjjjs]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
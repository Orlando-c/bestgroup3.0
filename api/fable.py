from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.fable import Fable

fable_api = Blueprint('fable_api', __name__,
                   url_prefix='/api/fable')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(fable_api)

class FableAPI:        
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
            uo = Fable(name=name, 
                      score=score)
            
            ''' Additional garbage error checking '''
            # set password if provided
            ''' #2: Key Code block to add user to database '''
            # create user in database
            fable = uo.create()
            # success returns json of user
            if fable:
                return jsonify(fable.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {score} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            fables = Fable.query.all()    # read/extract all users from database
            json_ready = [fable.read() for fable in fables]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
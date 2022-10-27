from flask import Flask, jsonify
from flask_restx import Resource, Api


# instantiate the app
app = Flask(__name__)

api = Api(app)


class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'Does this work?'
        }

app.config.from_object('src.config.DevelopmentConfig')

api.add_resource(Ping, '/ping')
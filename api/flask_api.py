"""
Brevets RESTful API
Name: Ethan Robb
"""
import os
from flask import Flask
from flask_restful import Api
from mongoengine import connect
from flask_cors import CORS
from os import environ as env
# You need to implement two resources: Brevet and Brevets.
from resources.brevet import Brevet
from resources.brevets import Brevets

connect(host=f"mongodb://{os.environ['MONGODB_HOSTNAME']}:27017/brevetsdb")

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:5002"}})

api.add_resource(Brevet, "/api/brevet/<string:brevet_id>")
api.add_resource(Brevets, "/api/brevets")

if __name__ == "__main__":
    # Run flask app normally
    # Read DEBUG and PORT from environment variables.
    print(f"Opening for global access on port {env['PORT']}")
    app.run(port=int(env["PORT"]), host="0.0.0.0")

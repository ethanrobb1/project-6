"""
Resource: Brevets
Name: Ethan Robb
"""
from flask import Response, request
from flask_restful import Resource
from mongoengine.errors import ValidationError

# You need to implement this in database/models.py
from database.models import Brevet

class Brevets(Resource):
    def get(self):
        """
        Get all brevets in the database
        """
        try:
            return Response(Brevet.objects.to_json(), mimetype="application/json", status=200)
        except Exception as exc:
            return {"error": str(exc)}, 500

    def post(self):
        """
        Post a new brevet in the database
        """
        try:
            new_doc = Brevet(**request.json).save(validate=True)
            return {"id": str(new_doc.id)}, 201
        except ValidationError as exc:
            err_text = "Error" 
            return {"error": err_text}, 400
        except Exception as exc:
            return {"error": str(exc)}, 500

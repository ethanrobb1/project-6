"""
Resource: Brevet
Name: Ethan Robb
"""
from flask import Response, request
from flask_restful import Resource
from database.models import Brevet
from mongoengine.errors import DoesNotExist, ValidationError

# You need to implement this in database/models.py
from database.models import Brevet

class Brevet(Resource):
    def get(self, brevet_id: str):
        """
        Get a brevet from the database
        """
        try:
            return Response(
                Brevet.objects.get(id=brevet_id).to_json(),
                mimetype="application/json",
                status=200
            )
        except DoesNotExist:
            return {"error": f"Brevet not found for id {brevet_id}."}, 404
        except ValidationError as exc:
            return {"error": str(exc)}, 400
        except Exception as exc:
            return {"error": str(exc)}, 500

    def put(self, brevet_id: str):
        """
        Swap a brevet in the database
        """
        try:
            Brevet(**request.json).validate()  
            docs_updated = Brevet.objects.get(id=brevet_id).update(
                __raw__={"$set": request.json}  
            )
            if docs_updated == 1:  
                return {"success": True}, 200
            else:  
                return {"error": "Internal Error"}, 500
        except DoesNotExist:
            return {"error": f"Brevet Not found for ID {brevet_id}."}, 404
        except ValidationError as exc:
            err_text = "\n".join(f"{str(k)}: {str(v)}" for k, v in exc.errors.items()) if exc.errors is not None \
                                                                                       else str(exc)
            return {"error": err_text}, 400
        except Exception as exc:
            return {"error": str(exc)}, 500

    def delete(self, brevet_id: str):
        """
        Delete a brevet from the database
        """
        try:
            Brevet.objects.get(id=brevet_id).delete()
            return {"success": True}, 200
        except DoesNotExist:
            return {"error": f"Brevet not found for id {brevet_id}."}, 404
        except ValidationError as exc:
            return {"error": str(exc)}, 400
        except Exception as exc:
            return {"error": str(exc)}, 500

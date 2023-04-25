from flask import Response, request
from flask_restful import Resource
from models import User
from views import get_authorized_user_ids
import json
import flask_jwt_extended

class SuggestionsListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        # suggestions should be any user with an ID that's not in this list:
        # print(get_authorized_user_ids(self.current_user))
        exclude_from = get_authorized_user_ids(current_user=self.current_user)
        all_users = User.query.all()
        user_suggestions = []
        for user in all_users:
            if user.id not in exclude_from:
                user_suggestions.append(user)
        del user_suggestions[7:]
        return Response(json.dumps([suggested_users.to_dict() for suggested_users in user_suggestions]), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint, 
        '/api/suggestions', 
        '/api/suggestions/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

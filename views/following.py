from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json
import flask_jwt_extended

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        # return all of the "following" records that the current user is following
        followings = Following.query.filter_by(user_id=self.current_user.id).all()
        return Response(json.dumps([f.to_dict_following() for f in followings]), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    def post(self):
        # create a new "following" record based on the data posted in the body 
        body = request.get_json()
        if len(body) == 0 or body.get("user_id") == None:
            return Response(json.dumps({ "msg": "invalid input" }), mimetype="application/json", status=400)
        user_id = body.get("user_id")
        try:
            user_id = int(user_id)
        except Exception as e:
            return Response(json.dumps({ "msg": f"invalid input: {e}" }), mimetype="application/json", status=400)
        
        user = User.query.get(user_id)
        if user == None:
            return Response(json.dumps({ "msg": "user not found" }), mimetype="application/json", status=404)

        checks = Following.query.filter_by(user_id=self.current_user.id, following_id=user_id).first()
        if checks != None:
            return Response(json.dumps({ "msg": "user already followed." }), mimetype="application/json", status=400)

        follow = Following(self.current_user.id, user_id)
        db.session.add(follow)
        db.session.commit()
        return Response(json.dumps(follow.to_dict_following()), mimetype="application/json", status=201)

class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # delete "following" record where "id"=id
        try:
            delete_id = int(id)
        except Exception as e:
            return Response(json.dumps({ "msg": f"invalid input: {e}" }), mimetype="application/json", status=400)
        
        unfollow = Following.query.get(delete_id)
        followings = Following.query.filter_by(user_id=self.current_user.id).all()
        if unfollow not in followings or unfollow == None:
            return Response(json.dumps({ "msg": "following not found" }), mimetype="application/json", status=404)
        
        db.session.delete(unfollow)
        db.session.commit()
        return Response(json.dumps({ "msg": "unfollowed successfully." }), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<int:id>', 
        '/api/following/<int:id>/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

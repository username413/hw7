from flask import Response, request
from flask_restful import Resource
from models import LikePost, db, Post
from views import get_authorized_user_ids
import json
import flask_jwt_extended

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def post(self):
        # create a new "like_post" based on the data posted in the body 
        body = request.get_json()
        post_id = body.get("post_id")
        if post_id == None:
            return Response(json.dumps({ "msg": "post not found"}), mimetype="application/json", status=404)
        try:
            post_id = int(post_id)
        except Exception as e:
            return Response(json.dumps({ "msg": f"invalid input {e}"}), mimetype="application/json", status=400)

        checks = LikePost.query.filter_by(user_id=self.current_user.id, post_id=post_id).first()
        if checks != None:
            post = Post.query.get(checks.post_id)
            authorized_users = get_authorized_user_ids(current_user=self.current_user)
            if post != None and post.user_id not in authorized_users:
                return Response(json.dumps({ "msg": "unauthorized access" }), mimetype="application/json", status=404)
            return Response(json.dumps({ "msg": "already liked" }), mimetype="application/json", status=400)
        
        post = LikePost.query.get(post_id)
        if post == None:
            return Response(json.dumps({ "msg": "post not found" }), mimetype="application/json", status=404)

        like = LikePost(self.current_user.id, post_id)
        db.session.add(like)
        db.session.commit()
        
        return Response(json.dumps(like.to_dict()), mimetype="application/json", status=201)

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # delete "like_post" where "id"=id
        try:
            delete_id = int(id)
        except Exception as e:
            return Response(json.dumps({ "msg": f"invalid input: {e}" }), mimetype="application/json", status=400)
        
        unlike = LikePost.query.get(delete_id)
        if unlike == None:
            return Response(json.dumps({ "msg": "like not found" }), mimetype="application/json", status=404)

        db.session.delete(unlike)
        db.session.commit()
        return Response(json.dumps({ "msg": "like deleted." }), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/likes', 
        '/api/posts/likes/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/likes/<int:id>', 
        '/api/posts/likes/<int:id>/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

from flask import Response, request
from flask_restful import Resource
import json
from models import db, Comment, Post
from views import get_authorized_user_ids

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        # create a new "Comment" based on the data posted in the body 
        body = request.get_json()
        if len(body) == 0 or body.get("post_id") == None or body.get("text") == None:
            return Response(json.dumps({ "msg": "invalid input" }), mimetype="application/json", status=400)
        try:
            post_id = int(body.get("post_id"))
        except Exception as e:
            return Response(json.dumps({ "msg": f"invalid input: {e}" }), mimetype="application/json", status=400)
        
        post = Post.query.get(post_id)
        authorized_users = get_authorized_user_ids(current_user=self.current_user)
        if post == None or post.user_id not in authorized_users:
            return Response(json.dumps({ "msg": "post not found or unauthorized access" }), mimetype="application/json", status=404)
        
        comment_in = Comment(body.get("text"), self.current_user.id, post_id)
        db.session.add(comment_in)
        db.session.commit()

        return Response(json.dumps(comment_in.to_dict()), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    def delete(self, id):
        # delete "Comment" record where "id"=id
        try:
            delete_id = int(id)
        except Exception as e:
            return Response(json.dumps({ "msg": f"invalid input: {e}" }), mimetype="application/json", status=400)

        comment = Comment.query.get(delete_id)
        if comment == None or comment.user_id != self.current_user.id:
            return Response(json.dumps({ "msg": "comment not found or unauthorized access" }), mimetype="application/json", status=404)
        
        db.session.delete(comment)
        db.session.commit()
        return Response(json.dumps({ "msg": "comment deleted." }), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': api.app.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<int:id>', 
        '/api/comments/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )

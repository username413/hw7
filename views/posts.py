from flask import Response, request
from flask_restful import Resource
from models import Post, db
from views import get_authorized_user_ids

import json

def get_path():
    return request.host_url + 'api/posts/'

class PostListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    def get(self):
        # get posts created by one of these users:
        authorized_users = get_authorized_user_ids(current_user=self.current_user)
        invalid_limit = { "msg": "invalid limit amount or type." }
        try:
            limit = int(request.args.get("limit", 20))
        except Exception as e:
            return Response(json.dumps(invalid_limit), mimetype="application/json", status=400)
        if limit > 50:
            return Response(json.dumps(invalid_limit), mimetype="application/json", status=400)
            
        posts = Post.query.filter(Post.user_id.in_(authorized_users)).limit(limit).all()
        return Response(json.dumps([post.to_dict() for post in posts]), mimetype="application/json", status=200)

    def post(self):
        # create a new post based on the data posted in the body 
        body = request.get_json()
        if body.get("image_url") == None or len(body) == 0:
            return Response(json.dumps({ "msg": "image_url is required" }), mimetype="application/json", status=400)    

        new_post = Post(
            image_url=body.get("image_url"),
            user_id=self.current_user.id,
            caption=body.get("caption") if body.get("caption") != None else None,
            alt_text=body.get("alt_text") if body.get("alt_text") != None else None
        )
        db.session.add(new_post)
        db.session.commit()

        return Response(json.dumps(new_post.to_dict()), mimetype="application/json", status=201)
        
class PostDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
        

    def patch(self, id):
        # update post based on the data posted in the body 
        body = request.get_json()
        post = Post.query.get(id)
        if post == None or post.user_id != self.current_user.id:
            return Response(json.dumps({ "msg": "post not found or unauthorized access" }), mimetype="application/json", status=404)
        elif body.get("image_url") == None or len(body) == 0:
            return Response(json.dumps({ "msg": "image_url is required" }), mimetype="application/json", status=400)
        
        post.image_url = body.get("image_url")
        post.caption = body.get("caption") if body.get("caption") != None else post.caption
        post.alt_text = body.get("alt_text") if body.get("alt_text") != None else post.alt_text
        db.session.commit()

        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)


    def delete(self, id):
        # delete post where "id"=id
        post = Post.query.get(id)
        if post == None or post.user_id != self.current_user.id:
            return Response(json.dumps({ "msg": "post not found or unauthorized access" }), mimetype="application/json", status=404)
        Post.query.filter_by(id=id).delete()
        db.session.commit()
        
        requery_post = Post.query.get(id)
        if requery_post != None:
            return Response(json.dumps({ "msg": "unable to delete post" }), mimetype="application/json", status=400)
            
        return Response(json.dumps({ "msg": f"post id {id} deleted." }), mimetype="application/json", status=200)


    def get(self, id):
        # get the post based on the id
        post = Post.query.get(id)
        authorized_users = get_authorized_user_ids(current_user=self.current_user)
        if post == None or post.user_id not in authorized_users:
            return Response(json.dumps({ "msg": "post not found or unauthorized access" }), mimetype="application/json", status=404)

        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(
        PostListEndpoint, 
        '/api/posts', '/api/posts/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        PostDetailEndpoint, 
        '/api/posts/<int:id>', '/api/posts/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
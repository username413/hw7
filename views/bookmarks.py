from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db, Post
import json
from views import get_authorized_user_ids

class BookmarksListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # get all bookmarks owned by the current user
        bookmarks = Bookmark.query.filter_by(user_id=self.current_user.id).all()
        return Response(json.dumps([bookmark.to_dict() for bookmark in bookmarks]), mimetype="application/json", status=200)

    def post(self):
        # create a new "bookmark" based on the data posted in the body 
        body = request.get_json()
        post_id = body.get("post_id")
        if post_id == None:
            return Response(json.dumps({ "msg": "post_id is required" }), mimetype="application/json", status=400)
        try:
            post_id = int(post_id)
        except Exception as e:
            return Response(json.dumps({ "msg": f"invalid input: {e}" }), mimetype="application/json", status=400)
        
        checks = Bookmark.query.filter_by(user_id=self.current_user.id, post_id=post_id).first()
        if checks != None:
            post = Post.query.get(checks.post_id)
            authorized_users = get_authorized_user_ids(current_user=self.current_user)
            if post != None and post.user_id not in authorized_users:
                return Response(json.dumps({ "msg": "unauthorized access" }), mimetype="application/json", status=404)
            return Response(json.dumps({ "msg": "already bookmarked" }), mimetype="application/json", status=400)

        post = Bookmark.query.get(post_id)
        if post == None:
            return Response(json.dumps({ "msg": "post not found" }), mimetype="application/json", status=404)
        
        bookmark = Bookmark(self.current_user.id, post_id)
        db.session.add(bookmark)
        db.session.commit()
        
        return Response(json.dumps(bookmark.to_dict()), mimetype="application/json", status=201)

class BookmarkDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # delete "bookmark" record where "id"=id
        try:
            delete_id = int(id)
        except Exception as e:
            return Response(json.dumps({ "msg": f"invalid input: {e}" }), mimetype="application/json", status=400)
        
        bookmark = Bookmark.query.get(delete_id)
        if bookmark == None:
            return Response(json.dumps({ "msg": "bookmark not found" }), mimetype="application/json", status=404)
        
        db.session.delete(bookmark)
        db.session.commit()
        return Response(json.dumps({ "msg": "bookmark deleted." }), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<int:id>', 
        '/api/bookmarks/<int:id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )

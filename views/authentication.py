from flask import request, \
    make_response, render_template, redirect
from models import User
import flask_jwt_extended

def logout():
    # # Uncomment these lines to delete the cookies and
    # # redirect the user to the login screen
    
    # response = make_response(redirect('/login', 302))
    # flask_jwt_extended.unset_jwt_cookies(response)
    # return response
    return 'TODO: Logout'

def login():
    if request.method == 'POST':
        print('See lecture 25 video + starter files')
        return 'See lecture 25 video + starter files'
    else:
        return render_template(
            'login.html'
        )

def initialize_routes(app):
    app.add_url_rule('/login', 
        view_func=login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', view_func=logout)
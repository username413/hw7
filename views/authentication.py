from flask import request, \
    make_response, render_template, redirect
from models import User
import flask_jwt_extended
import datetime

def logout():
    # Uncomment these lines to delete the cookies and
    # redirect the user to the login screen
    
    response = make_response(redirect('/login', 302))
    flask_jwt_extended.unset_jwt_cookies(response)
    return response

def login():
    if request.method == 'POST':
        un = request.form.get("username")
        pw = request.form.get("password")

        user = User.query.filter_by(username=un).one_or_none()
        if user == None:
            return render_template('login.html', message="wrong username" )
        if user and not user.check_password(pw):
            return render_template('login.html', message="wrong password")

        expiry = datetime.timedelta(minutes=20)
        access_token = flask_jwt_extended.create_access_token(
            identity=user.id, 
            expires_delta=expiry
        )
        response = make_response(redirect('/', 302))
        flask_jwt_extended.set_access_cookies(response, access_token)
        return response
    else:
        return render_template(
            'login.html'
        )

def initialize_routes(app):
    app.add_url_rule('/login', 
        view_func=login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', view_func=logout)
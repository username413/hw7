from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from flask import render_template
import os
from sqlalchemy import and_
from models import db, Post, User, Following, ApiNavigator, Story
from views import initialize_routes, get_authorized_user_ids
import flask_jwt_extended


app = Flask(__name__)
cors = CORS(app, 
    resources={r"/api/*": {"origins": '*'}}, 
    supports_credentials=True
)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    


db.init_app(app)
api = Api(app)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True 
jwt = flask_jwt_extended.JWTManager(app)

# # set logged in user
# with app.app_context():
#     app.current_user = User.query.filter_by(id=12).one()

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # print('JWT data:', jwt_data)
    user_id = jwt_data["sub"]
    return User.query.filter_by(id=user_id).one_or_none()

# Initialize routes for all of your API endpoints:
initialize_routes(api)

@flask_jwt_extended.jwt_required()
@app.route('/')
def home():
    return '''
       <p>View <a href="/api">REST API Tester</a>.</p>
       <p>Feel free to replace this code from HW2</p>
    '''


@app.route('/api')
@app.route("/api/")
def api_docs():
    navigator = ApiNavigator(app.current_user)
    return render_template(
        'api/api_docs.html', 
        user=app.current_user,
        endpoints=navigator.get_endpoints(),
        url_root=request.url_root[0:-1] # trim trailing slash
    )



# enables flask app to run using "python3 app.py"
if __name__ == '__main__':
    app.run()

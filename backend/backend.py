import warnings

import marshmallow as ma
from flask import Flask
from flask.views import MethodView
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_smorest import Api, Blueprint, abort
from flask_smorest.error_handler import ErrorSchema
from marshmallow import validate

warnings.filterwarnings("ignore", message="Multiple schemas resolved to the name ")


class UserSchema(ma.Schema):
    username = ma.fields.String(required=True, validate=validate.Length(max=20))
    email = ma.fields.Email(required=True, validate=validate.Length(max=50))

    uid = ma.fields.Integer(dump_only=True, attribute="userID", )
    role = ma.fields.String(dump_only=True)

    password = ma.fields.String(load_only=True, required=True, validate=validate.Length(min=7, max=50))


class PostSchema(ma.Schema):
    post_id = ma.fields.Integer(required=True, attribute="postID")
    forum_id = ma.fields.Integer(required=True, attribute="forumID")
    username = ma.fields.String(required=True, attribute="postName", validate=validate.Length(max=20))
    time = ma.fields.String(required=True, attribute="postTime", validate=validate.Length(max=23))
    text = ma.fields.String(required=True, attribute="postText", validate=validate.Length(max=200))


app = Flask(__name__)

app.config["API_TITLE"] = "ELEC0138 Forum API"
app.config["API_VERSION"] = "0.1.0"

# flask-smorest
app.config["OPENAPI_VERSION"] = "3.1.0"
app.config["OPENAPI_JSON_PATH"] = "api-spec.json"
app.config["OPENAPI_URL_PREFIX"] = "/api/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# flask-mysql
app.config["MYSQL_HOST"] = "47.122.18.213"
app.config["MYSQL_USER"] = "user"
app.config["MYSQL_PASSWORD"] = "3aRtVyBN17dUbCq9"
app.config["MYSQL_DB"] = "ELEC0138"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

CORS(app)
api = Api(app)
mysql = MySQL(app)

users_bp = Blueprint('user', __name__, url_prefix='/api/user')
posts_bp = Blueprint('post', __name__, url_prefix='/api/post')


@users_bp.route('register', endpoint='register')
class Users(MethodView):
    @users_bp.arguments(UserSchema, location='json')
    @users_bp.response(201, UserSchema)
    @users_bp.alt_response(409, schema=ErrorSchema)
    def post(self, args):
        """Create a new user"""
        email, password, name = args['email'], args['password'], args['username']

        with mysql.connection.cursor() as cursor:
            # Check if user's email already exists
            cursor.execute("SELECT 1 FROM Users WHERE email = %s", (email,))
            if cursor.fetchone():
                abort(409, message='Email already exists')

            # Check if user's username already exists
            cursor.execute("SELECT 1 FROM Users WHERE username = %s", (name,))
            if cursor.fetchone():
                abort(409, message='Username already exists')

            # Insert the new user
            cursor.execute(
                "INSERT INTO Users (email, password, username) VALUES (%s, %s, %s)",
                (email, password, name)
            )
            mysql.connection.commit()

            # Return the new user
            cursor.execute("SELECT * FROM Users WHERE username = %s", (name,))
            return cursor.fetchone()


@users_bp.route('/login', endpoint='login')
class UsersLogin(MethodView):
    @users_bp.arguments(UserSchema(only=("username", "password")), location='json')
    @users_bp.response(200, UserSchema)
    @users_bp.alt_response(404, schema=ErrorSchema)
    @users_bp.alt_response(401, schema=ErrorSchema)
    def post(self, args):
        """Login"""
        username, password = args['username'], args['password']

        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))

            if not (user := cursor.fetchone()):
                abort(404, message='User not found')

            if user['password'] != password:
                abort(401, message='Incorrect password')

        return user


@posts_bp.route('', endpoint='index')
class Posts(MethodView):
    @posts_bp.response(200, PostSchema(many=True))
    def get(self):
        """Get all posts"""
        with mysql.connection.cursor() as cursor:
            cursor.execute(
                "SELECT P.postID, P.forumID, P.postName, P.postTime, P.postText, U.email "
                "FROM Posts P "
                "INNER JOIN Users U ON P.postName = U.username"
            )
            return list(cursor.fetchall())

    @posts_bp.arguments(PostSchema(only=("forum_id", "username", "time", "text")), location='json')
    @posts_bp.response(201)
    def post(self, args):
        """Create a new post"""
        fid, name, time, text = args['forumID'], args['postName'], args['postTime'], args['postText']

        with mysql.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Posts (forumID, postName, postTime, postText) VALUES (%s, %s, %s, %s)",
                (fid, name, time, text)
            )
            mysql.connection.commit()

    @posts_bp.arguments(PostSchema(only=("forum_id", "post_id", "username", "text")), location='json')
    @posts_bp.response(204)
    def put(self, args):
        """Update a post"""
        fid, pid, name, text = args['forumID'], args['postID'], args['postName'], args['postText']

        with mysql.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE Posts SET postText = %s WHERE forumID = %s AND postID = %s AND postName = %s",
                (text, fid, pid, name)
            )
            mysql.connection.commit()

    @posts_bp.arguments(PostSchema(only=("forum_id", "post_id", "username")), location='json')
    @posts_bp.response(204)
    def delete(self, args):
        """Delete a post"""
        fid, pid, name = args['forumID'], args['postID'], args['postName']

        with mysql.connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM Posts WHERE forumID = %s AND postID = %s AND postName = %s",
                (fid, pid, name)
            )
            mysql.connection.commit()


api.register_blueprint(users_bp)
api.register_blueprint(posts_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=False)
    # app.run(host="127.0.0.1", port=80, debug=True)

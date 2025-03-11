"""
This file is the backend of the project. It is responsible for handling
the requests from the frontend and interacting with the database. It is
written in Python and uses Flask as the web framework.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL

# from waitress import serve

app = Flask(__name__)

# Enable CORs for all routes
CORS(app)


app.config["MYSQL_HOST"] = "47.122.18.213"
app.config["MYSQL_USER"] = "user"
app.config["MYSQL_PASSWORD"] = "3aRtVyBN17dUbCq9"
app.config["MYSQL_DB"] = "ELEC0138"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


class InvalidAPIUsage(Exception):
    """Custom exception for API errors"""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Convert exception to dictionary"""
        response_dict = dict(self.payload or ())
        response_dict["code"] = self.status_code
        response_dict["messages"] = self.message
        return response_dict


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(exception):
    """Error handler for InvalidAPIUsage"""
    return jsonify(exception.to_dict()), exception.status_code


def get_request_data():
    """Retrieve JSON data from the request."""
    try:
        data = request.get_json()
    except Exception as exc:
        raise InvalidAPIUsage("Invalid JSON format.", status_code=400) from exc
    if data is None:
        raise InvalidAPIUsage("JSON body is missing.", status_code=400)
    return data


def validate_field(data, key, friendly_name=None, max_length=None):
    """
    Validate that a field exists and does not exceed an optional maximum length.

    Parameters:
        data (dict): The JSON payload.
        key (str): The key to validate.
        friendly_name (str, optional): A user-friendly name for error messages.
        max_length (int, optional): The maximum allowed length.

    Returns:
        The value of the field if valid.

    Raises:
        InvalidAPIUsage: If the field is missing or too long.
    """
    friendly_name = friendly_name or key
    value = data.get(key)
    if not value:
        raise InvalidAPIUsage(f"{friendly_name} is required.", status_code=400)
    if max_length is not None and len(value) > max_length:
        raise InvalidAPIUsage(f"{friendly_name} is too long.", status_code=400)
    return value


@app.route("/user/login", methods=["POST"])
def user_login():
    """
    user login

    method: POST
    body: {"username": string, "password": string}
    return: JSON
    {
        code: int,
        messages: string or list of dictionary
    }

    messages:
        code 200: [{"userID": int, "username": string, "role": string}]
        code 400: Invalid JSON format, Username is required, Password is required
        code 403: Password is incorrect
        code 404: No such user
    """
    # Retrieve and validate JSON data from the request
    data = get_request_data()

    # Validate required fields and enforce maximum lengths where needed
    username = validate_field(data, "username", "username", max_length=20)
    password = validate_field(data, "password", "password", max_length=50)

    # Creating a connection cursor
    cursor = mysql.connection.cursor()

    # safe implementation to prevent SQL injection
    # cursor.execute(
    #     "SELECT userID, username, role FROM Users WHERE username=%s AND password=%s",
    #     (username, password),
    # )
    # print("********")
    # print(
    #     f"SELECT userID, username, role FROM Users WHERE username=%s AND password=%s",
    #     (username, password),
    # )
    # print("********")

    # not safe implementation
    query = (
        "SELECT * FROM Users WHERE username='"
        + username
        + "' AND password='"
        + password
        + "';"
    )

    # Request body in JSON format:
    # {
    #     "username": "anything' OR '1'='1",
    #     "password": "anything' OR '1'='1"
    # }

    # SELECT * FROM Users WHERE username='anything' OR '1'='1'
    # AND password='anything' OR '1'='1';

    cursor.execute(query)
    messages = cursor.fetchall()
    if len(messages) == 0:
        cursor.execute(
            "SELECT userID, username, role FROM Users WHERE username=%s", (username,)
        )
        messages = cursor.fetchall()
        if len(messages) == 0:
            raise InvalidAPIUsage("No such user.", status_code=404)
        if len(messages) >= 1:
            raise InvalidAPIUsage("Password is incorrect.", status_code=403)
    cursor.close()
    return jsonify(code=200, messages=messages)


@app.route("/user/register", methods=["POST"])
def user_register():
    """
    user register

    method: POST
    """

    # Retrieve and validate JSON data from the request
    data = get_request_data()

    # Validate required fields and enforce maximum lengths where needed
    username = validate_field(data, "username", "username", max_length=20)
    password = validate_field(data, "password", "password", max_length=50)
    email = validate_field(data, "email", "email", max_length=50)

    cursor = mysql.connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO Users (username, password, email) VALUES (%s, %s, %s)",
            (username, password, email),
        )
    except mysql.connection.Error as mysql_error:
        print(f"MySQL Error [{mysql_error.args[0]}]: {mysql_error.args[1]}")
        raise InvalidAPIUsage(
            f"MySQL Error [{mysql_error.args[0]}]: {mysql_error.args[1]}",
            status_code=500,
        ) from mysql_error
    finally:
        mysql.connection.commit()
        cursor.close()

    return jsonify(code=201, messages="User registered successfully."), 201


@app.route("/post/send", methods=["POST"])
def insert_post():
    """
    insert post

    method: POST
    body:
    {
        "forumID": int,
        "postID": int, (auto increment), unnecessary
        "postName": string,
        "postTime": string,
        "postText": string
    }
    return: JSON
    {
        code: int,
        messages: string or list of dictionary
    }

    messages:
        code 201: Post inserted successfully
        code 400: Invalid JSON format, ForumID is required,
                  Username is required, PostTime is required,
                  PostText is required
                  username is too long, postTime is too long,
                  postText is too long
        code 500: MySQL Error [error code]: error message
    """
    # Retrieve and validate JSON data from the request
    data = get_request_data()

    # Validate required fields and enforce maximum lengths where needed
    # post_id = validate_field(data, "postID", "PostID")
    forum_id = validate_field(data, "forumID", "ForumID")
    username = validate_field(data, "postName", "PostName", max_length=20)
    post_time = validate_field(data, "postTime", "PostTime", max_length=23)
    post_text = validate_field(data, "postText", "PostText", max_length=200)

    cursor = mysql.connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO Posts (forumID, postName, postTime, postText) "
            "VALUES (%s, %s, %s, %s)",
            (forum_id, username, post_time, post_text),
        )
    except mysql.connection.Error as mysql_error:
        print(f"MySQL Error [{mysql_error.args[0]}]: {mysql_error.args[1]}")
        raise InvalidAPIUsage(
            f"MySQL Error [{mysql_error.args[0]}]: {mysql_error.args[1]}",
            status_code=500,
        ) from mysql_error
    finally:
        mysql.connection.commit()
        cursor.close()

    return jsonify(code=201, messages="Post inserted successfully."), 201


@app.route("/post/get", methods=["GET"])
def get_post():
    """
    get post

    method: GET
    return: JSON
    {
        code: int,
        messages: list of dictionary
    }
    """

    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT postID, forumID, postName, postTime, postText, email "
        "FROM Posts, Users WHERE postName=username"
    )
    messages = cursor.fetchall()
    cursor.close()
    return jsonify(code=200, messages=messages)


@app.route("/post/update", methods=["POST"])
def edit_post():
    """
    edit post

    method: POST
    body:
    {
        "postID": int,
        "forumID": int,
        "postName": string,
        "postTime": string,
        "postText": string
    }
    return: JSON
    {
        code: int,
        messages: string
    }

    messages:
        code 200: Post updated successfully
        code 400: Invalid JSON format, PostID is required, ForumID is required,
                  Postname is required, PostTime is required,
                  PostText is required, Postname is too long,
                  PostTime is too long, PostText is too long
        code 404: No such post
        code 500: MySQL Error [error code]: error message
    """
    # Retrieve and validate JSON data from the request
    data = get_request_data()

    # Validate required fields and enforce maximum lengths where needed
    post_id = validate_field(data, "postID", "PostID")
    forum_id = validate_field(data, "forumID", "ForumID")
    post_name = validate_field(data, "postName", "PostName", max_length=20)
    post_time = validate_field(data, "postTime", "PostTime", max_length=23)
    post_text = validate_field(data, "postText", "PostText", max_length=200)

    cursor = mysql.connection.cursor()
    try:
        cursor.execute(
            "UPDATE Posts SET postTime=%s, postText=%s "
            "WHERE postName=%s AND postID=%s AND forumID=%s",
            (post_time, post_text, post_name, post_id, forum_id),
        )
        if cursor.rowcount == 0:
            raise InvalidAPIUsage("No Changes.", status_code=404)
    except mysql.connection.Error as mysql_error:
        print(f"MySQL Error [{mysql_error.args[0]}]: {mysql_error.args[1]}")
        raise InvalidAPIUsage(
            f"MySQL Error [{mysql_error.args[0]}]: {mysql_error.args[1]}",
            status_code=500,
        ) from mysql_error
    finally:
        mysql.connection.commit()
        cursor.close()

    return jsonify(code=201, messages="Post updated successfully."), 201


@app.route("/post/delete", methods=["POST"])
def delete_post():
    """
    delete post

    method: POST
    body: {"postID": int, "forumID": int, "postName": string}
    return: JSON
    {
        code: int,
        messages: string
    }

    messages:
        code 226: Post deleted successfully
        code 400: Invalid JSON format, PostID is required, ForumID is required, PostName is required
        code 404: No such post
        code 500: MySQL Error [error code]: error message
    """
    # Retrieve and validate JSON data from the request
    data = get_request_data()

    # Validate required fields and enforce maximum lengths where needed
    post_id = validate_field(data, "postID", "PostID")
    forum_id = validate_field(data, "forumID", "ForumID")
    post_name = validate_field(data, "postName", "PostName", max_length=20)

    cursor = mysql.connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM Posts WHERE postID=%s AND forumID=%s AND postName=%s",
            (post_id, forum_id, post_name),
        )
        if cursor.rowcount == 0:
            raise InvalidAPIUsage("No such post.", status_code=404)
    except mysql.connection.Error as mysql_error:
        print(f"MySQL Error [{mysql_error.args[0]}]: {mysql_error.args[1]}")
        raise InvalidAPIUsage(
            f"MySQL Error [{mysql_error.args[0]}]: {mysql_error.args[1]}",
            status_code=500,
        ) from mysql_error
    finally:
        mysql.connection.commit()
        cursor.close()

    return jsonify(code=226, messages="Post deleted successfully."), 226


# if __name__ == "__main__":
#     serve(app, host="0.0.0.0", port=80)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config["MYSQL_HOST"] = "47.122.18.213"
app.config["MYSQL_USER"] = "user"
app.config["MYSQL_PASSWORD"] = "3aRtVyBN17dUbCq9"
app.config["MYSQL_DB"] = "ELEC0138"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["code"] = self.status_code
        rv["messages"] = self.message
        return rv


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code


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
    try:
        data = request.get_json()
    except:
        raise InvalidAPIUsage("Invalid JSON format.", status_code=400)
    username = data.get("username")
    password = data.get("password")
    if not username:
        raise InvalidAPIUsage("Username is required.", status_code=400)
    if not password:
        raise InvalidAPIUsage("Password is required.", status_code=400)

    # Creating a connection cursor
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT userID, username, role FROM Users WHERE username=%s AND password=%s",
        (username, password),
    )
    rv = cursor.fetchall()
    if len(rv) == 0:
        cursor.execute(
            "SELECT userID, username, role FROM Users WHERE username=%s", (username,)
        )
        rv = cursor.fetchall()
        if len(rv) == 0:
            raise InvalidAPIUsage("No such user.", status_code=404)
        else:
            raise InvalidAPIUsage("Password is incorrect.", status_code=403)
    cursor.close()
    return jsonify(code=200, messages=rv)


@app.route("/post/send", methods=["POST"])
def insert_post():
    """
    insert post

    method: POST
    body: {"forumID": int, "postID": int, "postName": string, "postTime": string, "postText": string}
    return: JSON
    {
        code: int,
        messages: string or list of dictionary
    }

    messages:
        code 201: Post inserted successfully
        code 400: Invalid JSON format, ForumID is required, Username is required, PostTime is required, PostText is required
                  username is too long, postTime is too long, postText is too long
        code 500: MySQL Error [error code]: error message
    """

    try:
        data = request.get_json()
    except:
        raise InvalidAPIUsage("Invalid JSON format.", status_code=400)

    forumID = data.get("forumID")
    postID = data.get("postID")
    username = data.get("postName")
    postTime = data.get("postTime")
    postText = data.get("postText")

    if not forumID:
        raise InvalidAPIUsage("ForumID is required.", status_code=400)
    if not username:
        raise InvalidAPIUsage("Username is required.", status_code=400)
    elif len(username) > 20:
        raise InvalidAPIUsage("Username is too long.", status_code=400)
    if not postTime:
        raise InvalidAPIUsage("PostTime is required.", status_code=400)
    elif len(postTime) > 23:
        raise InvalidAPIUsage("PostTime is too long.", status_code=400)
    if not postText:
        raise InvalidAPIUsage("PostText is required.", status_code=400)
    elif len(postText) > 200:
        raise InvalidAPIUsage("PostText is too long.", status_code=400)

    cursor = mysql.connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO Posts (forumID, postName, postTime, postText) VALUES (%s, %s, %s, %s)",
            (forumID, username, postTime, postText),
        )
    except mysql.connection.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        raise InvalidAPIUsage(
            f"MySQL Error [{e.args[0]}]: {e.args[1]}", status_code=500
        )
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
    cursor.execute("SELECT * FROM Posts")
    rv = cursor.fetchall()
    cursor.close()
    return jsonify(code=200, messages=rv)


@app.route("/post/update", methods=["POST"])
def edit_post():
    """
    edit post

    method: POST
    body: {"postID": int, "forumID": int, "postName": string, "postTime": string, "postText": string}
    return: JSON
    {
        code: int,
        messages: string
    }

    messages:
        code 200: Post updated successfully
        code 400: Invalid JSON format, PostID is required, ForumID is required, Postname is required
                  PostTime is required, PostText is required, Postname is too long, PostTime is too long, PostText is too long
        code 404: No such post
        code 500: MySQL Error [error code]: error message
    """
    try:
        data = request.get_json()
    except:
        raise InvalidAPIUsage("Invalid JSON format.", status_code=400)
    postID = data.get("postID")
    forumID = data.get("forumID")
    postName = data.get("postName")
    postTime = data.get("postTime")
    postText = data.get("postText")
    if not postID:
        raise InvalidAPIUsage("PostID is required.", status_code=400)
    if not forumID:
        raise InvalidAPIUsage("ForumID is required.", status_code=400)
    if not postName:
        raise InvalidAPIUsage("Postname is required.", status_code=400)
    elif len(postName) > 20:
        raise InvalidAPIUsage("Postname is too long.", status_code=400)
    if not postTime:
        raise InvalidAPIUsage("PostTime is required.", status_code=400)
    elif len(postTime) > 23:
        raise InvalidAPIUsage("PostTime is too long.", status_code=400)
    if not postText:
        raise InvalidAPIUsage("PostText is required.", status_code=400)
    elif len(postText) > 200:
        raise InvalidAPIUsage("PostText is too long.", status_code=400)

    cursor = mysql.connection.cursor()
    try:
        cursor.execute(
            "UPDATE Posts SET postName=%s, postTime=%s, postText=%s WHERE postID=%s AND forumID=%s",
            (postName, postTime, postText, postID, forumID),
        )
        if cursor.rowcount == 0:
            raise InvalidAPIUsage("No Changes.", status_code=404)
    except mysql.connection.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        raise InvalidAPIUsage(
            f"MySQL Error [{e.args[0]}]: {e.args[1]}", status_code=500
        )
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
    try:
        data = request.get_json()
    except:
        raise InvalidAPIUsage("Invalid JSON format.", status_code=400)
    postID = data.get("postID")
    forumID = data.get("forumID")
    postName = data.get("postName")
    if not postID:
        raise InvalidAPIUsage("PostID is required.", status_code=400)
    if not forumID:
        raise InvalidAPIUsage("ForumID is required.", status_code=400)
    if not postName:
        raise InvalidAPIUsage("PostName is required.", status_code=400)

    cursor = mysql.connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM Posts WHERE postID=%s AND forumID=%s AND postName=%s",
            (postID, forumID, postName),
        )
        if cursor.rowcount == 0:
            raise InvalidAPIUsage("No such post.", status_code=404)
    except mysql.connection.Error as e:
        print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        raise InvalidAPIUsage(
            f"MySQL Error [{e.args[0]}]: {e.args[1]}", status_code=500
        )
    finally:
        mysql.connection.commit()
        cursor.close()

    return jsonify(code=226, messages="Post deleted successfully."), 226


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
    # app.run(host="127.0.0.1", port=80, debug=True)

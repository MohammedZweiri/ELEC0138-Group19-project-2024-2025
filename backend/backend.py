from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return jsonify(message="Welcome to the forum")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
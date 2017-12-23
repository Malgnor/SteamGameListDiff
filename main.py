from flask import Flask, render_template
from steam_api import get_steamid, get_owned_games, get_player_summaries
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
        profile1, profile2 = get_player_summaries(userid1, userid2)
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

    list1 = {v['appid']: v for v in games1}
    list2 = {v['appid']: v for v in games2}

    list3 = {}
    list4 = {}
    list5 = {}

    for appid, game in list1.items():
        if appid in list2:
            list3.update({appid: game})
        else:
            list4.update({appid: game})

    for appid, game in list2.items():
        if appid not in list3:
            list5.update({appid: game})

    return render_template('compare.html', games_user1=list4.values(), games_user2=list5.values(), games_both=list3.values(), user1=profile1, user2=profile2)

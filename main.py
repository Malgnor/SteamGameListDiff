from flask import Flask, render_template
from steam_api import get_steamid, get_owned_games, get_player_summaries
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


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

    games_both = games1 & games2
    games_only_u1 = games1 - games_both
    games_only_u2 = games2 - games_both

    return render_template('compare.html', games_user1=games_only_u1, games_user2=games_only_u2, games_both=games_both, user1=profile1, user2=profile2)

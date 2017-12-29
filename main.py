from flask import Flask, render_template, jsonify
from steam_api import get_steamid, get_owned_games, get_player_summaries, get_player_summary
app = Flask(__name__)


def get_steamids(*args):
    steamids = []
    for user in args:
        try:
            userid = int(user)
        except ValueError:
            try:
                userid = get_steamid(user)
            except ValueError as exception:
                raise ValueError(str(exception))
        steamids.append(userid)
    return steamids

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compare/<user1>/<user2>/')
def compare_users(user1, user2):
    errors = []
    try:
        steamids = get_steamids(user1, user2)
    except ValueError as exception:
        errors.append(str(exception))

    if len(errors) is not 0:
        return '<br>'.join(errors)

    try:
        profiles = get_player_summaries(steamids)
    except ValueError as exception:
        errors.append(str(exception))

    if len(errors) is not 0:
        return '<br>'.join(errors)

    if profiles[0]['steamid'] != steamids[0]:
        profiles.reverse()

    try:
        games1 = get_owned_games(profiles[0]['steamid'])
    except ValueError as exception:
        errors.append(str(exception))

    try:
        games2 = get_owned_games(profiles[1]['steamid'])
    except ValueError as exception:
        errors.append(str(exception))

    if len(errors) is not 0:
        return '<br>'.join(errors)

    games_both = games1 & games2
    games_only_u1 = games1 - games_both
    games_only_u2 = games2 - games_both

    return render_template('compare.html', games_user1=games_only_u1, games_user2=games_only_u2, games_both=games_both, user1=profiles[0], user2=profiles[1])


@app.route('/checkUser/<user>/')
def check_user(user):
    try:
        userid = int(user)
    except ValueError:
        try:
            userid = get_steamid(user)
        except ValueError:
            return jsonify(error='Custom url not found.')

    try:
        profile = get_player_summary(userid)
    except ValueError:
        return jsonify(error='Profile not found.')

    return jsonify(avatarfull=profile['avatarfull'], personaname=profile['personaname'])

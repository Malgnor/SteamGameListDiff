from itertools import combinations
from flask import Flask, render_template, jsonify
from steam_api import get_steamid, get_owned_games, get_player_summaries, get_player_summary
app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


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
        steamids.append(str(userid))
    return steamids


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compare/<user1>/<user2>/')
def compare_users(user1, user2):
    try:
        steamids = get_steamids(user1, user2)
    except ValueError as exception:
        return str(exception)

    try:
        profiles = get_player_summaries(steamids)
    except ValueError as exception:
        return str(exception)

    if profiles[0]['steamid'] != steamids[0]:
        profiles.reverse()

    try:
        games1 = get_owned_games(profiles[0]['steamid'])
    except ValueError as exception:
        return str(exception)

    try:
        games2 = get_owned_games(profiles[1]['steamid'])
    except ValueError as exception:
        return str(exception)

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


@app.route('/compareMulti/<users>/')
def compare_multi(users):
    try:
        steamids = get_steamids(*users.split(','))
    except ValueError as exception:
        return str(exception)

    try:
        _profiles = get_player_summaries(steamids)
    except ValueError as exception:
        return str(exception)

    profiles = []

    for steamid in steamids:
        for profile in _profiles:
            if profile['steamid'] == steamid:
                profiles.append(profile)
                _profiles.remove(profile)
                break

    games = []

    for profile in profiles:
        try:
            games.append(get_owned_games(profile['steamid']))
        except ValueError as exception:
            return str(exception)

    _index = range(len(profiles))
    groups = [combination for size in range(
        1, len(_index)) for combination in combinations(_index, size)]
    groups.append(_index)

    sets = [set() for _ in range(len(groups))]

    for set_index, group in enumerate(groups[::-1]):
        for profile in group:
            if len(sets[set_index]) == 0:
                sets[set_index].update(games[profile])
            else:
                sets[set_index].intersection_update(games[profile])
        for pindex in range(set_index):
            sets[set_index].difference_update(sets[pindex])

    sets.reverse()

    return render_template('compareMulti.html', profiles=profiles, groups=groups, games=sets)

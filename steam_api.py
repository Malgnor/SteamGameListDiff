import os
import requests

STEAM_WEB_API_KEY = os.getenv('STEAM_WEB_API_KEY', 'NO KEY :(')


def get_steamid(vanity_name):
    req = requests.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/',
                       {'key': STEAM_WEB_API_KEY, 'vanityurl': vanity_name})
    if req.status_code == 200:
        res = req.json()['response']
        if res['success'] == 1:
            return res['steamid']
        raise ValueError('Vanity name {} not found.'.format(vanity_name))
    raise ValueError('ResolveVanityURL status response: ' + res.status_code)


def get_owned_games(userid):
    req = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/',
                       {'key': STEAM_WEB_API_KEY, 'steamid': userid, 'include_appinfo': 1})
    if req.status_code == 200:
        res = req.json()['response']
        return res['games']
    raise ValueError('GetOwnedGames status response: ' + res.status_code)

def get_player_summaries(user1, user2):
    req = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
                       {'key': STEAM_WEB_API_KEY, 'steamids': '{},{}'.format(user1, user2)})
    if req.status_code == 200:
        res = req.json()['response']
        return (res['players'][0], res['players'][1]) if res['players'][0]['steamid'] == user1 else (res['players'][1], res['players'][0])
    raise ValueError('GetOwnedGames status response: ' + res.status_code)


# http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=XXXXXXXXXXXXXXXXXXXXXXX&vanityurl=userVanityUrlName
# http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=XXXXXXXXXXXXXXXXX&steamid=XXXXXXXXXXXXX&include_appinfo=true&format=json
# http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=XXXXXXXXXXXXXXXXXXXXXXX&steamids=XXXXXXX
# http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg

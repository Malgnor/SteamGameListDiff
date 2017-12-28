import os
import requests

STEAM_WEB_API_KEY = os.getenv('STEAM_WEB_API_KEY', 'NO KEY :(')


class SteamGame(object):
    def __init__(self, **kwargs):
        self.appid = kwargs.pop('appid')
        self.name = kwargs.pop('name')
        self.playtime_forever = kwargs.pop('playtime_forever')
        self.playtime_2weeks = kwargs.pop('playtime_2weeks', 0)
        self.img_icon_url = kwargs.pop('img_icon_url')
        self.img_logo_url = kwargs.pop('img_logo_url')
        self.has_community_visible_stats = kwargs.pop(
            'has_community_visible_stats', False)

        self.img_icon_full_url = 'http://media.steampowered.com/steamcommunity/public/images/apps/{}/{}.jpg'.format(
            self.appid, self.img_icon_url) if self.img_icon_url is not '' else '/static/questionmark.png'
        self.img_logo_full_url = 'http://media.steampowered.com/steamcommunity/public/images/apps/{}/{}.jpg'.format(
            self.appid, self.img_logo_url) if self.img_logo_url is not '' else '/static/questionmark.png'

    def __hash__(self):
        return self.appid

    def __eq__(self, other):
        return self.appid == other.appid


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
        return set(SteamGame(**game) for game in res['games'])
    raise ValueError('GetOwnedGames status response: ' + res.status_code)


def get_player_summaries(user1, user2):
    req = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
                       {'key': STEAM_WEB_API_KEY, 'steamids': '{},{}'.format(user1, user2)})
    if req.status_code == 200:
        res = req.json()['response']
        if len(res['players']) is 1:
            raise ValueError('A profile(id={}) wasn\'t found.'.format(user1 if res['players'][0]['steamid'] == str(user1) else user2))
        elif len(res['players']) is 0:
            raise ValueError('No profiles found.')
        return (res['players'][0], res['players'][1]) if res['players'][0]['steamid'] == str(user1) else (res['players'][1], res['players'][0])
    raise ValueError('GetPlayerSummaries status response: ' + res.status_code)


# http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=XXXXXXXXXXXXXXXXXXXXXXX&vanityurl=userVanityUrlName
# http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=XXXXXXXXXXXXXXXXX&steamid=XXXXXXXXXXXXX&include_appinfo=1&format=json
# http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=XXXXXXXXXXXXXXXXXXXXXXX&steamids=XXXXXXX
# http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg

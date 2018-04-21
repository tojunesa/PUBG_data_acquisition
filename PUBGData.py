import requests
import time
import matplotlib.pyplot as plt


# API authorization key
with open('PUBGAPIkey.txt', 'r') as keyfile:
    APIkey = keyfile.read()

    
def Players_Last_Match(player_name):
    """
    Retrieve the last match's id of the player

    """

    personal_url = "https://api.playbattlegrounds.com/shards/pc-na/players?filter[playerNames]="+player_name
    player_header = {"Authorization": "Bearer "+APIkey,
                "Accept": "application/vnd.api+json"
                }
    # Request data
    request_player = requests.get(personal_url, headers = player_header)
    data_player = request_player.json()
    
    if "errors" in data_player:
        print(data_player['errors']['title'])
        return 0

    # Get match id
    matches = data_player['data'][0]['relationships']['matches']['data']
    match_id = matches[0]['id'] # 0 indicates the last match
    return match_id

def Players_Trace(match_id, player_name):
    """
    Plot the trace of the player

    """
    match_url = "https://api.playbattlegrounds.com/shards/some-region/matches/"+match_id
    match_header = {"Authorization": "Bearer "+APIkey,
                "Accept": "application/vnd.api+json"
                }

    request_match = requests.get(match_url, headers = match_header)
    data_match = request_match.json()

    for item in data_match['included']:
        if item['type'] == 'asset':
            telemetry_url = item['attributes']['URL']

    telemetry_header = {"Accept": "application/vnd.api+json"}

    request_telemetry = requests.get(telemetry_url, headers = telemetry_header)
    data_telemetry = request_telemetry.json()

    ric_position = {'x':[], 'y':[], 'z':[]}

    for event in data_telemetry:
        if "character" in event:
            if event['character']['name'] == player_name:
                player_position['x'].append(event['character']['location']['x'])
                player_position['y'].append(event['character']['location']['y'])
                player_position['z'].append(event['character']['location']['z'])
            
    return player_position



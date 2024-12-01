# import sys
import os
import requests
# import argparse
# import concurrent.futures
# import random
import pickle
import time
from datetime import datetime
# import re

SLEEP = 0.05

def get_response(url, params, auth, client_id, tries=3):
    headers = {
    'Authorization': auth,
    'Client-Id': client_id,
    }
    for _ in range(tries):
        try:
            response = requests.get(url, headers=headers, params=params)
            return(response)
        except Exception as e:
            print(e)
            time.sleep(SLEEP)

def get_top_games(auth, client_id, top_games={}):
    url = 'https://api.twitch.tv/helix/games/top'
    params = {
        'first': 100
    }
    try:
        response = get_response(url, params, auth, client_id)
        for game in response.json()['data']:
            top_games[game['name'].lower()] = {'id' : game['id'], 'box_art_url' : game['box_art_url'], 'name' : game['name'], 'igdb_id': game['igdb_id']}
    except Exception as e:
        print(e)
        print("Couldn't get first page of top games! Maybe the API key is broken or the API is broken")
        return top_games
    try:
        pag = response.json()['pagination']['cursor']
        params['after'] = pag
        while pag:
            response = get_response(url, params, auth, client_id)
            for game in response.json()['data']:
                top_games[game['name'].lower()] = {'id' : game['id'], 'box_art_url' : game['box_art_url'], 'name' : game['name'], 'igdb_id': game['igdb_id']}
                pag = response.json()['pagination']['cursor']
                params['after'] = pag
    except Exception as e:
        print(e)
        return top_games

def main():
    auth = 'Bearer 6v91ackg29ptj0c8nmx5igrp9x4whq'
    client_id = 'gp762nuuoqcoxypju8c569th9wz7q5'
    if os.path.exists("top_games.pickle"):
        with open("top_games.pickle", "rb") as f:
            top_games = pickle.load(f)
    else:
        top_games = {}
        with open("top_games.pickle", "wb") as f:
            pickle.dump(top_games, f)
    top_games = get_top_games(auth, client_id, top_games)
    print("Number of games in top_games.pickle is", len(top_games))
    with open("top_games.pickle", "wb") as f:
            pickle.dump(top_games, f)

if __name__ == "__main__":
    main()
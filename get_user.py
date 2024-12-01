import os
import requests
import pickle
import sys
import concurrent.futures
import time

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

def get_user_by_name(auth, client_id, user_name, users):
    url = 'https://api.twitch.tv/helix/users'
    params = {
        'login': user_name,
    }
    try:
        response = get_response(url, params, auth, client_id)
        data = response.json()['data'][0]
        users[user_name] = {'id': data['id'], 'display_name': data['display_name'], 'login': data['login'], 'profile_image_url': data['profile_image_url'], 'offline_image_url': data['offline_image_url'], 'created_at': data['created_at']}
        return users
    except Exception as e:
        print(e)
        return users

def print_user(user):
    with open("users.pickle", "rb") as f:
        users = pickle.load(f)
    print(users[user])

def print_all_users(users):
    for user in users:
        print(users[user])

def get_users(user_list):
    auth = 'Bearer 6v91ackg29ptj0c8nmx5igrp9x4whq'
    client_id = 'gp762nuuoqcoxypju8c569th9wz7q5'
    if os.path.exists("users.pickle"):
        with open("users.pickle", "rb") as f:
            users = pickle.load(f)
    else:
        users = {}

    for user in user_list:
        users = get_user_by_name(auth, client_id, user, users)

    with open("users.pickle", "wb") as f:
        pickle.dump(users, f)

if __name__ == "__main__":
    user_list = []
    for user in sys.argv[1:]:
        user_list.append(user.lower())
    get_users(user_list)

import sys
import os
import requests
import argparse
import concurrent.futures
import secrets
import random
import time
from datetime import datetime
import re
import pickle
import csv
import io
from PIL import Image

import manage_folders
import manage_db
import get_top_games
import get_user

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36']

SLEEP = 0.02

def full_page_screenshot(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    parts = []
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(secrets.uniform(2.1, 2.9)) # Wait to load page
        part = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
        parts.append(part)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    full_img = Image.new('RGB', (parts[0].width, sum(p.height for p in parts)))
    offset = 0
    for part in parts:
        full_img.paste(part, (0, offset))
        offset += part.height
    return full_img

def get_response(url, params, tries=696969):
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

def get_user_id(user_name):
    url = 'https://api.twitch.tv/helix/users'
    params = {
        'login': user_name,
    }
    try:
        response = get_response(url, params)
        return(response.json()['data'][0]['id'])
    except Exception as e:
        print(e)
        return(None)

def get_top_streams(conn, game_id=None, pages=100):
    top_streamers = set()
    url = 'https://api.twitch.tv/helix/streams'
    params = {
        'first': 100,
    }
    if game_id:
        params['game_id'] = int(game_id)
    try:
        response = get_response(url, params)
    except Exception as e:
        print(e)
        print("Cannot get top streams!")
        return(top_streamers)
    for i in response.json()['data']:
        try:
            user_name = i['user_name'].lower()
            table_name = manage_db.get_table_name(user_name)
            if manage_db.check_table_exists(conn, table_name):
                try:
                    max_viewer_count = max(i['viewer_count'], manage_db.get_max_viewer_count(conn, user_name))
                except Exception as e:
                    print(e)
                    max_viewer_count = i['viewer_count']
                new_values = {'user_name': user_name, 'latest_viewer_count': i['viewer_count'], 'max_viewer_count': max_viewer_count}
                manage_db.update_user(conn, i['user_id'], new_values)
                top_streamers.add(user_name)
            else:
                manage_db.insert_user(conn, i['user_id'], user_name, i['viewer_count'], i['viewer_count'])
                manage_db.create_user_table(conn, table_name)
                top_streamers.add(user_name)
        except Exception as e:
            print(e)
            print(f"Error in get_top_streams() for {i['user_name']}")
    
    for i in range(pages):
        try:
            pag = response.json()['pagination']['cursor']
        except Exception as e:
            print(e)
            return(top_streamers)
        params = {
            'first': 100,
            'after': pag,
        }
        response = get_response(url, params)
        for i in response.json()['data']:
            try:
                user_name = i['user_name'].lower()
                table_name = manage_db.get_table_name(user_name)
                if manage_db.check_table_exists(conn, table_name):
  
                    try:
                        max_viewer_count = max(i['viewer_count'], manage_db.get_max_viewer_count(conn, user_name))
                    except Exception as e:
                        print(e)
                        max_viewer_count = i['viewer_count']
                    new_values = {'user_name': user_name, 'latest_viewer_count': i['viewer_count'], 'max_viewer_count': max_viewer_count}
                    manage_db.update_user(conn, i['user_id'], new_values)
                    top_streamers.add(user_name)
                else:
                    manage_db.insert_user(conn, i['user_id'], user_name, i['viewer_count'], i['viewer_count'])
                    manage_db.create_user_table(conn, table_name)
                    top_streamers.add(user_name)
            except Exception as e:
                print(e)
                print(f"Error in get_top_streams() for {i['user_name']}")
    return(top_streamers)

def get_streamer_videos(user_name):
    conn = manage_db.create_connection()
    # multitthread random sleep to make the API requests not execute at exactly the same time
    time.sleep(random.uniform(0.05, 0.2))
    try:
        user_id = get_user_id(user_name)
    except Exception as e:
        print(e)
        print(f"Cannot find user_id for {user_name}!")
        return
    url = 'https://api.twitch.tv/helix/videos'
    params = {
        'first' : 100,
        'user_id': user_id,
    }
    try:
        response = get_response(url, params)
        data = response.json()
        if manage_db.is_streamer_in_users(conn, user_name) == False:
            try:
                max_viewer_count = manage_db.get_max_viewer_count(conn, user_name)
                manage_db.insert_user(conn, user_id, user_name, 0, max_viewer_count)
            except Exception as e:
                print(e)
                print("Couldn't insert {user_name} into users table from get_streamer_videos() function!")
    except Exception as e:
        print(e)
        print(f"Cannot get response for get_streamer_videos({user_name})!")
        return
    table_name = manage_db.get_table_name(user_name)
    if manage_db.check_table_exists(conn, table_name):
        pass
    else:
        manage_db.create_user_table(conn, table_name)
    try:
        for v in data['data']:
            if manage_db.check_if_video_exists(conn, table_name, v['id']):
                print(f"video already exists in db {v['id']}")
                return
            else:
                try:
                    # print(table_name, v['id'], v['title'], v['created_at'], v['published_at'], v['duration'], v['thumbnail_url'], v['view_count'], v['language'])
                    manage_db.insert_video(conn, table_name, v['id'], v['title'], v['created_at'], v['published_at'], v['duration'], v['thumbnail_url'], v['view_count'], v['language'])
                    print(f"ADDED video id {v['id']} for user {user_name}")
                except Exception as e:
                    print(e)
                    print(f"COULD NOT ADD VIDEO ID {v['id']} for user {user_name}")
    except Exception as e:
        print(e)
        return
    try:
        pag = data['pagination']['cursor']
    except Exception as e:
        print(e)
        return
    while True:
        url = f'https://api.twitch.tv/helix/videos?user_id={user_id}'
        params = {
            'first' : 100,
            'after': pag,
        }
        try:
            response = get_response(url, params)
            data = response.json()
        except Exception as e:
            print(e)
            return
        table_name = manage_db.get_table_name(user_name)
        if manage_db.check_table_exists(conn, table_name):
            pass
        else:
            manage_db.create_user_table(conn, table_name)
        try:
            for v in data['data']:
                if manage_db.check_if_video_exists(conn, table_name, v['id']):
                    print(f"video already exists in db {v['id']}")
                    return
                else:
                    try:
                        manage_db.insert_video(conn, table_name, v['id'], v['title'], v['created_at'], v['published_at'], v['duration'], v['thumbnail_url'], v['view_count'], v['language'])
                        print(f"ADDED video id {v['id']} for user {user_name}")
                    except Exception as e:
                        print(e)
                        print(f"COULD NOT ADD VIDEO ID {v['id']} for user {user_name}")
        except Exception as e:
            print(e)
            return
        try:
            pag = data['pagination']['cursor']
        except Exception as e:
            print(e)
            return

def download_video(url, user_name):
    os.system(f"yt-dlp --netrc-cmd '' -f 'bv*[height=480]+ba' --extractor-retries infinite -P videos/{user_name} {url}")

def dl_videos(video_list, user_name, max_threads=10):
    vl = []
    print(f"Video List for {user_name} is {video_list}")
    for i in video_list:
        vl.append("https://www.twitch.tv/videos/" + str(i))
    path_list= [user_name] * len(video_list)
    for i in range(len(video_list) // threads + 1):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            try:
                list(executor.map(download_video, vl[i*max_threads:(i+1)*max_threads], path_list[i*max_threads:(i+1)*max_threads]))
                manage_folders.rename_videos(user_name)
                for v in video_list[i*max_threads:(i+1)*max_threads]:
                    manage_db.set_video_downloaded(conn, manage_db.get_table_name(user_name), v, {'downloaded_yet': 1})
            except Exception as e:
                print(e)
                list(executor.map(download_video, vl[i*max_threads:len(video_list)-1], path_list[i*max_threads:len(video_list)-1]))
                manage_folders.rename_videos(user_name)
                for v in video_list[i*max_threads:len(video_list)-1]:
                    manage_db.set_video_downloaded(conn, manage_db.get_table_name(user_name), v, {'downloaded_yet': 1})

def thread_get_streamer(streamer_list, max_threads=10):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(get_streamer_videos, streamer) for streamer in streamer_list]
        concurrent.futures.wait(futures)

def is_english(string):
  pattern = re.compile(r'^[a-zA-Z]+$')
  return pattern.match(string) is not None

def get_profile_picture(streamer):
    if is_english(streamer):
        time.sleep(random.uniform(0.1, 2.3))
        try:
            chromedriver_executable = Service('chromedriver')
            options = Options()
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--incognito")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-extensions")
            options.add_argument('--ignore-ssl-errors')
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features")
            random_user_agent = random.choice(user_agent_list)
            options.add_argument(f"user-agent={random_user_agent}")
            driver = webdriver.Chrome(service = chromedriver_executable, options = options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.set_window_size(1920, 1080*3)
            driver.get(f"https://twitch.tv/{streamer}")
            user_agent = driver.execute_script("return window.navigator.userAgent")
            is_webdriver = driver.execute_script("return window.navigator.webdriver")
            print("User Agent:", user_agent)
            print("Webdriver is", is_webdriver)
            time.sleep(random.uniform(5.5, 6.5))
            try:
                os.system(f"mkdir screenshots/{streamer} > /dev/null 2>&1")
            except:
                pass
            driver.save_screenshot(f"screenshots/{streamer}/{get_timestamp()}_{streamer}.png")
            print(f"saved screenshot for {streamer} on {get_timestamp()}")
            driver.get(f"https://twitch.tv/{streamer}/about")
            time.sleep(random.uniform(5.5, 6.5))
            os.system(f"mkdir screenshots/{streamer}/about > /dev/null 2>&1")
            driver.save_screenshot(f"screenshots/{streamer}/about/{get_timestamp()}_{streamer}.png")
            print(f"saved screenshot for {streamer} about section on {get_timestamp()}")
        except Exception as e:
            print(e)
            print(f"could not save screenshot for {streamer} on {get_timestamp()}")

def thread_profile_picture(streamer_list, max_threads=160):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(get_profile_picture, streamer) for streamer in streamer_list]
        concurrent.futures.wait(futures)

def get_timestamp():
    timestamp = datetime.now()
    timestr = str(timestamp).replace(' ', '_')
    timestr = timestr.replace(':', '-')
    timestr = timestr[:-7]
    return timestr

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Usage of dl_twitch.py: incomplete; taking a RE exploit dump')
    parser.add_argument('streamers', nargs=argparse.REMAINDER, help='command line arugments for specific streamer names')
    parser.add_argument('-NV', action='store_true', help='no flag for videos to download')
    parser.add_argument('-TS', action='store_true', help='get top streamers and update all existing metadata')
    parser.add_argument('-NS', action='store_true', help='no flag for no screenshots to download')
    parser.add_argument('--USERS', action='store_true', help='build users pickle')
    parser.add_argument('--STAFF', action='store_true', help='get twitch staff data')
    #parser.add_argument('--CLEAN', action='store_true', help='clean up all folders and files and start fresh')
    parser.add_argument('--threads', type=int, help='number of threads to use')
    parser.add_argument('--pages', type=int, help='how many pages of streamers do you want to downlaod? 1 page = 100 streamers.')
    parser.add_argument('--authorization', type=str, help='https://twitchtokengenerator.com/')
    parser.add_argument('--client-id', type=str, help='https://dev.twitch.tv/console/apps/')
    parser.add_argument('--games', type=str, help='get all data from specific games query; eg query casino to get all casino games including slots, blackjack, etc.')
    args = parser.parse_args()
    authorization = args.authorization
    client_id = args.client_id
    games_query = args.games
    if args.pages:
        pages_to_dl = args.pages
    else:
        pages_to_dl = 300
    game_ids_list = []
    print("Games query:", games_query)
    if games_query:
        get_top_games.main()
        with open("top_games.pickle", "rb") as f:
                top_games = pickle.load(f)
        for game in top_games:
            if games_query.lower() in game.lower():
                game_ids_list.append(top_games[game]['id'])
    print("Game IDs List: ", game_ids_list)
    threads = args.threads
    if threads:
        pass
    else:
        threads = 10
    streamers_args = args.streamers
    if authorization:
        auth = 'Bearer ' + authorization
    else:
        auth = 'Bearer wz8car8y2up0fgf1w7ww8ilqwq9az8'
    if client_id:
        client_id = client_id
    else:
        client_id = 'gp762nuuoqcoxypju8c569th9wz7q5'

    manage_folders.make_root_folders()

    if len(sys.argv) < 2:
        print("Usage: python dl_twitch.py user_name or other command line arguments")
        sys.exit()
    
    streamer_set = set()
    for user_name in streamers_args:
        if user_name != "-NV" and user_name != "-TS":
            if get_user_id(user_name) != None:
                streamer_set.add(user_name.lower())
    if args.STAFF:
        with open("twitch_staff.pickle", "rb") as f:
            twitch_staff = pickle.load(f)
        for staff in twitch_staff:
            if is_english(staff):
                streamer_set.add(staff.lower())
    
    conn = manage_db.create_connection()
    manage_db.create_users_table(conn)

    print(f"Len streamer set is {len(streamer_set)}")
    if len(game_ids_list) > 0:
        for game_id in game_ids_list:
            game_streamers = get_top_streams(conn, game_id)
            print(f"Len streamer set is {len(streamer_set)}")
            for streamer in game_streamers:
                streamer_set.add(streamer)
            print(f"Len streamer set is {len(streamer_set)}")

    if args.TS or pages_to_dl != 300:
        top_streamers = get_top_streams(conn, None, pages_to_dl)
        for streamer in top_streamers:
            streamer_set.add(streamer)
        
    streamer_list = list(streamer_set)
    print(f"Length of current streamer_list to get metadata or download videos is {len(streamer_list)}")

    with open("run_log.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([get_timestamp(), len(streamer_list)])

    random.shuffle(streamer_list)

    if args.USERS:
        if os.path.exists("users.pickle"):
            with open("users.pickle", "rb") as f:
                users = pickle.load(f)
        else:
            users = {}
        for streamer in streamer_list:
            get_user.get_user_by_name(auth, client_id, streamer, users)
        with open("users.pickle", "wb") as f:
            pickle.dump(users, f)

    if "-NS" not in sys.argv:
        thread_profile_picture(streamer_list, threads)
    thread_get_streamer(streamer_list, threads)

    if "-NV" in sys.argv:
        print("You've entered the -NV tag so no videos are being downloaded!")
        sys.exit()
    elif "-TS" in sys.argv:
        check_user = input("You've entered TS parameters; are you sure you want to download all videos which takes forever? Please answer 'Yes' or else the program quits! ")
        if check_user != "Yes":
            print("You didn't answer 'Yes' so the program is exiting!")
            sys.exit()
    for user_name in streamer_list:
        try:
            os.mkdir(f"videos/{user_name}")
        except FileExistsError:
            pass
        video_list = manage_db.get_video_list(conn, user_name)
        sorted_list = sorted(video_list, reverse=True)
        dl_videos(sorted_list, user_name, threads)
        print(f"Finished downloading videos for {user_name}!")
    print("Finished downloading all videos!")

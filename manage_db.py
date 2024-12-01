import sqlite3
from sqlite3 import Error

def get_table_name(user_name):
    try:
        if int(user_name[0]):
            table_name = "_" + user_name
    except:
        table_name = user_name
    return(table_name)

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('twitch.db') 
        # print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def create_users_table(conn):
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY,
                user_name TEXT NOT NULL,
                max_viewer_count INTEGER NOT NULL,
                latest_viewer_count INTEGER NOT NULL,
                is_banned INTEGER NOT NULL
            );
        ''')
        print("users table created successfully.")
    except Error as e:
        print(e)

def check_table_exists(conn, table_name):
    """
    Check if a table exists
    """
    c = conn.cursor()
    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    result = c.fetchone()
    if result:
        return True
    else:
        return False
    
def insert_user(conn, user_id, user_name, latest_viewer_count, max_viewer_count):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (:user_id, :user_name, :max_viewer_count, :latest_viewer_count, :is_banned)", 
                      {'user_id': user_id, 'user_name': user_name, 'max_viewer_count': max_viewer_count, 
                       'latest_viewer_count': latest_viewer_count, 'is_banned': 0})
        print(f"Inserted {user_name} into users table")
    except Error as e:
        print(e)
    conn.commit()

def update_user(conn, user_id, new_values):
    try:
        c = conn.cursor()
        update_clause = ', '.join(f"{key} = :{key}" for key in new_values.keys())
        c.execute(f"UPDATE users SET {update_clause} WHERE user_id = :user_id", {**new_values, 'user_id': user_id})
        # print(f"User with id {user_id} updated successfully.")
        conn.commit()
    except:
        print(f"Cannot update user with id {user_id}")

def get_max_viewer_count(conn, user_name):
    try:
        c = conn.cursor()
        c.execute(f"SELECT max_viewer_count FROM users WHERE user_name = '{user_name}'")
        result = c.fetchone()
        # print(f"exisitng max viewer for {user_name} is {result}")
        return(result[0])
    except:
        print(f"Cannot manage_db.get_max_viewer_count({user_name})")
        return(0)

def get_video_list(conn, user_name):
    video_list = []
    try:
        if int(user_name[0]):
            table_name = "_" + user_name
    except:
        table_name = user_name
    try:
        c = conn.cursor()
        c.execute(f"SELECT video_id FROM {table_name} WHERE downloaded_yet = 0")
        video_ids = c.fetchall()
        for video in video_ids:
            video_list.append(video[0])
        return(video_list)
    except:
        print(f"Cannot manage_db.get_video_list({user_name})")
        return(video_list)

def create_user_table(conn, table_name):
    c = conn.cursor()
    try:
        c.execute(f'''
            CREATE TABLE {table_name} (
                video_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL,
                published_at TEXT NOT NULL,
                duration TEXT NOT NULL,
                thumbnail_url TEXT NOT NULL,
                view_count INTEGER NOT NULL,
                language TEXT NOT NULL,
                downloaded_yet INTEGER NOT NULL,
                cloud_url TEXT NOT NULL
            );
        ''')
        print(f"Table {table_name} created successfully.")
        conn.commit()
    except Error as e:
        print(e)

def check_if_video_exists(conn, table_name, video_id):
    c = conn.cursor()
    c.execute(f"SELECT video_id FROM {table_name} WHERE video_id = {video_id}")
    result = c.fetchone()
    if result:
        return True
    else:
        return False

def insert_video(conn, table_name, video_id, title, created_at, published_at, duration, thumbnail_url, view_count, language):
    try:
        c = conn.cursor()
        try:
            c.execute(f"INSERT INTO {table_name} VALUES (:video_id, :title, :created_at, :published_at, :duration, :thumbnail_url, :view_count, :language, :downloaded_yet, :cloud_url)", 
                    {'video_id': video_id, 'title': title, 
                    'created_at': created_at, 
                    'published_at': published_at, 
                    'duration': duration, 
                    'thumbnail_url': thumbnail_url, 
                    'view_count': view_count, 
                    'language': language, 
                    'downloaded_yet': 0,
                    'cloud_url': 'blank'})
            conn.commit()
        except:
            print(f"Cannot insert video_id {video_id} into {table_name}")
    except Error as e:
        print(e)

def set_video_downloaded(conn, table_name, video_id, new_values):
    try:
        c = conn.cursor()
        update_clause = ', '.join(f"{key} = :{key}" for key in new_values.keys())
        c.execute(f"UPDATE {table_name} SET {update_clause} WHERE video_id = :video_id", {**new_values, 'video_id': video_id})
    except:
        print(f"Cannot set video downloaded {video_id} in {table_name}")

def is_streamer_in_users(conn, user_name):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name=?", (user_name,))
        result = cursor.fetchone()
    except:
        result = None
    return result is not None

def get_user_id(conn, user_name):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_name=?", (user_name,))
        result = cursor.fetchone()
    except:
        result = None
    return result[0]
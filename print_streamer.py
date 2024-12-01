import sqlite3
from sqlite3 import Error
import sys

import manage_db

def is_streamer_in_users(user_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_name='{user_name}'")
    result = cursor.fetchone()
    return result is not None

def select_user(user_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_name = '{user_name}'")
    result = cursor.fetchone()
    return result

def get_column_names_from_users():
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    for column in columns:
        print(column[1])

def print_rows_from_users():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def print_videos(table_name):
    try:
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        for row in rows:
            print(row)
    except Error as e:
        print(e)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        user_name = sys.argv[1]
    elif len(sys.argv) == 1:
        user_name = input("Enter streamer name you want to get information for: ")
    else:
        print("Too many arguments!")
        sys.exit(1)
    conn = manage_db.create_connection()
    print(select_user(user_name))
    check = ""
    while check != "Y" and check != "N":
        check = input("Do you want to print streamer videos? (Y/N) or ctrl-c to quit: ")
        if check == "Y":
            print_videos(manage_db.get_table_name(user_name))
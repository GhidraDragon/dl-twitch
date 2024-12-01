import csv
import sys
import os

import get_user

def get_users_from_csv():
    if len(sys.argv) != 2 or sys.argv[1].endswith(".csv") == False:
        print("Usage: python3 import_from_csv.py <csv_filename>")
        sys.exit(1)
    with open(sys.argv[1], mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            get_user.get_users([row[0]])

if __name__ == "__main__":
    get_users_from_csv()
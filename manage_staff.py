import pickle
import sys
import csv

with (open("twitch_staff.pickle", "rb")) as f:
    staff_set = pickle.load(f)

for staff in sys.argv[1:]:
    staff_set.add(staff.lower())

with (open("twitch_staff.csv", "w")) as f:
    writer = csv.writer(f)
    for staff in staff_set:
        writer.writerow([staff])

with (open("twitch_staff.pickle", "wb")) as f:
    pickle.dump(staff_set, f)


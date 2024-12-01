import pickle
with open("twitch_staff.pickle", "rb") as f:
    twitch_staff = pickle.load(f)

for staff in twitch_staff:
    print(staff)
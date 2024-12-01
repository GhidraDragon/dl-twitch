import pickle
with open("users.pickle", "rb") as f:
    users = pickle.load(f)
for user in users:
    print(user, users[user])
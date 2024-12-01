import pickle

with open("top_games.pickle", "rb") as f:
    top_games = pickle.load(f)

for game in top_games:
    if "casino" in game:
        print(game, top_games[game]['id'])
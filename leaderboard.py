import json
from player_data import load_players

def get_leaderboard():
    players = load_players()
    sorted_players = sorted(players.items(), key=lambda x: x[1]['coins'], reverse=True)
    return sorted_players[:10]

import time
from player_data import update_player_data

CHECKIN_INTERVAL = 300  # 5 minutes

last_checkin = {}

def can_checkin(user_id):
    now = time.time()
    last = last_checkin.get(user_id, 0)
    if now - last >= CHECKIN_INTERVAL:
        last_checkin[user_id] = now
        return True
    return False

def checkin(user_id):
    if can_checkin(user_id):
        update_player_data(user_id, 100)
        return True
    return False

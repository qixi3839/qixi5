from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_game_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("抽牌", callback_data='hit'), InlineKeyboardButton("停牌", callback_data='stand')],
        [InlineKeyboardButton("查看余额", callback_data='balance'), InlineKeyboardButton("领取金币", callback_data='checkin')],
        [InlineKeyboardButton("排行榜", callback_data='leaderboard')]
    ])

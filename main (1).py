
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random
import datetime

TOKEN = "YOUR_BOT_TOKEN"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# 简单的内存数据存储
users = {}
last_checkin = {}

def get_score(cards):
    score = sum(cards)
    return score

def draw_card():
    return random.randint(1, 11)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.setdefault(user_id, {"balance": 100, "cards": [], "score": 0})
    await update.message.reply_text("欢迎来到 21 点游戏！发送 /join 开始游戏。")

async def checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = datetime.datetime.now()
    last_time = last_checkin.get(user_id)

    if not last_time or (now - last_time).seconds >= 300:
        users.setdefault(user_id, {"balance": 100, "cards": [], "score": 0})
        users[user_id]["balance"] += 20
        last_checkin[user_id] = now
        await update.message.reply_text("✅ 签到成功，获得 20 金币！")
    else:
        await update.message.reply_text("❌ 每 5 分钟才能签到一次，请稍后再来。")

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {"balance": 100, "cards": [], "score": 0}

    users[user_id]["cards"] = [draw_card(), draw_card()]
    users[user_id]["score"] = get_score(users[user_id]["cards"])

    keyboard = [
        [InlineKeyboardButton("要牌", callback_data="hit"),
         InlineKeyboardButton("停牌", callback_data="stand")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"你的牌: {users[user_id]['cards']}
当前点数: {users[user_id]['score']}",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "hit":
        card = draw_card()
        users[user_id]["cards"].append(card)
        users[user_id]["score"] = get_score(users[user_id]["cards"])
        if users[user_id]["score"] > 21:
            await query.edit_message_text(f"你抽了 {card}，当前点数：{users[user_id]['score']}，爆了💥！")
        else:
            keyboard = [
                [InlineKeyboardButton("要牌", callback_data="hit"),
                 InlineKeyboardButton("停牌", callback_data="stand")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"你抽了 {card}，当前牌: {users[user_id]['cards']}
点数: {users[user_id]['score']}",
                reply_markup=reply_markup
            )
    elif query.data == "stand":
        await query.edit_message_text(f"你停牌，最终点数为: {users[user_id]['score']}。
等待庄家操作...")

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorted_users = sorted(users.items(), key=lambda x: x[1]["balance"], reverse=True)
    text = "🏆 排行榜（金币）:
"
    for i, (uid, data) in enumerate(sorted_users[:10], start=1):
        name = context.bot.get_chat(uid).first_name if context.bot.get_chat(uid) else str(uid)
        text += f"{i}. {name} - {data['balance']}💰
"
    await update.message.reply_text(text)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("checkin", checkin))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()

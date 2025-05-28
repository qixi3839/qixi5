
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler
from game import BlackjackGame, PlayerManager

TOKEN = "YOUR_BOT_TOKEN"  # 替换为你的 BotFather 提供的 Token

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

game = BlackjackGame()
players = PlayerManager()

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await update.message.reply_text("🎮 欢迎来到 Telegram 二十一点！输入 /join 加入游戏。")

async def join(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    players.add_player(user_id, user_name)
    await update.message.reply_text(f"{user_name} 已加入游戏！输入 /hit 抽牌 或 /stand 停牌。")

async def hit(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not players.in_game(user_id):
        return await update.message.reply_text("请先输入 /join 加入游戏。")
    card = game.draw_card(user_id)
    await update.message.reply_text(f"你抽到：{card}。总点数：{game.get_score(user_id)}")
    if game.is_bust(user_id):
        await update.message.reply_text("💥 爆牌！")

async def stand(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user_id = update.effective_user.id
    score = game.get_score(user_id)
    game.stand(user_id)
await update.message.reply_text(f"你选择停牌，最终点数：{score}。")
await update.message.reply_text("等待其他玩家操作...")

async def balance(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user_id = update.effective_user.id
    coins = players.get_balance(user_id)
    await update.message.reply_text(f"💰 当前金币余额：{coins}")

async def daily(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user_id = update.effective_user.id
    result = players.claim_daily(user_id)
    await update.message.reply_text(result)

async def leaderboard(update: Update, context: CallbackContext.DEFAULT_TYPE):
    text = players.get_leaderboard()
    await update.message.reply_text(text)

async def help_command(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await update.message.reply_text("/join - 加入游戏
/hit - 抽牌
/stand - 停牌
/balance - 查看余额
/daily - 5分钟领金币
/leaderboard - 查看排行榜")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("hit", hit))
    app.add_handler(CommandHandler("stand", stand))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("help", help_command))
    app.run_polling()

if __name__ == "__main__":
    main()

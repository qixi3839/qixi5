
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

class BlackjackGame:
    def __init__(self):
        self.players = {}
        self.dealer = []
        self.scores = {}
        self.coins = {}
        self.cooldowns = {}

    def register_handlers(self, app):
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("join", self.join_game))
        app.add_handler(CommandHandler("hit", self.hit))
        app.add_handler(CommandHandler("stand", self.stand))
        app.add_handler(CommandHandler("help", self.help))
        app.add_handler(CommandHandler("balance", self.balance))
        app.add_handler(CommandHandler("daily", self.daily_coins))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🎉 欢迎来到 21 点游戏！输入 /join 加入游戏。")

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("/join 加入游戏\n/hit 要牌\n/stand 停牌\n/balance 查看余额\n/daily 签到领金币")

    async def join_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        name = update.effective_user.first_name
        if user_id in self.players:
            await update.message.reply_text(f"{name} 已经在游戏中。")
            return

        self.players[user_id] = {
            'cards': [self.draw_card(), self.draw_card()],
            'stand': False
        }
        self.coins.setdefault(user_id, 1000)

        await update.message.reply_text(
            f"{name} 加入了游戏。\n初始牌：{self._format_cards(self.players[user_id]['cards'])} 总点数：{self._calculate_points(self.players[user_id]['cards'])}"
        )

    async def hit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        name = update.effective_user.first_name
        if user_id not in self.players:
            await update.message.reply_text("请先输入 /join 加入游戏。")
            return
        if self.players[user_id]['stand']:
            await update.message.reply_text("你已经停牌，不能再要牌。")
            return

        self.players[user_id]['cards'].append(self.draw_card())
        total = self._calculate_points(self.players[user_id]['cards'])
        msg = f"{name} 要了一张牌：{self._format_cards(self.players[user_id]['cards'])} 总点数：{total}"

        if total > 21:
            msg += " 💥 爆掉了！"
        await update.message.reply_text(msg)

    async def stand(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.players[user_id]['stand'] = True
        await update.message.reply_text("你已停牌，等待庄家操作。")

    async def balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        coins = self.coins.get(user_id, 0)
        await update.message.reply_text(f"你的余额是：{coins} 💰")

    async def daily_coins(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        import time
        user_id = update.effective_user.id
        now = time.time()
        last = self.cooldowns.get(user_id, 0)
        if now - last >= 300:  # 5分钟
            self.cooldowns[user_id] = now
            self.coins[user_id] = self.coins.get(user_id, 0) + 100
            await update.message.reply_text("领取成功，获得100金币 💰")
        else:
            await update.message.reply_text("领取过于频繁，请5分钟后再试。")

    def draw_card(self):
        return random.choice(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"])

    def _calculate_points(self, cards):
        total = 0
        aces = 0
        for card in cards:
            if card in ["J", "Q", "K"]:
                total += 10
            elif card == "A":
                aces += 1
                total += 11
            else:
                total += int(card)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def _format_cards(self, cards):
        return " ".join([f"🂠{c}" for c in cards])

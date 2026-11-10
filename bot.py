import os
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import (Application, CommandHandler, CallbackQueryHandler,
                          PreCheckoutQueryHandler, MessageHandler, filters,
                          ContextTypes)

TOKEN = os.environ["BOT_TOKEN"]
PROVIDER_TOKEN = os.environ["PROVIDER_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
PRICE_SOM = 100000  # narxni o'zgartiring

web = Flask(__name__)

@web.route("/")
def home():
    return "Bot ishlayapti"

def run_web():
    web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("💳 To'lov qilish", callback_data="buy")]])
    await update.message.reply_text(
        f"Assalomu alaykum, {update.effective_user.first_name}! 👋\n"
        "Yopiq kanalga kirish uchun to'lovni amalga oshiring.",
        reply_markup=kb)

async def buy(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await ctx.bot.send_invoice(
        chat_id=q.message.chat_id,
        title="Kanalga kirish",
        description="Yopiq kanalga to'liq kirish",
        payload="channel_access",
        provider_token=PROVIDER_TOKEN,
        currency="UZS",
        prices=[LabeledPrice("Kanal", PRICE_SOM * 100)])  # tiyinda

async def precheckout(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

async def paid(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    link = await ctx.bot.create_chat_invite_link(chat_id=CHANNEL_ID, member_limit=1)
    await update.message.reply_text(
        f"✅ To'lov qabul qilindi, rahmat!\nKanalga kirish: {link.invite_link}")

Thread(target=run_web, daemon=True).start()

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buy, pattern="^buy$"))
app.add_handler(PreCheckoutQueryHandler(precheckout))
app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, paid))
app.run_polling()

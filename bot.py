import os
from flask import Flask
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ishlayapti ✅")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

web = Flask(__name__)
@web.route('/')
def home():
    return "Bot ishlayapti ✅"

threading.Thread(target=lambda: web.run(host='0.0.0.0', port=10000)).start()

app.run_polling()

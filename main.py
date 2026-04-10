import logging
import os
import asyncio
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler
)

# ================= লগিং =================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ================= Flask =================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# ================= CONFIG =================
BOT_TOKEN = "8511299158:AAFXkGzhz5Li22MXmXl1wThQLaSGp0om2Lc"
ADMIN_ID = 7406442919
REQUIRED_CHANNEL_ID = -1001481593780
LINK_REGISTRATION = "https://bit.ly/BLACK220"
CHANNEL_INVITE_LINK = "https://t.me/+3U0nMzWs4Aw0YjFl"
ADMIN_USER_LINK = "https://t.me/SUNNY_BRO1"

IMG_START = "https://i.ibb.co.com/7dDFg5WQ/new-updear-photo.png"
IMG_LANG = "https://i.ibb.co.com/23VVWgSS/file-00000000d21472088a8b84f9b1faa902.png"
IMG_CHOOSE_PLATFORM = "https://i.ibb.co.com/NdFDsT4P/file-000000005308720880754a5daa131c74.png"
IMG_REGISTRATION = "https://i.ibb.co.com/NdFDsT4P/file-000000005308720880754a5daa131c74.png"
FINAL_IMAGE_URL = "https://i.ibb.co.com/xy9RwRS/opnen-haxl.png"
WEBAPP_URL = "https://1xbet-melbet-apple.unaux.com/"
USER_FILE = "users.txt"

# ================= TEXT =================
TEXTS = {
    'bn': {
        'join_msg': "👋 <b>হ্যালো {name}!</b>\n\nবটটি ব্যবহার করতে আমাদের চ্যানেলে জয়েন করুন।",
        'choose_platform_caption': "🎮 <b>প্ল্যাটফর্ম নির্বাচন করুন</b>",
        'btn_help': "🆘 সাহায্য",
        'reg_title': "🚀 <b>{platform} রেজিস্ট্রেশন</b>",
        'reg_msg': "⚠️ আমাদের লিংক ব্যবহার করুন!",
        'btn_reg_link': "🔗 রেজিস্ট্রেশন",
        'btn_next': "✅ Done",
        'wait_msg': "⏳ Checking...",
        'ask_id': "📩 ID পাঠান",
        'error_length': "❌ ভুল ID",
        'success_caption': "✅ Success ID: <code>{uid}</code>",
        'btn_open_hack': "🍎 Open Hack",
        'btn_contact': "👨‍💻 Admin"
    }
}

# ================= STATES =================
START, SELECT_LANGUAGE, CHOOSE_PLATFORM, WAITING_FOR_ID = range(4)

# ================= USER SAVE =================
def save_user(uid):
    if not os.path.exists(USER_FILE):
        open(USER_FILE, "w").close()
    with open(USER_FILE, "r") as f:
        users = f.read().splitlines()
    if str(uid) not in users:
        with open(USER_FILE, "a") as f:
            f.write(f"{uid}\n")

# ================= MEMBERSHIP =================
async def check_membership(update, context):
    try:
        member = await context.bot.get_chat_member(REQUIRED_CHANNEL_ID, update.effective_user.id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)

    is_member = await check_membership(update, context)

    if not is_member:
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_INVITE_LINK)],
            [InlineKeyboardButton("✅ I Joined", callback_data='check_join')]
        ]

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=IMG_START,
            caption=TEXTS['bn']['join_msg'].format(name=user.first_name),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
        return START

    # Language select
    keyboard = [[InlineKeyboardButton("🇧🇩 বাংলা", callback_data='lang_bn')]]

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=IMG_LANG,
        caption="Language Select করুন",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )
    return SELECT_LANGUAGE

# ================= CHECK JOIN BUTTON =================
async def check_join_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    is_member = await check_membership(update, context)

    if not is_member:
        await query.answer("❌ আগে চ্যানেলে জয়েন করুন!", show_alert=True)
        return START

    # joined হলে next step
    await query.message.delete()

    keyboard = [[InlineKeyboardButton("🔵 1XBET", callback_data='platform_1xbet')]]

    await context.bot.send_photo(
        chat_id=query.message.chat.id,
        photo=IMG_CHOOSE_PLATFORM,
        caption=TEXTS['bn']['choose_platform_caption'],
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )
    return CHOOSE_PLATFORM

# ================= PLATFORM =================
async def platform_callback(update, context):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🔗 Register", url=LINK_REGISTRATION)],
        [InlineKeyboardButton("✅ Next", callback_data='go_verify')]
    ]

    await query.message.delete()

    await context.bot.send_photo(
        chat_id=query.message.chat.id,
        photo=IMG_REGISTRATION,
        caption="রেজিস্ট্রেশন করুন",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return CHOOSE_PLATFORM

# ================= ASK ID =================
async def ask_id(update, context):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text("ID পাঠান")
    return WAITING_FOR_ID

# ================= VERIFY =================
async def verify(update, context):
    uid = update.message.text

    if not uid.isdigit():
        await update.message.reply_text("❌ ভুল")
        return WAITING_FOR_ID

    keyboard = [[InlineKeyboardButton("🍎 Open", web_app=WebAppInfo(url=WEBAPP_URL))]]

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=FINAL_IMAGE_URL,
        caption=f"✅ ID: {uid}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return ConversationHandler.END

# ================= MAIN =================
if __name__ == '__main__':
    keep_alive()

    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [CallbackQueryHandler(check_join_callback, pattern='check_join')],
            SELECT_LANGUAGE: [CallbackQueryHandler(platform_callback, pattern='lang_')],
            CHOOSE_PLATFORM: [
                CallbackQueryHandler(platform_callback, pattern='platform_'),
                CallbackQueryHandler(ask_id, pattern='go_verify')
            ],
            WAITING_FOR_ID: [MessageHandler(filters.TEXT, verify)]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    app_bot.add_handler(conv)

    print("Bot Running...")
    app_bot.run_polling()

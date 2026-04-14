import logging
import os
import asyncio
from threading import Thread
from flask import Flask
import firebase_admin
from firebase_admin import credentials, db
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

# ================= লগিং কনফিগারেশন =================
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ================= ফায়ারবেস সেটআপ =================
# আপনার দেওয়া JSON ফাইলটি 'firebase-key.json' নামে সেভ থাকতে হবে
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://telegram-60f96-default-rtdb.firebaseio.com/' # <--- আপনার ডাটাবেস ইউআরএল এখানে দিন
})

# ================= ডাটাবেস ফাংশন =================
def save_user_to_firebase(user):
    """ইউজার ডাটা ফায়ারবেসে সেভ করে"""
    ref = db.reference(f'users/{user.id}')
    if not ref.get():
        ref.set({
            'id': user.id,
            'first_name': user.first_name,
            'username': user.username,
            'status': 'active'
        })
        logger.info(f"New user saved to Firebase: {user.id}")

def get_all_users():
    """সব ইউজারের আইডি লিস্ট দেয়"""
    ref = db.reference('users')
    users = ref.get()
    return list(users.keys()) if users else []

# ================= ওয়েব সার্ভার (Railway) =================
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running 24/7 with Firebase!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# ================= কনফিগারেশন =================
BOT_TOKEN = "8511299158:AAFXkGzhz5Li22MXmXl1wThQLaSGp0om2Lc"
ADMIN_ID = 7406442919  
REQUIRED_CHANNEL_ID = "-1001481593780"
PROMO_CODES = {"1XBET": "BLACK696", "MELBET": "BETBD666"}
LINK_REGISTRATION = "https://bit.ly/BLACK220" 
CHANNEL_INVITE_LINK = "https://t.me/+3U0nMzWs4Aw0YjFl"
ADMIN_USER_LINK = "https://t.me/SUNNY_BRO1"
WEBAPP_URL = "https://1xbet-melbet-apple.unaux.com/"

# Images
IMG_START = "https://i.ibb.co.com/23VVWgSS/file-00000000d21472088a8b84f9b1faa902.png"
IMG_LANG = "https://i.ibb.co.com/23VVWgSS/file-00000000d21472088a8b84f9b1faa902.png"
IMG_CHOOSE_PLATFORM = "https://i.ibb.co.com/NdFDsT4P/file-000000005308720880754a5daa131c74.png"
IMG_REGISTRATION = "https://i.ibb.co.com/NdFDsT4P/file-000000005308720880754a5daa131c74.png"
FINAL_IMAGE_URL = "https://i.ibb.co.com/vxfM0vv5/file-00000000f15071fa8c883abb1421fa69.png"

# ================= TEXTS =================
TEXTS = {
    'en': {
        'choose_platform_caption': "🎮 <b>CHOOSE YOUR PLATFORM</b>\n\nWhich casino do you want to hack? Select below 👇",
        'btn_help': "🆘 Help / Support",
        'reg_title': "🚀 <b>{platform} REGISTRATION</b>",
        'reg_msg': "⚠️ <b>WARNING:</b> Hack works ONLY with our Link!\n\n1️⃣ Delete old account.\n2️⃣ Click 'Register' (Use promo <code>{promo}</code>).\n3️⃣ Create account and send ID.",
        'btn_reg_link': "🔗 Register {platform}",
        'btn_next': "✅ I Registered (Verify ID)",
        'wait_msg': "⏳ <b>Connecting to Server...</b>",
        'ask_id': "📩 <b>SEND YOUR NEW ID</b>",
        'error_digit': "❌ Digits only.",
        'error_length': "❌ Invalid ID length.",
        'success_caption': "✅ <b>VERIFIED!</b>\n🆔 ID: <code>{uid}</code>\nPromo: <b>{promo}</b>",
        'btn_open_hack': "🍎 OPEN HACK (WebApp)",
        'btn_contact': "👨‍💻 Contact Admin"
    },
    'bn': {
        'choose_platform_caption': "🎮 <b>প্ল্যাটফর্ম নির্বাচন করুন</b>\nনিচে থেকে ক্যাসিনো সিলেক্ট করুন 👇",
        'btn_help': "🆘 সাহায্য / সাপোর্ট",
        'reg_title': "🚀 <b>{platform} রেজিস্ট্রেশন</b>",
        'reg_msg': "⚠️ <b>সতর্কতা:</b> হ্যাকটি শুধুমাত্র আমাদের লিংকে কাজ করবে!\n\n1️⃣ পুরনো একাউন্ট ডিলিট করুন।\n2️⃣ রেজিস্ট্রেশন করুন (প্রোমো: <code>{promo}</code>)।\n3️⃣ আইডি পাঠান।",
        'btn_reg_link': "🔗 {platform} রেজিস্ট্রেশন লিংক",
        'btn_next': "✅ রেজিস্ট্রেশন করেছি",
        'wait_msg': "⏳ <b>সার্ভারে কানেক্ট হচ্ছে...</b>",
        'ask_id': "📩 <b>আপনার আইডি পাঠান</b>",
        'error_digit': "❌ শুধুমাত্র সংখ্যা পাঠান।",
        'error_length': "❌ ভুল আইডি।",
        'success_caption': "✅ <b>ভেরিফাইড সফল!</b>\n🆔 ID: <code>{uid}</code>\nপ্রোমো: <b>{promo}</b>",
        'btn_open_hack': "🍎 হ্যাক চালু করুন (WebApp)",
        'btn_contact': "👨‍💻 এডমিন সাপোর্ট"
    }
}

# ================= STATES =================
CHECK_JOIN, SELECT_LANGUAGE, CHOOSE_PLATFORM, WAITING_FOR_ID = range(4)
ADMIN_MENU, ADMIN_GET_CONTENT, ADMIN_CONFIRM = range(10, 13)

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL_ID, user_id=update.effective_user.id)
        return member.status in ['creator', 'administrator', 'member']
    except: return False

async def safe_send_photo(context, chat_id, photo, caption=None, reply_markup=None):
    try:
        await context.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=reply_markup, parse_mode='HTML')
    except:
        await context.bot.send_message(chat_id=chat_id, text=caption, reply_markup=reply_markup, parse_mode='HTML')

# ================= হ্যান্ডলারস =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user_to_firebase(user) # ফায়ারবেসে সেভ হচ্ছে
    context.user_data.clear()

    if not await check_membership(update, context):
        keyboard = [[InlineKeyboardButton("📢 Join Channel", url=CHANNEL_INVITE_LINK)],
                    [InlineKeyboardButton("✅ I Have Joined", callback_data='check_join_status')]]
        await safe_send_photo(context, update.effective_chat.id, IMG_START, f"👋 Hello {user.first_name}!\nJoin channel to use this bot.", InlineKeyboardMarkup(keyboard))
        return CHECK_JOIN
    
    await show_language_menu(update, context)
    return SELECT_LANGUAGE

async def check_join_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if await check_membership(update, context):
        await show_language_menu(update, context)
        return SELECT_LANGUAGE
    else:
        await query.message.reply_text("❌ Join first!")
        return CHECK_JOIN

async def show_language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🇺🇸 English", callback_data='lang_en'), InlineKeyboardButton("🇧🇩 বাংলা", callback_data='lang_bn')]]
    if update.callback_query:
        try: await update.callback_query.message.delete()
        except: pass
    await safe_send_photo(context, update.effective_chat.id, IMG_LANG, "🌐 Select Language:", InlineKeyboardMarkup(keyboard))

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['lang'] = query.data.split('_')[1]
    
    lang = context.user_data['lang']
    t = TEXTS[lang]
    keyboard = [[InlineKeyboardButton("🔵 1XBET", callback_data='platform_1XBET'), InlineKeyboardButton("🟡 MELBET", callback_data='platform_MELBET')],
                [InlineKeyboardButton(t['btn_help'], url=ADMIN_USER_LINK)]]
    try: await query.message.delete()
    except: pass
    await safe_send_photo(context, update.effective_chat.id, IMG_CHOOSE_PLATFORM, t['choose_platform_caption'], InlineKeyboardMarkup(keyboard))
    return CHOOSE_PLATFORM

async def platform_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    platform = query.data.split('_')[1]
    context.user_data['chosen_platform'] = platform
    lang = context.user_data.get('lang', 'en')
    t = TEXTS[lang]
    promo = PROMO_CODES.get(platform)
    
    text = f"{t['reg_title'].format(platform=platform)}\n\n{t['reg_msg'].format(promo=promo)}"
    keyboard = [[InlineKeyboardButton(t['btn_reg_link'].format(platform=platform), url=LINK_REGISTRATION)],
                [InlineKeyboardButton(t['btn_next'], callback_data='account_created')]]
    try: await query.message.delete()
    except: pass
    await safe_send_photo(context, update.effective_chat.id, IMG_REGISTRATION, text, InlineKeyboardMarkup(keyboard))
    return CHOOSE_PLATFORM

async def wait_and_ask_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'en')
    msg = await query.message.reply_text(TEXTS[lang]['wait_msg'], parse_mode='HTML')
    await asyncio.sleep(3)
    try: await msg.delete()
    except: pass
    await query.message.reply_text(TEXTS[lang]['ask_id'], parse_mode='HTML')
    return WAITING_FOR_ID

async def receive_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()
    lang = context.user_data.get('lang', 'en')
    t = TEXTS[lang]
    if not uid.isdigit() or len(uid) < 9:
        await update.message.reply_text(t['error_digit'])
        return WAITING_FOR_ID
    
    platform = context.user_data.get('chosen_platform', '1XBET')
    promo = PROMO_CODES.get(platform)
    keyboard = [[InlineKeyboardButton(t['btn_open_hack'], web_app=WebAppInfo(url=WEBAPP_URL))],
                [InlineKeyboardButton(t['btn_contact'], url=ADMIN_USER_LINK)]]
    
    await safe_send_photo(context, update.effective_chat.id, FINAL_IMAGE_URL, t['success_caption'].format(uid=uid, promo=promo), InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END

# ================= অ্যাডমিন ব্রডকাস্ট =================
async def admin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    await update.message.reply_text("👑 Admin: Send me the message (Text/Photo) to broadcast.")
    return ADMIN_GET_CONTENT

async def admin_get_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['bc_msg'] = update.message
    await update.message.reply_text("Confirm? Type /send to broadcast to all.")
    return ADMIN_CONFIRM

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_ids = get_all_users()
    msg = context.user_data['bc_msg']
    count = 0
    await update.message.reply_text(f"🚀 Sending to {len(user_ids)} users...")
    for uid in user_ids:
        try:
            await context.bot.copy_message(chat_id=uid, from_chat_id=msg.chat_id, message_id=msg.message_id)
            count += 1
            await asyncio.sleep(0.05)
        except: pass
    await update.message.reply_text(f"✅ Sent to {count} users.")
    return ConversationHandler.END

# ================= মেইন =================
if __name__ == '__main__':
    keep_alive()
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    user_conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHECK_JOIN: [CallbackQueryHandler(check_join_callback, pattern='^check_join_status$')],
            SELECT_LANGUAGE: [CallbackQueryHandler(set_language, pattern='^lang_')],
            CHOOSE_PLATFORM: [
                CallbackQueryHandler(platform_choice, pattern='^platform_'),
                CallbackQueryHandler(wait_and_ask_id, pattern='^account_created$')
            ],
            WAITING_FOR_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_id)],
        },
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True
    )

    admin_conv = ConversationHandler(
        entry_points=[CommandHandler('admin', admin_start)],
        states={
            ADMIN_GET_CONTENT: [MessageHandler(filters.ALL, admin_get_content)],
            ADMIN_CONFIRM: [CommandHandler('send', admin_broadcast)]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    application.add_handler(user_conv)
    application.add_handler(admin_conv)
    print("Bot with Firebase is running...")
    application.run_polling()

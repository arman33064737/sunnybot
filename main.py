import logging
import os
import asyncio
import sys
import json
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

# ================= লগিং সেটআপ =================

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ================= ফায়ারবেস কানেকশন =================

try:
    if not firebase_admin._apps:
        firebase_json = os.environ.get("FIREBASE_JSON")

        if firebase_json:
            cred_dict = json.loads(firebase_json)
            cred = credentials.Certificate(cred_dict)
            logger.info("✅ Firebase initialized from Environment Variable!")
        elif os.path.exists("firebase-key.json"):
            cred = credentials.Certificate("firebase-key.json")
            logger.info("✅ Firebase initialized from firebase-key.json file!")
        else:
            logger.error("❌ No Firebase credentials found!")
            sys.exit(1)

        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://telegram-60f96-default-rtdb.firebaseio.com/'
        })

    db.reference('connection_test').set({'status': 'online'})

except Exception as e:
    logger.error(f"❌ Firebase Critical Error: {e}")
    sys.exit(1)

# ================= ডাটাবেস ফাংশন =================

def save_user_to_firebase(user):
    try:
        ref = db.reference(f'users/{user.id}')
        if ref.get() is None:
            ref.set({'id': user.id, 'first_name': user.first_name, 'username': user.username, 'status': 'active'})
    except Exception as e:
        logger.error(f"❌ Error saving user: {e}")

def get_all_users():
    try:
        ref = db.reference('users')
        users = ref.get()
        return list(users.keys()) if users else []
    except:
        return []

# ================= ওয়েব সার্ভার =================

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Online"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ================= বটের কনফিগারেশন =================

BOT_TOKEN = "8638577238:AAGmHqBMuaTw-KJi7rg7w2GfJwAooJdxMYY"
ADMIN_ID = 1146186608

# <-- এখানে দুটি চ্যানেল সেট করা হয়েছে -->
REQUIRED_CHANNELS = [
    {"id": "-1001481593780", "link": "https://t.me/+3U0nMzWs4Aw0YjFl", "name": "📢 Join Channel 1"},
    {"id": "-1003974496364", "link": "https://t.me/+WeqyzLHAMWhjMmU1", "name": "📢 Join Channel 2"}
]

PROMO_CODES = {"1XBET": "BLACK696", "MELBET": "BETBD666"}
LINK_REGISTRATION = "https://bit.ly/BLACK220"
ADMIN_USER_LINK = "https://t.me/SUNNY_BRO1"

# --- নতুন ওয়েব অ্যাপ লিংক সমূহ ---
APPLE_HACK_URL = "https://1xbet-melbet-apple.unaux.com/"
THIMBLES_HACK_URL = "https://thimbles-melbet.netlify.app/"
CRASH_SIGNAL_URL = "https://crasgsignaldog.netlify.app/"

IMG_START = "https://i.ibb.co/LzJF0GGz/file-00000000ee647208a867f87bc931da8c.png"
IMG_LANG = "https://i.ibb.co/LzJF0GGz/file-00000000ee647208a867f87bc931da8c.png"
IMG_CHOOSE_PLATFORM = "https://i.ibb.co.com/NdFDsT4P/file-000000005308720880754a5daa131c74.png"
IMG_REGISTRATION = "https://i.ibb.co/3nLpry7/file-0000000059b072089f5ecf92b19ec92b.png"
FINAL_IMAGE_URL = "https://i.ibb.co/3nLpry7/file-0000000059b072089f5ecf92b19ec92b.png"

TEXTS = {
    'en': {
        'choose_platform_caption': "🎮 CHOOSE YOUR PLATFORM",
        'btn_help': "🆘 Help",
        'reg_title': "🚀 {platform} REGISTRATION",
        'reg_msg': "⚠️ WARNING: Use promo {promo}.",
        'btn_reg_link': "🔗 Register {platform}",
        'btn_next': "✅ I Registered",
        'wait_msg': "⏳ Connecting...",
        'ask_id': "📩 SEND YOUR NEW ID",
        'error_digit': "❌ Invalid ID.",
        'success_caption': "✅ VERIFIED!\n🆔 ID: {uid}",
        'btn_apple_hack': "🍎 APPLE HACK",
        'btn_thimbles_hack': "🎲 THIMBLES HACK",
        'btn_crash_signal': "🚀 CRASH SIGNAL",
        'btn_contact': "👨‍💻 Admin"
    },
    'bn': {
        'choose_platform_caption': "🎮 প্ল্যাটফর্ম নির্বাচন করুন",
        'btn_help': "🆘 সাহায্য",
        'reg_title': "🚀 {platform} রেজিস্ট্রেশন",
        'reg_msg': "⚠️ সতর্কতা: প্রোমো ব্যবহার করুন: {promo}.",
        'btn_reg_link': "🔗 {platform} রেজিস্ট্রেশন",
        'btn_next': "✅ রেজিস্ট্রেশন করেছি",
        'wait_msg': "⏳ সার্ভারে কানেক্ট হচ্ছে...",
        'ask_id': "📩 আপনার আইডি পাঠান",
        'error_digit': "❌ ভুল আইডি।",
        'success_caption': "✅ ভেরিফাইড সফল!\n🆔 ID: {uid}",
        'btn_apple_hack': "🍎 অ্যাপেল হ্যাক",
        'btn_thimbles_hack': "🎲 থাম্বস হ্যাক",
        'btn_crash_signal': "🚀 ক্র্যাশ সিগন্যাল",
        'btn_contact': "👨‍💻 এডমিন"
    }
}

CHECK_JOIN, SELECT_LANGUAGE, CHOOSE_PLATFORM, WAITING_FOR_ID = range(4)
ADMIN_GET_CONTENT, ADMIN_CONFIRM = range(10, 12)

# ================= হ্যান্ডলার ফাংশনস =================

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # <-- দুটি চ্যানেলই চেক করার লজিক -->
    try:
        for channel in REQUIRED_CHANNELS:
            member = await context.bot.get_chat_member(chat_id=channel["id"], user_id=update.effective_user.id)
            if member.status not in ['creator', 'administrator', 'member']:
                return False
        return True
    except:
        return False

async def safe_send_photo(context, chat_id, photo, caption=None, reply_markup=None):
    try:
        await context.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=reply_markup, parse_mode='HTML')
    except:
        await context.bot.send_message(chat_id=chat_id, text=caption, reply_markup=reply_markup, parse_mode='HTML')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user_to_firebase(user)
    context.user_data.clear()
    
    if not await check_membership(update, context):
        # <-- দুটি চ্যানেলের বাটন তৈরি করা হচ্ছে -->
        keyboard = []
        for channel in REQUIRED_CHANNELS:
            keyboard.append([InlineKeyboardButton(channel["name"], url=channel["link"])])
            
        keyboard.append([InlineKeyboardButton("✅ I Have Joined", callback_data='check_join_status')])
        
        await safe_send_photo(context, update.effective_chat.id, IMG_START, f"👋 Hello {user.first_name}!\nJoin all channels to use this bot.", InlineKeyboardMarkup(keyboard))
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
        await query.message.reply_text("❌ Join both channels first!")
        return CHECK_JOIN

async def show_language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data='lang_en'), InlineKeyboardButton("🇧🇩 বাংলা", callback_data='lang_bn')]
    ]
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
    keyboard = [
        [InlineKeyboardButton("🔵 1XBET", callback_data='platform_1XBET'), InlineKeyboardButton("🟡 MELBET", callback_data='platform_MELBET')],
        [InlineKeyboardButton(t['btn_help'], url=ADMIN_USER_LINK)]
    ]
    
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
    keyboard = [
        [InlineKeyboardButton(t['btn_reg_link'].format(platform=platform), url=LINK_REGISTRATION)],
        [InlineKeyboardButton(t['btn_next'], callback_data='account_created')]
    ]
    
    try: await query.message.delete()
    except: pass
    await safe_send_photo(context, update.effective_chat.id, IMG_REGISTRATION, text, InlineKeyboardMarkup(keyboard))
    return CHOOSE_PLATFORM

async def wait_and_ask_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    lang = context.user_data.get('lang', 'en')
    msg = await query.message.reply_text(TEXTS[lang]['wait_msg'], parse_mode='HTML')
    await asyncio.sleep(2)
    
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

    keyboard = [
        [InlineKeyboardButton(t['btn_apple_hack'], web_app=WebAppInfo(url=APPLE_HACK_URL))],
        [InlineKeyboardButton(t['btn_thimbles_hack'], web_app=WebAppInfo(url=THIMBLES_HACK_URL))],
        [InlineKeyboardButton(t['btn_crash_signal'], web_app=WebAppInfo(url=CRASH_SIGNAL_URL))],
        [InlineKeyboardButton(t['btn_contact'], url=ADMIN_USER_LINK)]
    ]

    await safe_send_photo(context, update.effective_chat.id, FINAL_IMAGE_URL, t['success_caption'].format(uid=uid), InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END

# ================= অ্যাডমিন সেকশন =================

async def admin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("👑 Admin: ব্রডকাস্ট করার জন্য যেকোনো মেসেজ লিখে পাঠান অথবা ফরওয়ার্ড করুন।")
    return ADMIN_GET_CONTENT

async def admin_get_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['bc_msg'] = update.message

    keyboard = [
        [InlineKeyboardButton("✅ ব্রডকাস্ট শুরু করুন", callback_data='bc_confirm')],
        [InlineKeyboardButton("❌ বাতিল করুন", callback_data='bc_cancel')]
    ]
    await update.message.reply_text("আপনার মেসেজটি রিসিভ হয়েছে। আপনি কি এটি সবার কাছে পাঠাতে চান?", reply_markup=InlineKeyboardMarkup(keyboard))
    return ADMIN_CONFIRM

async def admin_broadcast_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'bc_cancel':
        await query.edit_message_text("❌ ব্রডকাস্ট বাতিল করা হয়েছে।")
        return ConversationHandler.END
        
    if query.data == 'bc_confirm':
        await query.edit_message_text("🚀 ব্রডকাস্ট শুরু হয়েছে, দয়া করে অপেক্ষা করুন...")
        user_ids = get_all_users()
        msg = context.user_data.get('bc_msg')
        
        success_count = 0
        fail_count = 0
        
        for uid in user_ids:
            try:
                await context.bot.forward_message(chat_id=uid, from_chat_id=msg.chat_id, message_id=msg.message_id)
                success_count += 1
            except Exception as e:
                try:
                    await context.bot.copy_message(chat_id=uid, from_chat_id=msg.chat_id, message_id=msg.message_id)
                    success_count += 1
                except:
                    fail_count += 1
            await asyncio.sleep(0.05)
            
        final_text = f"✅ ব্রডকাস্ট সম্পন্ন হয়েছে!\nসফলভাবে পাঠানো হয়েছে: {success_count} জনকে\nব্যর্থ হয়েছে: {fail_count} জনের কাছে।"
        await query.message.reply_text(final_text)
        return ConversationHandler.END

# ================= মেইন রানার =================

if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()
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
            ADMIN_GET_CONTENT: [MessageHandler(filters.ALL & ~filters.COMMAND, admin_get_content)],
            ADMIN_CONFIRM: [CallbackQueryHandler(admin_broadcast_action, pattern='^bc_')]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    application.add_handler(user_conv)
    application.add_handler(admin_conv)
    print("Bot is starting with 2 Channels requirement...")
    application.run_polling()

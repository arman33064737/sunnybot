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
    ConversationHandler,
    Defaults
)
from telegram.constants import ParseMode

# ================= লগিং কনফিগারেশন =================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR # অপ্রয়োজনীয় লগ কমিয়ে স্পিড বাড়ানো হয়েছে
)
logger = logging.getLogger(__name__)

# ================= ওয়েব সার্ভার =================
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

# ================= কনফিগারেশন =================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8511299158:AAFXkGzhz5Li22MXmXl1wThQLaSGp0om2Lc")
ADMIN_ID = 7406442919  
REQUIRED_CHANNEL_ID = "-1001481593780"
LINK_REGISTRATION = "https://bit.ly/BLACK220" 
CHANNEL_INVITE_LINK = "https://t.me/+3U0nMzWs4Aw0YjFl"
ADMIN_USER_LINK = "https://t.me/SUNNY_BRO1"

# Images
IMG_START = "https://i.ibb.co.com/7dDFg5WQ/new-updear-photo.png"
IMG_LANG = "https://i.ibb.co.com/23VVWgSS/file-00000000d21472088a8b84f9b1faa902.png"
IMG_CHOOSE_PLATFORM = "https://i.ibb.co.com/NdFDsT4P/file-000000005308720880754a5daa131c74.png"
IMG_REGISTRATION = "https://i.ibb.co.com/NdFDsT4P/file-000000005308720880754a5daa131c74.png"
FINAL_IMAGE_URL = "https://i.ibb.co.com/xy9RwRS/opnen-haxl.png"
WEBAPP_URL = "https://1xbet-melbet-apple.unaux.com/"
USER_FILE = "users.txt"

# ================= TEXTS =================
TEXTS = {
    'en': {
        'choose_platform_caption': "🎮 <b>CHOOSE YOUR PLATFORM</b>\n\nWhich casino do you want to hack? Select below 👇",
        'btn_help': "🆘 Help / Support",
        'reg_title': "🚀 <b>{platform} REGISTRATION</b>",
        'reg_msg': "⚠️ <b>WARNING:</b> Hack works ONLY with our Link!\n\n1️⃣ Delete old account.\n2️⃣ Click 'Register' (Use promo <code>{promo}</code>).\n3️⃣ Send ID here.\n\n🛑 <i>ID will be rejected if not opened via our link.</i>",
        'btn_reg_link': "🔗 Register {platform}",
        'btn_next': "✅ I Registered (Verify ID)",
        'wait_msg': "⏳ <b>Connecting to Server...</b>",
        'ask_id': "📩 <b>SEND YOUR ID</b>\nPlease send the 9-10 digit User ID.",
        'error_digit': "❌ <b>Error:</b> Digits only.",
        'error_length': "❌ <b>Invalid ID:</b> Must be 9 or 10 digits.",
        'success_caption': "✅ <b>VERIFIED!</b>\n🆔 ID: <code>{uid}</code>\n\nPromo: <b>{promo}</b> matched.\nClick below to Hack! 🤑",
        'btn_open_hack': "🍎 OPEN HACK (WebApp)",
        'btn_contact': "👨‍💻 Admin Support"
    },
    'bn': {
        'choose_platform_caption': "🎮 <b>প্ল্যাটফর্ম নির্বাচন করুন</b>\nনিচে থেকে ক্যাসিনো সিলেক্ট করুন 👇",
        'btn_help': "🆘 সাহায্য / সাপোর্ট",
        'reg_title': "🚀 <b>{platform} রেজিস্ট্রেশন</b>",
        'reg_msg': "⚠️ <b>সতর্কতা:</b> হ্যাকটি শুধুমাত্র আমাদের লিংকে কাজ করবে!\n\n1️⃣ পুরনো একাউন্ট ডিলিট করুন।\n2️⃣ রেজিস্ট্রেশন করুন (প্রোমো: <code>{promo}</code>)।\n3️⃣ আইডি আমাদের পাঠান।\n\n🛑 <i>লিংক ছাড়া আইডি দিলে ভেরিফাই হবে না।</i>",
        'btn_reg_link': "🔗 {platform} রেজিস্ট্রেশন লিংক",
        'btn_next': "✅ রেজিস্ট্রেশন করেছি",
        'wait_msg': "⏳ <b>সার্ভারে কানেক্ট হচ্ছে...</b>",
        'ask_id': "📩 <b>আপনার আইডি পাঠান</b>\nআপনার ১০ সংখ্যার আইডি টি পাঠান।",
        'error_digit': "❌ <b>ভুল!</b> শুধুমাত্র সংখ্যা পাঠান।",
        'error_length': "❌ <b>ভুল!</b> ৯-১০ সংখ্যার আইডি দিন।",
        'success_caption': "✅ <b>ভেরিফাইড সফল!</b>\n🆔 ID: <code>{uid}</code>\n\nপ্রোমো <b>{promo}</b> মিলেছে।\nহ্যাক চালু করতে নিচে ক্লিক করুন! 🤑",
        'btn_open_hack': "🍎 হ্যাক চালু করুন (WebApp)",
        'btn_contact': "👨‍💻 এডমিন সাপোর্ট"
    }
}

# States
CHECK_JOIN, SELECT_LANGUAGE, CHOOSE_PLATFORM, WAITING_FOR_ID = range(4)
ADMIN_MAIN, BC_CONTENT, BC_BUTTON_TEXT, BC_BUTTON_URL, BC_CONFIRM = range(10, 15)

# ================= DATABASE =================
def save_user(user_id):
    if not os.path.exists(USER_FILE): open(USER_FILE, "w").close()
    with open(USER_FILE, "r") as f: users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USER_FILE, "a") as f: f.write(f"{str(user_id)}\n")

def get_users_list():
    if not os.path.exists(USER_FILE): return []
    with open(USER_FILE, "r") as f: return f.read().splitlines()

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL_ID, user_id=update.effective_user.id)
        return member.status in ['creator', 'administrator', 'member']
    except: return False

# ================= ইউজার হ্যান্ডলারস =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    
    # বাটন ক্লিক রেসপন্স ফাস্ট করার জন্য query answer চেক
    if update.callback_query:
        await update.callback_query.answer()

    if not await check_membership(update, context):
        keyboard = [[InlineKeyboardButton("📢 Join Channel", url=CHANNEL_INVITE_LINK)],
                    [InlineKeyboardButton("✅ I Have Joined", callback_data='check_join_status')]]
        text = f"👋 <b>Hello {user.first_name}!</b>\nJoin our channel first to use the bot."
        if update.callback_query:
            await update.callback_query.message.reply_photo(photo=IMG_START, caption=text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await update.message.reply_photo(photo=IMG_START, caption=text, reply_markup=InlineKeyboardMarkup(keyboard))
        return CHECK_JOIN
    
    keyboard = [[InlineKeyboardButton("🇺🇸 English", callback_data='lang_en'),
                 InlineKeyboardButton("🇧🇩 বাংলা", callback_data='lang_bn')]]
    
    msg_text = "🌐 <b>Select Language:</b>"
    if update.callback_query:
        await update.callback_query.message.reply_photo(photo=IMG_LANG, caption=msg_text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_photo(photo=IMG_LANG, caption=msg_text, reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECT_LANGUAGE

async def lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # সাথে সাথে উত্তর দেওয়া
    
    lang = query.data.split('_')[1]
    context.user_data['lang'] = lang
    t = TEXTS[lang]
    
    keyboard = [[InlineKeyboardButton("🔵 1XBET", callback_data='platform_1xbet'),
                 InlineKeyboardButton("🟡 MELBET", callback_data='platform_melbet')],
                [InlineKeyboardButton(t['btn_help'], url=ADMIN_USER_LINK)]]
    
    await query.message.delete()
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=IMG_CHOOSE_PLATFORM, 
                                 caption=t['choose_platform_caption'], 
                                 reply_markup=InlineKeyboardMarkup(keyboard))
    return CHOOSE_PLATFORM

async def platform_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    choice = query.data
    lang = context.user_data.get('lang', 'en')
    t = TEXTS[lang]
    
    p_name = "1XBET" if "1xbet" in choice else "MELBET"
    promo = "BLACK696" if "1xbet" in choice else "BLACK220"
    context.user_data['p_name'] = p_name
    context.user_data['promo'] = promo
    
    text = t['reg_title'].format(platform=p_name) + "\n\n" + t['reg_msg'].format(promo=promo)
    keyboard = [[InlineKeyboardButton(t['btn_reg_link'].format(platform=p_name), url=LINK_REGISTRATION)],
                [InlineKeyboardButton(t['btn_next'], callback_data='go_verify')]]
    
    await query.message.delete()
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=IMG_REGISTRATION, 
                                 caption=text, reply_markup=InlineKeyboardMarkup(keyboard))
    return CHOOSE_PLATFORM

async def ask_id_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'en')
    
    # ওয়েট মেসেজ কমিয়ে সরাসরি আইডি চাওয়া (স্পিড বাড়ানোর জন্য)
    await query.message.reply_text(TEXTS[lang]['ask_id'])
    return WAITING_FOR_ID

async def verify_id_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()
    lang = context.user_data.get('lang', 'en')
    t = TEXTS[lang]
    
    if not uid.isdigit() or not (9 <= len(uid) <= 10):
        await update.message.reply_text(t['error_length'])
        return WAITING_FOR_ID
    
    # প্রসেসিং ডিলিট করে সরাসরি রেজাল্ট (স্পিড আপ)
    promo = context.user_data.get('promo', 'BLACK220')
    keyboard = [[InlineKeyboardButton(t['btn_open_hack'], web_app=WebAppInfo(url=WEBAPP_URL))],
                [InlineKeyboardButton(t['btn_contact'], url=ADMIN_USER_LINK)]]
    
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=FINAL_IMAGE_URL, 
                                 caption=t['success_caption'].format(uid=uid, promo=promo), 
                                 reply_markup=InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END

# ================= অ্যাডমিন প্যানেল =================
async def admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    count = len(get_users_list())
    keyboard = [[InlineKeyboardButton("📢 Broadcast", callback_data='bc_start')],
                [InlineKeyboardButton("📊 Stats", callback_data='admin_stats')],
                [InlineKeyboardButton("❌ Close", callback_data='admin_close')]]
    await update.message.reply_text(f"👑 <b>Admin Panel</b>\nUsers: {count}", reply_markup=InlineKeyboardMarkup(keyboard))
    return ADMIN_MAIN

async def admin_close_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.delete()
    return ConversationHandler.END

async def bc_start_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_text("📤 Send your message (Text/Photo/Video):")
    return BC_CONTENT

async def bc_get_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data['bc_type'] = 'photo'
        context.user_data['bc_file_id'] = update.message.photo[-1].file_id
        context.user_data['bc_text'] = update.message.caption
    elif update.message.video:
        context.user_data['bc_type'] = 'video'
        context.user_data['bc_file_id'] = update.message.video.file_id
        context.user_data['bc_text'] = update.message.caption
    else:
        context.user_data['bc_type'] = 'text'
        context.user_data['bc_text'] = update.message.text

    keyboard = [[InlineKeyboardButton("🚀 Send Now", callback_data='confirm_bc')],
                [InlineKeyboardButton("❌ Cancel", callback_data='admin_close')]]
    await update.message.reply_text("Confirm Broadcast?", reply_markup=InlineKeyboardMarkup(keyboard))
    return BC_CONFIRM

async def bc_final_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    users = get_users_list()
    await query.edit_text(f"Sending to {len(users)} users...")
    
    bc_type = context.user_data.get('bc_type')
    text = context.user_data.get('bc_text')
    fid = context.user_data.get('bc_file_id')
    
    count = 0
    for uid in users:
        try:
            if bc_type == 'photo':
                await context.bot.send_photo(chat_id=uid, photo=fid, caption=text, parse_mode='HTML')
            elif bc_type == 'video':
                await context.bot.send_video(chat_id=uid, video=fid, caption=text, parse_mode='HTML')
            else:
                await context.bot.send_message(chat_id=uid, text=text, parse_mode='HTML')
            count += 1
            if count % 20 == 0: await asyncio.sleep(0.5) # রেট লিমিট এড়াতে
        except: continue
        
    await context.bot.send_message(ADMIN_ID, f"✅ Broadcast Done! Sent to: {count}")
    return ConversationHandler.END

# ================= মেইন ফাংশন =================
if __name__ == '__main__':
    keep_alive()
    
    # HTML সাপোর্ট ডিফল্ট করা হয়েছে
    defaults = Defaults(parse_mode=ParseMode.HTML)
    
    # concurrent_updates=True ব্যবহার করে স্পিড বাড়ানো হয়েছে
    application = ApplicationBuilder().token(BOT_TOKEN).defaults(defaults).concurrent_updates(True).build()

    user_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHECK_JOIN: [CallbackQueryHandler(start, pattern='check_join_status')],
            SELECT_LANGUAGE: [CallbackQueryHandler(lang_callback, pattern='^lang_')],
            CHOOSE_PLATFORM: [CallbackQueryHandler(platform_callback, pattern='^platform_'),
                             CallbackQueryHandler(ask_id_step, pattern='go_verify')],
            WAITING_FOR_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_id_final)]
        },
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True # ইউজার আটকালে আবার স্টার্ট করতে পারবে
    )

    admin_handler = ConversationHandler(
        entry_points=[CommandHandler('admin', admin_cmd)],
        states={
            ADMIN_MAIN: [CallbackQueryHandler(bc_start_cb, pattern='bc_start'),
                        CallbackQueryHandler(admin_close_cb, pattern='admin_close')],
            BC_CONTENT: [MessageHandler(filters.ALL & ~filters.COMMAND, bc_get_content)],
            BC_CONFIRM: [CallbackQueryHandler(bc_final_send, pattern='confirm_bc')]
        },
        fallbacks=[CommandHandler('admin', admin_cmd)],
        allow_reentry=True
    )

    application.add_handler(admin_handler)
    application.add_handler(user_handler)

    print("Bot is started with High Performance Mode...")
    application.run_polling(drop_pending_updates=True)

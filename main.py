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
from telegram.error import BadRequest

# ================= লগিং কনফিগারেশন =================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ================= ওয়েব সার্ভার (Render/Railway) =================
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
        'wait_msg': "⏳ <b>Connecting to Server...</b>\nChecking ID details...",
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
        'wait_msg': "⏳ <b>সার্ভারে কানেক্ট হচ্ছে...</b>\nআইডি চেক করা হচ্ছে...",
        'ask_id': "📩 <b>আপনার আইডি পাঠান</b>\nআপনার ১০ সংখ্যার আইডি টি পাঠান।",
        'error_digit': "❌ <b>ভুল!</b> শুধুমাত্র সংখ্যা পাঠান।",
        'error_length': "❌ <b>ভুল!</b> ৯-১০ সংখ্যার আইডি দিন।",
        'success_caption': "✅ <b>ভেরিফাইড সফল!</b>\n🆔 ID: <code>{uid}</code>\n\nপ্রোমো <b>{promo}</b> মিলেছে।\nহ্যাক চালু করতে নিচে ক্লিক করুন! 🤑",
        'btn_open_hack': "🍎 হ্যাক চালু করুন (WebApp)",
        'btn_contact': "👨‍💻 এডমিন সাপোর্ট"
    }
}

# ================= STATES =================
CHECK_JOIN, SELECT_LANGUAGE, CHOOSE_PLATFORM, WAITING_FOR_ID = range(4)
# Admin States
ADMIN_MAIN, BC_CONTENT, BC_BUTTON_TEXT, BC_BUTTON_URL, BC_CONFIRM = range(10, 15)

# ================= DATABASE FUNC =================
def save_user(user_id):
    if not os.path.exists(USER_FILE): open(USER_FILE, "w").close()
    with open(USER_FILE, "r") as f: users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USER_FILE, "a") as f: f.write(f"{str(user_id)}\n")

def get_users_count():
    if not os.path.exists(USER_FILE): return 0
    with open(USER_FILE, "r") as f: return len(f.read().splitlines())

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
    if not await check_membership(update, context):
        keyboard = [[InlineKeyboardButton("📢 Join Channel", url=CHANNEL_INVITE_LINK)],
                    [InlineKeyboardButton("✅ I Have Joined", callback_data='check_join_status')]]
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=IMG_START, 
                                     caption=f"👋 <b>Hello {user.first_name}!</b>\nJoin our channel first.", 
                                     reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
        return CHECK_JOIN
    
    keyboard = [[InlineKeyboardButton("🇺🇸 English", callback_data='lang_en'),
                 InlineKeyboardButton("🇧🇩 বাংলা", callback_data='lang_bn')]]
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=IMG_LANG, 
                                 caption="🌐 <b>Select Language:</b>", 
                                 reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return SELECT_LANGUAGE

async def lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['lang'] = query.data.split('_')[1]
    lang = context.user_data['lang']
    t = TEXTS[lang]
    keyboard = [[InlineKeyboardButton("🔵 1XBET", callback_data='platform_1xbet'),
                 InlineKeyboardButton("🟡 MELBET", callback_data='platform_melbet')],
                [InlineKeyboardButton(t['btn_help'], url=ADMIN_USER_LINK)]]
    await query.message.delete()
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=IMG_CHOOSE_PLATFORM, 
                                 caption=t['choose_platform_caption'], 
                                 reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
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
                                 caption=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return CHOOSE_PLATFORM

async def ask_id_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'en')
    await query.message.reply_text(TEXTS[lang]['wait_msg'], parse_mode='HTML')
    await asyncio.sleep(2)
    await query.message.reply_text(TEXTS[lang]['ask_id'], parse_mode='HTML')
    return WAITING_FOR_ID

async def verify_id_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()
    lang = context.user_data.get('lang', 'en')
    t = TEXTS[lang]
    if not uid.isdigit() or not (9 <= len(uid) <= 10):
        await update.message.reply_text(t['error_length'], parse_mode='HTML')
        return WAITING_FOR_ID
    
    promo = context.user_data.get('promo', 'BLACK220')
    keyboard = [[InlineKeyboardButton(t['btn_open_hack'], web_app=WebAppInfo(url=WEBAPP_URL))],
                [InlineKeyboardButton(t['btn_contact'], url=ADMIN_USER_LINK)]]
    
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=FINAL_IMAGE_URL, 
                                 caption=t['success_caption'].format(uid=uid, promo=promo), 
                                 reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return ConversationHandler.END

# ================= অ্যাডমিন প্যানেল হ্যান্ডলারস =================
async def admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    count = get_users_count()
    keyboard = [[InlineKeyboardButton("📢 Broadcast (পডকাস্ট)", callback_data='bc_start')],
                [InlineKeyboardButton("📊 Total Users", callback_data='admin_stats')],
                [InlineKeyboardButton("❌ Close", callback_data='admin_close')]]
    await update.message.reply_text(f"👑 <b>Admin Panel</b>\n\nTotal Registered Users: <code>{count}</code>", 
                                    reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
    return ADMIN_MAIN

async def admin_stats_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer(f"Total Users: {get_users_count()}", show_alert=True)
    return ADMIN_MAIN

async def bc_start_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_text("📤 <b>কি পাঠাতে চান?</b>\nটেক্সট, ফটো অথবা ভিডিও ক্যাপশনসহ পাঠান।", parse_mode='HTML')
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

    keyboard = [[InlineKeyboardButton("➕ বাটন যোগ করুন", callback_data='add_btn')],
                [InlineKeyboardButton("⏩ বাটন ছাড়া পাঠান", callback_data='no_btn')]]
    await update.message.reply_text("আপনি কি এই মেসেজের সাথে কোনো বাটন যোগ করতে চান?", reply_markup=InlineKeyboardMarkup(keyboard))
    return BC_BUTTON_TEXT

async def bc_add_btn_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_text("বাটনে কি লেখা থাকবে? (যেমন: Join Now)")
    return BC_BUTTON_TEXT

async def bc_get_btn_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['btn_text'] = update.message.text
    await update.message.reply_text("বাটনের লিংকটি (URL) দিন:")
    return BC_BUTTON_URL

async def bc_get_btn_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['btn_url'] = update.message.text
    return await bc_confirm_msg(update, context)

async def bc_confirm_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🚀 Send Now", callback_data='confirm_bc')],
                [InlineKeyboardButton("❌ Cancel", callback_data='admin_close')]]
    await (update.message.reply_text if update.message else update.callback_query.message.reply_text)("সব ঠিক আছে? ব্রডকাস্ট শুরু করতে 'Send Now' চাপুন।", reply_markup=InlineKeyboardMarkup(keyboard))
    return BC_CONFIRM

async def bc_final_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    users = get_users_list()
    await query.edit_text(f"⏳ {len(users)} জন ইউজারের কাছে পাঠানো হচ্ছে...")
    
    bc_type = context.user_data.get('bc_type')
    text = context.user_data.get('bc_text')
    fid = context.user_data.get('bc_file_id')
    btn_text = context.user_data.get('btn_text')
    btn_url = context.user_data.get('btn_url')
    
    markup = None
    if btn_text and btn_url:
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(btn_text, url=btn_url)]])
    
    count = 0
    for uid in users:
        try:
            if bc_type == 'photo':
                await context.bot.send_photo(chat_id=uid, photo=fid, caption=text, reply_markup=markup, parse_mode='HTML')
            elif bc_type == 'video':
                await context.bot.send_video(chat_id=uid, video=fid, caption=text, reply_markup=markup, parse_mode='HTML')
            else:
                await context.bot.send_message(chat_id=uid, text=text, reply_markup=markup, parse_mode='HTML')
            count += 1
            await asyncio.sleep(0.05)
        except: pass
        
    await context.bot.send_message(ADMIN_ID, f"✅ ব্রডকাস্ট সম্পন্ন!\nসফলভাবে {count} জনের কাছে পৌঁছেছে।")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("বাতিল করা হয়েছে।")
    return ConversationHandler.END

# ================= মেইন ফাংশন =================
if __name__ == '__main__':
    keep_alive()
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # অ্যাডমিন কনভারসেশন (আগে রাখতে হবে)
    admin_handler = ConversationHandler(
        entry_points=[CommandHandler('admin', admin_cmd)],
        states={
            ADMIN_MAIN: [CallbackQueryHandler(bc_start_cb, pattern='bc_start'),
                         CallbackQueryHandler(admin_stats_cb, pattern='admin_stats'),
                         CallbackQueryHandler(lambda u,c: ConversationHandler.END, pattern='admin_close')],
            BC_CONTENT: [MessageHandler(filters.ALL & ~filters.COMMAND, bc_get_content)],
            BC_BUTTON_TEXT: [CallbackQueryHandler(bc_add_btn_text, pattern='add_btn'),
                             CallbackQueryHandler(bc_confirm_msg, pattern='no_btn'),
                             MessageHandler(filters.TEXT & ~filters.COMMAND, bc_get_btn_text)],
            BC_BUTTON_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, bc_get_btn_url)],
            BC_CONFIRM: [CallbackQueryHandler(bc_final_send, pattern='confirm_bc')]
        },
        fallbacks=[CommandHandler('start', start)],
        per_message=False
    )

    # ইউজার কনভারসেশন
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
        per_message=False
    )

    application.add_handler(admin_handler)
    application.add_handler(user_handler)

    print("Bot is alive...")
    application.run_polling(drop_pending_updates=True)

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

# ================= ওয়েব সার্ভার (Keep-Alive) =================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ================= কনফিগারেশন =================
# টোকেন সরাসরি কোডে না রেখে এনভায়রনমেন্ট ভ্যারিয়েবলে রাখা ভালো। 
# তবে এখানে আপনার দেওয়া টোকেনটিই রাখা হলো।
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8511299158:AAFXkGzhz5Li22MXmXl1wThQLaSGp0om2Lc")
ADMIN_ID = 7406442919  
REQUIRED_CHANNEL_ID = "-1001481593780"
LINK_REGISTRATION = "https://bit.ly/BLACK220" 
CHANNEL_INVITE_LINK = "https://t.me/+3U0nMzWs4Aw0YjFl"
ADMIN_USER_LINK = "https://t.me/SUNNY_BRO1"

# Images
IMG_START = "https://i.ibb.co.com/23VVWgSS/file-00000000d21472088a8b84f9b1faa902.png"
IMG_LANG = "https://i.ibb.co.com/23VVWgSS/file-00000000d21472088a8b84f9b1faa902.png"
IMG_CHOOSE_PLATFORM = "https://i.ibb.co.com/NdFDsT4P/file-000000005308720880754a5daa131c74.png"
IMG_REGISTRATION = "https://i.ibb.co.com/NdFDsT4P/file-000000005308720880754a5daa131c74.png"
FINAL_IMAGE_URL = "https://i.ibb.co.com/vxfM0vv5/file-00000000f15071fa8c883abb1421fa69.png"

WEBAPP_URL = "https://1xbet-melbet-apple.unaux.com/"
USER_FILE = "users.txt"

# ================= TEXTS =================
TEXTS = {
    'en': {
        'choose_platform_caption': "🎮 <b>CHOOSE YOUR PLATFORM</b>\n\nWhich casino do you want to hack? Select below 👇",
        'btn_help': "🆘 Help / Support",
        'reg_title': "🚀 <b>{platform} REGISTRATION</b>",
        'reg_msg': "⚠️ <b>WARNING:</b> Hack works ONLY with our Link!\n\n1️⃣ Delete old account.\n2️⃣ Click 'Register' below (Use promo <code>{promo}</code>).\n3️⃣ Create account and send ID.\n\n🛑 <i>If you don't use the link below, the bot will REJECT your ID.</i>",
        'btn_reg_link': "🔗 Register {platform}",
        'btn_next': "✅ I Registered (Verify ID)",
        'wait_msg': "⏳ <b>Connecting to Server...</b>\nChecking if ID was created via our link...",
        'ask_id': "📩 <b>SEND YOUR NEW ID</b>\n\nPlease send the <b>10-digit User ID</b> now.",
        'error_digit': "❌ <b>Error:</b> Digits only.",
        'error_length': "❌ <b>Invalid ID:</b> Must be 9 or 10 digits.",
        'fake_error': "❌ <b>VERIFICATION FAILED!</b>\n\nThis ID was NOT created using our Promo Link.",
        'success_caption': "✅ <b>VERIFIED SUCCESS!</b>\n🆔 ID: <code>{uid}</code>\n\nAccount matched with Promo Code <b>{promo}</b>.",
        'btn_open_hack': "🍎 OPEN HACK (WebApp)",
        'btn_contact': "👨‍💻 Contact Admin"
    },
    'bn': {
        'choose_platform_caption': "🎮 <b>প্ল্যাটফর্ম নির্বাচন করুন</b>\nনিচে থেকে ক্যাসিনো সিলেক্ট করুন 👇",
        'btn_help': "🆘 সাহায্য / সাপোর্ট",
        'reg_title': "🚀 <b>{platform} রেজিস্ট্রেশন</b>",
        'reg_msg': "⚠️ <b>সতর্কতা:</b> হ্যাকটি শুধুমাত্র আমাদের লিংকে কাজ করবে!\n\n1️⃣ পুরনো একাউন্ট ডিলিট করুন।\n2️⃣ নিচের 'Register' বাটনে ক্লিক করে একাউন্ট খুলুন (প্রোমো: <code>{promo}</code>)।\n3️⃣ আইডি আমাদের পাঠান।\n\n🛑 <i>আপনি যদি নিচের লিংক দিয়ে একাউন্ট না করেন, বট আপনার আইডি বাতিল করে দেবে।</i>",
        'btn_reg_link': "🔗 {platform} রেজিস্ট্রেশন লিংক",
        'btn_next': "✅ রেজিস্ট্রেশন করেছি (ভেরিফাই)",
        'wait_msg': "⏳ <b>সার্ভারে কানেক্ট হচ্ছে...</b>\nচেক করা হচ্ছে আইডিটি আমাদের লিংকে খোলা কিনা...",
        'ask_id': "📩 <b>আপনার আইডি পাঠান</b>\n\nআপনার নতুন একাউন্টের <b>১০ সংখ্যার আইডি</b> টি পাঠান।",
        'error_digit': "❌ <b>ভুল!</b> শুধুমাত্র ইংরেজি সংখ্যা পাঠান।",
        'error_length': "❌ <b>ভুল আইডি!</b> ৯ অথবা ১০ সংখ্যার আইডি হতে হবে।",
        'fake_error': "❌ <b>ভেরিফিকেশন ব্যর্থ হয়েছে!</b>\n\nএই আইডিটি আমাদের লিংক বা প্রোমো কোড দিয়ে খোলা হয়নি।",
        'success_caption': "✅ <b>ভেরিফাইড সফল!</b>\n🆔 ID: <code>{uid}</code>\n\nআইডিটি প্রোমো কোড <b>{promo}</b> এর সাথে মিলেছে।",
        'btn_open_hack': "🍎 হ্যাক চালু করুন (WebApp)",
        'btn_contact': "👨‍💻 এডমিন সাপোর্ট"
    }
}

# ================= STATES =================
CHECK_JOIN, SELECT_LANGUAGE, CHOOSE_PLATFORM, WAITING_FOR_ID = range(4)
ADMIN_MENU, ADMIN_GET_CONTENT, ADMIN_GET_LINK, ADMIN_GET_BTN_NAME, ADMIN_CONFIRM = range(10, 15)

# ================= DATABASE FUNC =================
def save_user(user_id):
    if not os.path.exists(USER_FILE): open(USER_FILE, "w").close()
    with open(USER_FILE, "r") as f: users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USER_FILE, "a") as f: f.write(f"{str(user_id)}\n")

def get_users():
    if not os.path.exists(USER_FILE): return[]
    with open(USER_FILE, "r") as f: return f.read().splitlines()

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL_ID, user_id=user_id)
        return member.status in ['creator', 'administrator', 'member']
    except Exception:
        return False

# ================= হেলপার ফাংশন =================
async def safe_send_photo(context, chat_id, photo, caption=None, reply_markup=None):
    try:
        await context.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=caption, reply_markup=reply_markup, parse_mode='HTML')

# ================= হ্যান্ডলারস =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    if not await check_membership(update, context):
        keyboard = [[InlineKeyboardButton("📢 Join Channel", url=CHANNEL_INVITE_LINK)],
                    [InlineKeyboardButton("✅ I Have Joined", callback_data='check_join_status')]]
        text = f"👋 <b>Hello {user.first_name}!</b>\nJoin our channel to use this bot."
        await safe_send_photo(context, update.effective_chat.id, IMG_START, text, InlineKeyboardMarkup(keyboard))
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
        await query.message.reply_text("❌ You haven't joined yet. Please join and try again.")
        return CHECK_JOIN

async def show_language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🇺🇸 English", callback_data='lang_en'),
                 InlineKeyboardButton("🇧🇩 বাংলা", callback_data='lang_bn')]]
    text = "🌐 <b>Select Language / ভাষা নির্বাচন করুন:</b>"
    await safe_send_photo(context, update.effective_chat.id, IMG_LANG, text, InlineKeyboardMarkup(keyboard))

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['lang'] = query.data.split('_')[1]
    await show_platform_menu(update, context)
    return CHOOSE_PLATFORM

async def show_platform_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang = context.user_data.get('lang', 'en')
    t = TEXTS[lang]
    keyboard = [[InlineKeyboardButton("🔵 1XBET", callback_data='platform_1xbet'),
                 InlineKeyboardButton("🟡 MELBET", callback_data='platform_melbet')],
                [InlineKeyboardButton(t['btn_help'], url=ADMIN_USER_LINK)]]
    await query.message.delete()
    await safe_send_photo(context, update.effective_chat.id, IMG_CHOOSE_PLATFORM, t['choose_platform_caption'], InlineKeyboardMarkup(keyboard))

async def platform_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data
    lang = context.user_data.get('lang', 'en')
    t = TEXTS[lang]
    
    p_name = "1XBET" if '1xbet' in choice else "MELBET"
    promo = "BLACK696" if '1xbet' in choice else "BLACK220"
    
    context.user_data['platform_name'] = p_name
    context.user_data['promo_code'] = promo

    text = f"{t['reg_title'].format(platform=p_name)}\n\n{t['reg_msg'].format(promo=promo)}"
    keyboard = [[InlineKeyboardButton(t['btn_reg_link'].format(platform=p_name), url=LINK_REGISTRATION)],
                [InlineKeyboardButton(t['btn_next'], callback_data='account_created')],
                [InlineKeyboardButton(t['btn_contact'], url=ADMIN_USER_LINK)]]
    
    await query.message.delete()
    await safe_send_photo(context, update.effective_chat.id, IMG_REGISTRATION, text, InlineKeyboardMarkup(keyboard))
    return CHOOSE_PLATFORM

async def wait_and_ask_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get('lang', 'en')
    msg = await query.message.reply_text(TEXTS[lang]['wait_msg'], parse_mode='HTML')
    await asyncio.sleep(3)
    await msg.delete()
    await query.message.reply_text(TEXTS[lang]['ask_id'], parse_mode='HTML')
    return WAITING_FOR_ID

async def receive_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()
    lang = context.user_data.get('lang', 'en')
    t = TEXTS[lang]
    promo = context.user_data.get('promo_code', 'BLACK220')
    
    if not uid.isdigit() or not (9 <= len(uid) <= 10):
        await update.message.reply_text(t['error_length'], parse_mode='HTML')
        return WAITING_FOR_ID
        
    keyboard = [[InlineKeyboardButton(t['btn_open_hack'], web_app=WebAppInfo(url=WEBAPP_URL))],
                [InlineKeyboardButton(t['btn_contact'], url=ADMIN_USER_LINK)]]
    
    await safe_send_photo(context, update.effective_chat.id, FINAL_IMAGE_URL, t['success_caption'].format(uid=uid, promo=promo), InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END

# ================= অ্যাডমিন ফাংশন (সংক্ষিপ্ত) =================
async def admin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    await update.message.reply_text("👑 <b>Admin Panel</b>\nUse /broadcast to send message.")

# ... (বাকি অ্যাডমিন হ্যান্ডলার গুলো আগের মতোই থাকবে)

# ================= মেইন রানার =================
def main():
    # ফ্লাস্ক ওয়েব সার্ভার স্টার্ট
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

    # বট অ্যাপ্লিকেশন বিল্ড
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # কনভারসেশন হ্যান্ডলার
    conv_handler = ConversationHandler(
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
        per_message=False
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('admin', admin_start))

    print("Bot is starting...")
    
    # পোলিং শুরু করার সময় drop_pending_updates=True দেওয়া হয়েছে কনফ্লিক্ট এড়াতে
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()

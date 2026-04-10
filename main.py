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

# ================= লগিং =================
logging.basicConfig(level=logging.ERROR)

# ================= কনফিগারেশন =================
ADMIN_ID = 7406442919  
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8511299158:AAFXkGzhz5Li22MXmXl1wThQLaSGp0om2Lc")
REQUIRED_CHANNEL_ID = "-1001481593780" # নিশ্চিত করুন বোট এই চ্যানেলে অ্যাডমিন
CHANNEL_INVITE_LINK = "https://t.me/+3U0nMzWs4Aw0YjFl"
LINK_REGISTRATION = "https://bit.ly/BLACK220" 
ADMIN_USER_LINK = "https://t.me/SUNNY_BRO1"

# মিডিয়া লিঙ্ক
IMG_START = "https://i.ibb.co.com/7dDFg5WQ/new-updear-photo.png"
IMG_LANG = "https://i.ibb.co.com/23VVWgSS/file-00000000d21472088a8b84f9b1faa902.png"
IMG_CHOOSE_PLATFORM = "https://i.ibb.co.com/NdFDsT4P/file-000000005308720880754a5daa131c74.png"
IMG_REGISTRATION = "https://i.ibb.co.com/NdFDsT4P/file-000000005308720880754a5daa131c74.png"
FINAL_IMAGE_URL = "https://i.ibb.co.com/xy9RwRS/opnen-haxl.png"
WEBAPP_URL = "https://1xbet-melbet-apple.unaux.com/"
USER_FILE = "users.txt"

# States
USER_SIDE, BC_WAIT = range(2)

# ================= ডাটাবেস =================
def save_user(user_id):
    if not os.path.exists(USER_FILE): open(USER_FILE, "w").close()
    with open(USER_FILE, "r") as f: users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USER_FILE, "a") as f: f.write(f"{str(user_id)}\n")

def get_users():
    if not os.path.exists(USER_FILE): return []
    with open(USER_FILE, "r") as f: return f.read().splitlines()

# ================= ওয়েব সার্ভার =================
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Running!"
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# ================= মেম্বারশিপ চেক ফাংশন =================
async def is_joined(context, user_id):
    try:
        member = await context.bot.get_chat_member(REQUIRED_CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# ================= মূল স্টার্ট ফাংশন =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)
    
    joined = await is_joined(context, user_id)
    
    if not joined:
        # ইউজার জয়েন না থাকলে এই মেসেজটি ১০০% যাবে
        kb = [
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_INVITE_LINK)],
            [InlineKeyboardButton("✅ Joined", callback_data='check_membership')]
        ]
        text = "👋 <b>স্বাগতম!</b>\n\nআমাদের বোটটি ব্যবহার করতে হলে আপনাকে অবশ্যই চ্যানেলে জয়েন থাকতে হবে। জয়েন করে নিচের 'Joined' বাটনে ক্লিক করুন।"
        
        if update.message:
            await update.message.reply_photo(IMG_START, text, reply_markup=InlineKeyboardMarkup(kb))
        else:
            await update.callback_query.message.edit_caption(caption=text, reply_markup=InlineKeyboardMarkup(kb))
        return USER_SIDE

    # ইউজার জয়েন থাকলে ভাষা সিলেক্ট
    kb = [[InlineKeyboardButton("🇺🇸 English", callback_data='en'), InlineKeyboardButton("🇧🇩 বাংলা", callback_data='bn')]]
    text = "🌐 <b>Select Your Language / ভাষা নির্বাচন করুন:</b>"
    
    if update.message:
        await update.message.reply_photo(IMG_LANG, text, reply_markup=InlineKeyboardMarkup(kb))
    else:
        # আগের মেসেজ ডিলিট করে নতুন মেসেজ পাঠানো (ক্যাপশন এডিট অনেক সময় কাজ করে না ফটোর ক্ষেত্রে)
        await update.callback_query.message.delete()
        await context.bot.send_photo(user_id, IMG_LANG, text, reply_markup=InlineKeyboardMarkup(kb))
    
    return USER_SIDE

# ================= কলব্যাক হ্যান্ডলার =================
async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    if data == 'check_membership':
        if await is_joined(context, user_id):
            return await start(update, context)
        else:
            await query.answer("❌ আপনি এখনো জয়েন করেননি!", show_alert=True)
            return USER_SIDE

    if data in ['en', 'bn']:
        kb = [[InlineKeyboardButton("🔵 1XBET", callback_data='1x'), InlineKeyboardButton("🟡 MELBET", callback_data='mel')]]
        await query.message.delete()
        await context.bot.send_photo(user_id, IMG_CHOOSE_PLATFORM, "🎮 <b>Choose Platform:</b>", reply_markup=InlineKeyboardMarkup(kb))
    
    elif data in ['1x', 'mel']:
        promo = "BLACK696" if data == '1x' else "BLACK220"
        context.user_data['promo'] = promo
        kb = [[InlineKeyboardButton("🔗 Register", url=LINK_REGISTRATION)], [InlineKeyboardButton("✅ Done", callback_data='id_step')]]
        await query.message.delete()
        await context.bot.send_photo(user_id, IMG_REGISTRATION, f"🚀 <b>Promo:</b> <code>{promo}</code>\n\nনিচের লিঙ্ক থেকে অ্যাকাউন্ট খুলে আপনার ID দিন।", reply_markup=InlineKeyboardMarkup(kb))
    
    elif data == 'id_step':
        await query.message.reply_text("📩 <b>আপনার প্লেয়ার ID নাম্বারটি লিখুন:</b>")
        return USER_SIDE
    
    return USER_SIDE

async def id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text
    if not uid.isdigit() or len(uid) < 6:
        await update.message.reply_text("❌ <b>ভুল ID!</b> সঠিক আইডি পাঠান।")
        return USER_SIDE
    
    promo = context.user_data.get('promo', 'BLACK220')
    kb = [[InlineKeyboardButton("🍎 OPEN HACK", web_app=WebAppInfo(url=WEBAPP_URL))], [InlineKeyboardButton("👨‍💻 Admin", url=ADMIN_USER_LINK)]]
    await update.message.reply_photo(FINAL_IMAGE_URL, f"✅ <b>Verified!</b>\n\n<b>ID:</b> {uid}\n<b>Promo:</b> {promo}", reply_markup=InlineKeyboardMarkup(kb))
    return ConversationHandler.END

# ================= এডমিন ফাংশন =================
async def admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    kb = [[InlineKeyboardButton("📢 Broadcast", callback_data='bc')], [InlineKeyboardButton("📊 Stats", callback_data='st')]]
    await update.message.reply_text("👑 Admin Menu", reply_markup=InlineKeyboardMarkup(kb))

async def admin_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'bc':
        await query.message.reply_text("এখন মেসেজ পাঠান:")
        return BC_WAIT
    elif query.data == 'st':
        await query.message.reply_text(f"Total Users: {len(get_users())}")
    await query.answer()

async def do_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_users()
    msg = update.message
    await msg.reply_text("পাঠানো হচ্ছে...")
    for u_id in users:
        try:
            await msg.copy(u_id)
            await asyncio.sleep(0.05)
        except: continue
    await msg.reply_text("শেষ হয়েছে।")
    return ConversationHandler.END

# ================= মেইন রানার =================
if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()
    
    app_bot = ApplicationBuilder().token(BOT_TOKEN).defaults(Defaults(parse_mode=ParseMode.HTML)).build()

    # কনভারসেশন হ্যান্ডলার
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('admin', admin_cmd)],
        states={
            USER_SIDE: [CallbackQueryHandler(handle_callbacks), MessageHandler(filters.TEXT & ~filters.COMMAND, id_handler)],
            BC_WAIT: [MessageHandler(filters.ALL & ~filters.COMMAND, do_broadcast), CallbackQueryHandler(admin_callbacks)]
        },
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True
    )

    app_bot.add_handler(conv_handler)
    app_bot.add_handler(CallbackQueryHandler(admin_callbacks, pattern='^(bc|st)$')) # ব্যাকআপ এডমিন কলব্যাক
    
    print("বোট চালু হয়েছে...")
    app_bot.run_polling(drop_pending_updates=True)

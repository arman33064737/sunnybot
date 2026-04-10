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
REQUIRED_CHANNEL_ID = "-1001481593780"
LINK_REGISTRATION = "https://bit.ly/BLACK220" 
CHANNEL_INVITE_LINK = "https://t.me/+3U0nMzWs4Aw0YjFl"
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
USER_SIDE, ADMIN_SIDE, BC_WAIT = range(3)

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
def home(): return "Running!"
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# ================= এডমিন লজিক =================
async def admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    
    kb = [
        [InlineKeyboardButton("📢 Broadcast", callback_data='go_bc')],
        [InlineKeyboardButton("📊 Total Users", callback_data='stats')],
        [InlineKeyboardButton("❌ Close", callback_data='close')]
    ]
    await update.message.reply_text(f"👑 <b>Admin Panel</b>\nUsers: {len(get_users())}", reply_markup=InlineKeyboardMarkup(kb))
    return ADMIN_SIDE

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'go_bc':
        await query.edit_message_text("📤 <b>Broadcast Mode:</b>\nএখন মেসেজ পাঠান।")
        return BC_WAIT
    elif query.data == 'stats':
        await query.message.reply_text(f"Total Users: {len(get_users())}")
    elif query.data == 'close':
        await query.message.delete()
        return ConversationHandler.END
    return ADMIN_SIDE

async def start_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = get_users()
    msg = update.message
    await msg.reply_text(f"🚀 {len(users)} জনের কাছে পাঠানো হচ্ছে...")
    count = 0
    for u_id in users:
        try:
            if msg.photo: await context.bot.send_photo(u_id, msg.photo[-1].file_id, caption=msg.caption)
            elif msg.video: await context.bot.send_video(u_id, msg.video.file_id, caption=msg.caption)
            else: await context.bot.send_message(u_id, msg.text)
            count += 1
            await asyncio.sleep(0.05)
        except: continue
    await msg.reply_text(f"✅ সফলভাবে {count} জনের কাছে পাঠানো হয়েছে।")
    return ConversationHandler.END

# ================= ইউজার লজিক (FIXED) =================
async def check_membership(bot, user_id):
    try:
        member = await bot.get_chat_member(REQUIRED_CHANNEL_ID, user_id)
        return member.status in ['creator', 'administrator', 'member']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    
    # মেম্বারশিপ চেক
    is_member = await check_membership(context.bot, user.id)

    if not is_member:
        kb = [
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_INVITE_LINK)],
            [InlineKeyboardButton("✅ Joined", callback_data='check_join')]
        ]
        text = "👋 <b>You must join our channel to use this bot!</b>\n\nনিচের চ্যানেলে জয়েন করে 'Joined' বাটনে ক্লিক করুন।"
        
        if update.callback_query:
            await update.callback_query.message.delete()
            await context.bot.send_photo(update.effective_chat.id, IMG_START, text, reply_markup=InlineKeyboardMarkup(kb))
        else:
            await update.message.reply_photo(IMG_START, text, reply_markup=InlineKeyboardMarkup(kb))
        return USER_SIDE

    # যদি জয়েন থাকে তবে ভাষা পছন্দ করতে বলবে
    kb = [[InlineKeyboardButton("🇺🇸 English", callback_data='en'), InlineKeyboardButton("🇧🇩 বাংলা", callback_data='bn')]]
    if update.callback_query:
        await update.callback_query.message.delete()
        await context.bot.send_photo(update.effective_chat.id, IMG_LANG, "🌐 <b>Select Language:</b>", reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_photo(IMG_LANG, "🌐 <b>Select Language:</b>", reply_markup=InlineKeyboardMarkup(kb))
    return USER_SIDE

async def user_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    # জয়েন বাটন চেক করা
    if data == 'check_join':
        is_member = await check_membership(context.bot, user_id)
        if is_member:
            # জয়েন থাকলে ভাষা সিলেকশনে পাঠাবে
            kb = [[InlineKeyboardButton("🇺🇸 English", callback_data='en'), InlineKeyboardButton("🇧🇩 বাংলা", callback_data='bn')]]
            await query.message.delete()
            await context.bot.send_photo(update.effective_chat.id, IMG_LANG, "🌐 <b>Select Language:</b>", reply_markup=InlineKeyboardMarkup(kb))
        else:
            await query.answer("❌ You haven't joined yet!", show_alert=True)
        return USER_SIDE

    if data in ['en', 'bn']:
        context.user_data['lang'] = data
        kb = [[InlineKeyboardButton("🔵 1XBET", callback_data='1x'), InlineKeyboardButton("🟡 MELBET", callback_data='mel')]]
        await query.message.delete()
        await context.bot.send_photo(update.effective_chat.id, IMG_CHOOSE_PLATFORM, "🎮 <b>Choose Platform:</b>", reply_markup=InlineKeyboardMarkup(kb))
    
    elif data in ['1x', 'mel']:
        promo = "BLACK696" if data == '1x' else "BLACK220"
        context.user_data['promo'] = promo
        kb = [[InlineKeyboardButton("🔗 Register", url=LINK_REGISTRATION)], [InlineKeyboardButton("✅ Done", callback_data='id_step')]]
        await query.message.delete()
        await context.bot.send_photo(update.effective_chat.id, IMG_REGISTRATION, f"🚀 <b>Promo:</b> <code>{promo}</code>\n\nঅ্যাকাউন্ট খুলে নিচের 'Done' বাটনে ক্লিক করে আপনার ID পাঠান।", reply_markup=InlineKeyboardMarkup(kb))
    
    elif data == 'id_step':
        await query.message.reply_text("📩 <b>আপনার ID নাম্বারটি এখানে লিখুন:</b>")
        return USER_SIDE
    
    return USER_SIDE

async def id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text
    if not uid.isdigit() or len(uid) < 8:
        await update.message.reply_text("❌ <b>ভুল ID!</b> সঠিক আইডি নাম্বার পাঠান।")
        return USER_SIDE
    
    promo = context.user_data.get('promo', 'BLACK220')
    kb = [[InlineKeyboardButton("🍎 OPEN HACK", web_app=WebAppInfo(url=WEBAPP_URL))], [InlineKeyboardButton("👨‍💻 Admin", url=ADMIN_USER_LINK)]]
    await update.message.reply_photo(FINAL_IMAGE_URL, f"✅ <b>Verified!</b>\n\n<b>ID:</b> {uid}\n<b>Promo:</b> {promo}\n\nএখন নিচের অ্যাপ অপশনে ক্লিক করে কাজ শুরু করুন।", reply_markup=InlineKeyboardMarkup(kb))
    return ConversationHandler.END

# ================= মেইন রানার =================
if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()
    
    bot_app = ApplicationBuilder().token(BOT_TOKEN).defaults(Defaults(parse_mode=ParseMode.HTML)).concurrent_updates(True).build()

    # Admin Handler
    admin_conv = ConversationHandler(
        entry_points=[CommandHandler('admin', admin_cmd)],
        states={
            ADMIN_SIDE: [CallbackQueryHandler(admin_callback)],
            BC_WAIT: [MessageHandler(filters.ALL & ~filters.COMMAND, start_broadcast)]
        },
        fallbacks=[CommandHandler('admin', admin_cmd)],
        allow_reentry=True
    )

    # User Handler
    user_conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            USER_SIDE: [CallbackQueryHandler(user_callback), 
                        MessageHandler(filters.TEXT & ~filters.COMMAND, id_handler)]
        },
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True
    )

    bot_app.add_handler(admin_conv)
    bot_app.add_handler(user_conv)
    
    print("Bot is ready and fixed!")
    bot_app.run_polling(drop_pending_updates=True)

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

# ================= কনফিগারেশন =================
# আপনার সঠিক আইডি এখানে দিন। আইডি ভুল হলে /admin কাজ করবে না।
ADMIN_ID = 7406442919  
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8511299158:AAFXkGzhz5Li22MXmXl1wThQLaSGp0om2Lc")
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

# States
CHECK_JOIN, SELECT_LANGUAGE, CHOOSE_PLATFORM, WAITING_FOR_ID = range(4)
ADMIN_MAIN, BC_CONTENT, BC_BUTTON_TEXT, BC_BUTTON_URL, BC_CONFIRM = range(10, 15)

# ================= ডাটাবেস =================
def save_user(user_id):
    if not os.path.exists(USER_FILE): open(USER_FILE, "w").close()
    with open(USER_FILE, "r") as f: users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USER_FILE, "a") as f: f.write(f"{str(user_id)}\n")

def get_users_list():
    if not os.path.exists(USER_FILE): return []
    with open(USER_FILE, "r") as f: return f.read().splitlines()

# ================= ওয়েব সার্ভার =================
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# ================= ইউজার টেক্সট =================
TEXTS = {
    'en': {
        'choose_platform_caption': "🎮 <b>CHOOSE YOUR PLATFORM</b>",
        'btn_help': "🆘 Help",
        'reg_title': "🚀 <b>{platform} REGISTRATION</b>",
        'reg_msg': "⚠️ Use promo <code>{promo}</code>\nSend ID here.",
        'btn_reg_link': "🔗 Register {platform}",
        'btn_next': "✅ I Registered",
        'ask_id': "📩 <b>SEND YOUR ID</b>",
        'error_length': "❌ 9-10 digits only.",
        'success_caption': "✅ <b>VERIFIED!</b>\n🆔 ID: <code>{uid}</code>\nPromo: <b>{promo}</b>",
        'btn_open_hack': "🍎 OPEN HACK (WebApp)",
        'btn_contact': "👨‍💻 Admin"
    },
    'bn': {
        'choose_platform_caption': "🎮 <b>প্ল্যাটফর্ম নির্বাচন করুন</b>",
        'btn_help': "🆘 সাহায্য",
        'reg_title': "🚀 <b>{platform} রেজিস্ট্রেশন</b>",
        'reg_msg': "⚠️ প্রোমো কোড: <code>{promo}</code>\nরেজিস্ট্রেশন করে আইডি পাঠান।",
        'btn_reg_link': "🔗 {platform} লিংক",
        'btn_next': "✅ রেজিস্ট্রেশন করেছি",
        'ask_id': "📩 <b>আপনার আইডি পাঠান</b>",
        'error_length': "❌ ভুল আইডি! ৯-১০ সংখ্যা দিন।",
        'success_caption': "✅ <b>ভেরিফাইড সফল!</b>\n🆔 ID: <code>{uid}</code>\nপ্রোমো: <b>{promo}</b>",
        'btn_open_hack': "🍎 হ্যাক চালু করুন",
        'btn_contact': "👨‍💻 এডমিন"
    }
}

# ================= এডমিন ফাংশনস =================
async def admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return ConversationHandler.END
    
    users = get_users_list()
    keyboard = [
        [InlineKeyboardButton("📢 Broadcast (মেসেজ পাঠান)", callback_data='bc_start')],
        [InlineKeyboardButton("📊 Total Users", callback_data='admin_stats')],
        [InlineKeyboardButton("❌ Close", callback_data='admin_close')]
    ]
    await update.message.reply_text(
        f"👑 <b>Admin Panel</b>\n\nTotal Users: <code>{len(users)}</code>",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return ADMIN_MAIN

async def admin_stats_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    users_count = len(get_users_list())
    await query.answer(f"Total Users: {users_count}", show_alert=True)
    return ADMIN_MAIN

async def bc_start_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_text("📤 <b>কি পাঠাতে চান?</b>\nটেক্সট, ফটো বা ভিডিও পাঠান (ক্যাপশনসহ)।")
    return BC_CONTENT

async def bc_get_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        context.user_data['bc_type'], context.user_data['bc_fid'] = 'photo', update.message.photo[-1].file_id
        context.user_data['bc_text'] = update.message.caption
    elif update.message.video:
        context.user_data['bc_type'], context.user_data['bc_fid'] = 'video', update.message.video.file_id
        context.user_data['bc_text'] = update.message.caption
    else:
        context.user_data['bc_type'], context.user_data['bc_text'] = 'text', update.message.text

    keyboard = [[InlineKeyboardButton("🚀 Send Now", callback_data='confirm_bc')],
                [InlineKeyboardButton("❌ Cancel", callback_data='admin_close')]]
    await update.message.reply_text("মেসেজটি কি এখনই পাঠাবেন?", reply_markup=InlineKeyboardMarkup(keyboard))
    return BC_CONFIRM

async def bc_final_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    users = get_users_list()
    await query.edit_text(f"⏳ {len(users)} জনের কাছে পাঠানো হচ্ছে...")

    bc_type = context.user_data.get('bc_type')
    text = context.user_data.get('bc_text')
    fid = context.user_data.get('bc_fid')
    
    count = 0
    for uid in users:
        try:
            if bc_type == 'photo': await context.bot.send_photo(uid, fid, caption=text)
            elif bc_type == 'video': await context.bot.send_video(uid, fid, caption=text)
            else: await context.bot.send_message(uid, text)
            count += 1
            if count % 25 == 0: await asyncio.sleep(0.5)
        except: continue

    await context.bot.send_message(ADMIN_ID, f"✅ ব্রডকাস্ট সফল!\nপ্রেরিত: {count}")
    return ConversationHandler.END

# ================= ইউজার হ্যান্ডলারস =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    if update.callback_query: await update.callback_query.answer()

    # মেম্বারশিপ চেক
    try:
        member = await context.bot.get_chat_member(REQUIRED_CHANNEL_ID, user.id)
        is_member = member.status in ['creator', 'administrator', 'member']
    except: is_member = False

    if not is_member:
        keyboard = [[InlineKeyboardButton("📢 Join Channel", url=CHANNEL_INVITE_LINK)],
                    [InlineKeyboardButton("✅ Joined", callback_data='check_join')]]
        await context.bot.send_photo(update.effective_chat.id, IMG_START, "👋 Join our channel first!", reply_markup=InlineKeyboardMarkup(keyboard))
        return CHECK_JOIN

    keyboard = [[InlineKeyboardButton("🇺🇸 English", callback_data='lang_en'),
                 InlineKeyboardButton("🇧🇩 বাংলা", callback_data='lang_bn')]]
    await context.bot.send_photo(update.effective_chat.id, IMG_LANG, "🌐 Select Language:", reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECT_LANGUAGE

async def lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split('_')[1]
    context.user_data['lang'] = lang
    t = TEXTS[lang]
    keyboard = [[InlineKeyboardButton("🔵 1XBET", callback_data='p_1xbet'),
                 InlineKeyboardButton("🟡 MELBET", callback_data='p_melbet')]]
    await query.message.delete()
    await context.bot.send_photo(update.effective_chat.id, IMG_CHOOSE_PLATFORM, t['choose_platform_caption'], reply_markup=InlineKeyboardMarkup(keyboard))
    return CHOOSE_PLATFORM

async def platform_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    p_name = "1XBET" if "1xbet" in query.data else "MELBET"
    promo = "BLACK696" if "1xbet" in query.data else "BLACK220"
    context.user_data.update({'p_name': p_name, 'promo': promo})
    lang = context.user_data.get('lang', 'en')
    t = TEXTS[lang]
    keyboard = [[InlineKeyboardButton(t['btn_reg_link'].format(platform=p_name), url=LINK_REGISTRATION)],
                [InlineKeyboardButton(t['btn_next'], callback_data='go_verify')]]
    await query.message.delete()
    await context.bot.send_photo(update.effective_chat.id, IMG_REGISTRATION, t['reg_msg'].format(promo=promo), reply_markup=InlineKeyboardMarkup(keyboard))
    return CHOOSE_PLATFORM

async def ask_id_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    lang = context.user_data.get('lang', 'en')
    await update.callback_query.message.reply_text(TEXTS[lang]['ask_id'])
    return WAITING_FOR_ID

async def verify_id_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()
    lang = context.user_data.get('lang', 'en')
    t = TEXTS[lang]
    if not uid.isdigit() or not (9 <= len(uid) <= 10):
        await update.message.reply_text(t['error_length'])
        return WAITING_FOR_ID
    
    keyboard = [[InlineKeyboardButton(t['btn_open_hack'], web_app=WebAppInfo(url=WEBAPP_URL))],
                [InlineKeyboardButton(t['btn_contact'], url=ADMIN_USER_LINK)]]
    await update.message.reply_photo(FINAL_IMAGE_URL, t['success_caption'].format(uid=uid, promo=context.user_data['promo']), reply_markup=InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END

# ================= মেইন রানার =================
if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()
    
    app_bot = ApplicationBuilder().token(BOT_TOKEN).defaults(Defaults(parse_mode=ParseMode.HTML)).concurrent_updates(True).build()

    # এডমিন হ্যান্ডলার (এটি সবার উপরে রাখতে হবে)
    admin_h = ConversationHandler(
        entry_points=[CommandHandler('admin', admin_cmd)],
        states={
            ADMIN_MAIN: [CallbackQueryHandler(bc_start_cb, pattern='bc_start'),
                        CallbackQueryHandler(admin_stats_cb, pattern='admin_stats'),
                        CallbackQueryHandler(lambda u,c: ConversationHandler.END, pattern='admin_close')],
            BC_CONTENT: [MessageHandler(filters.ALL & ~filters.COMMAND, bc_get_content)],
            BC_CONFIRM: [CallbackQueryHandler(bc_final_send, pattern='confirm_bc')]
        },
        fallbacks=[CommandHandler('admin', admin_cmd)],
        allow_reentry=True
    )

    # ইউজার হ্যান্ডলার
    user_h = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHECK_JOIN: [CallbackQueryHandler(start, pattern='check_join')],
            SELECT_LANGUAGE: [CallbackQueryHandler(lang_callback, pattern='^lang_')],
            CHOOSE_PLATFORM: [CallbackQueryHandler(platform_callback, pattern='^p_'),
                             CallbackQueryHandler(ask_id_step, pattern='go_verify')],
            WAITING_FOR_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_id_final)]
        },
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True
    )

    app_bot.add_handler(admin_h)
    app_bot.add_handler(user_h)
    
    print("Bot is alive and optimized...")
    app_bot.run_polling(drop_pending_updates=True)

import logging
import os
importid, photo=photo, caption=caption, reply_markup=reply_markup, parse_mode='HTML') asyncio
import sys
import json
from threading import Thread
from flask import Flask
import firebase_admin
from firebase_admin import credentials, db
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext
    except:
        await context.bot.send_message(chat_id=chat_id, text=caption, reply_markup=reply_markup, parse_mode='HTML')

async def start(update: import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
     Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_MessageHandler,
    filters,
    ConversationHandler
)

# ================= লগিং সেটআপ =================

logging.user_to_firebase(user)
    context.user_data.clear()
    
    if notbasicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO await check_membership(update, context):
        keyboard = []
        for channel in REQUIRED_CHANNELS:
            keyboard.append([InlineKeyboardButton(channel["name"], url=channel["link"])])
            
)
logger = logging.getLogger(__name__)

# ================= ফায়ারবেস কানেকশন =================

try        keyboard.append([InlineKeyboardButton("✅ I Have Joined", callback_data='check_join_status')])
:
    if not firebase_admin._apps:
        firebase_json = os.environ.get("FIRE        
        await safe_send_photo(context, update.effective_chat.id, IMG_START, fBASE_JSON")

        if firebase_json:
            cred_dict = json.loads(firebase_json)
            cred = credentials.Certificate(cred_dict)
            logger.info("✅ Firebase initialized from Environment"👋 Hello {user.first_name}!\nJoin all channels to use this bot.", InlineKeyboardMarkup(keyboard Variable!")
        elif os.path.exists("firebase-key.json"):
            cred = credentials.Certificate))
        return CHECK_JOIN
        
    await show_language_menu(update, context)
    ("firebase-key.json")
            logger.info("✅ Firebase initialized from firebase-key.json file!")return SELECT_LANGUAGE

async def check_join_callback(update: Update, context: ContextTypes.DEFAULT_
        else:
            logger.error("❌ No Firebase credentials found!")
            sys.exit(1)

        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://telegram-TYPE):
    query = update.callback_query
    await query.answer()
    
    if await check_membership(update, context):
        await show_language_menu(update, context)
        return60f96-default-rtdb.firebaseio.com/'
        })

    db. SELECT_LANGUAGE
    else:
        await query.message.reply_text("❌ Join both channels first!")reference('connection_test').set({'status': 'online'})

except Exception as e:
    logger.error
        return CHECK_JOIN

async def show_language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data='lang_en'), InlineKeyboardButton("🇧🇩 বাংলা", callback_data='lang_bn')]
    ]
    if(f"❌ Firebase Critical Error: {e}")
    sys.exit(1)

# ================= ডাটাবেস ফাংশন =================

def save_user_to_firebase(user):
    try:
        ref = db.reference(f'users/{user.id}')
        if ref.get() is None:
 update.callback_query:
        try: await update.callback_query.message.delete()
        except            ref.set({'id': user.id, 'first_name': user.first_name, 'username': user.username, 'status': 'active'})
    except Exception as e:
        logger.error(: pass
        
    await safe_send_photo(context, update.effective_chat.id, IMG_LANG, "🌐 Select Language:", InlineKeyboardMarkup(keyboard))

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answerf"❌ Error saving user: {e}")

def get_all_users():
    try:
        ref = db.reference('users')
        users = ref.get()
        return list(users.keys()
    context.user_data['lang'] = query.data.split('_')[1]
    
    lang = context.user_data['lang']
    t = TEXTS[lang]
    keyboard =()) if users else []
    except:
        return []

# ================= ওয়েব সার্ভার =================

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Online"

def run_flask():
    port = int(os.environ.get("PORT", 808 [
        [InlineKeyboardButton("🔵 1XBET", callback_data='platform_1XBET'), InlineKeyboardButton("🟡 MELBET", callback_data='platform_MELBET')],
        [InlineKeyboardButton(t['btn_help'], url=ADMIN_USER_LINK)]
    ]
    
    try: await query.message.0))
    app.run(host='0.0.0.0', port=port)

#delete()
    except: pass
    await safe_send_photo(context, update.effective_chat. ================= বটের কনফিগারেশন =================

BOT_TOKEN = "8638577238:AAGmHqBMuaTw-KJi7rg7w2GfJwAooJdxMYid, IMG_CHOOSE_PLATFORM, t['choose_platform_caption'], InlineKeyboardMarkup(keyboard))
    return CHOOSE_PLATFORM

async def platform_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):Y"
ADMIN_ID = 1146186608

# <-- এখানে দুটি চ্যানেল সেট
    query = update.callback_query
    await query.answer()
    
    platform = query. করা হয়েছে -->
REQUIRED_CHANNELS =data.split('_')[1]
    context.user_data['chosen_platform'] = platform
    lang = context.user_data.get('lang', 'en')
    t = TEXTS[lang]
    promo = PROMO_CODES.get(platform)
    
    text = f"{t['reg_title'].format(platform=platform)}\n\n{t['reg_msg'].format(promo=promo)}" [
    {"id": "-1001481593780", "link": "https://t.me/+3U0nMzWs4Aw0YjFl", "name": "📢 Join Channel 1"},
    {"id": "-1003974496364", "link": "https://t.me/+WeqyzLHAMWhjMmU1", "name": "📢 Join Channel 2"}
]

PROMO
    keyboard = [
        [InlineKeyboardButton(t['btn_reg_link'].format(platform=platform), url=LINK_REGISTRATION)],
        [InlineKeyboardButton(t['btn_next'], callback_data='_CODES = {"1XBET": "BLACK696", "MELBET": "BETBD666account_created')]
    ]
    
    try: await query.message.delete()
    except:"}
LINK_REGISTRATION = "https://bit.ly/BLACK220"
ADMIN_USER_LINK = "https://t.me/SUNNY_BRO1"

# --- নতুন ওয়েব অ্যাপ লিংক সমূহ ---
APPLE_HACK_URL = "https://1xbet-melbet-apple.unaux.com/" pass
    await safe_send_photo(context, update.effective_chat.id, IMG_REGISTRATION, text, InlineKeyboardMarkup(keyboard))
    return CHOOSE_PLATFORM

async def wait_and_ask_
THIMBLES_HACK_URL = "https://thimbles-melbet.netlify.appid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    /"
CRASH_SIGNAL_URL = "https://crasgsignaldog.netlify.app/"

await query.answer()
    
    lang = context.user_data.get('lang', 'en')
    msg = await query.message.reply_text(TEXTS[lang]['wait_msg'], parse_mode='IMG_START = "https://i.ibb.co/LzJF0GGz/file-00000000ee647208a867f87bc931da8c.png"
IMG_LANG = "https://i.ibb.co/LzJF0GGzHTML')
    await asyncio.sleep(2)
    
    try: await msg.delete()
    /file-00000000ee647208a867f8except: pass
    await query.message.reply_text(TEXTS[lang]['ask_id'], parse_mode='HTML')
    return WAITING_FOR_ID

async def receive_id(update: Update7bc931da8c.png"
IMG_CHOOSE_PLATFORM = "https://i, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.text.strip()
    .ibb.co.com/NdFDsT4P/file-00000000lang = context.user_data.get('lang', 'en')
    t = TEXTS[lang]
    
    if not uid.isdigit() or len(uid) < 9:
        await update.5308720880754a5daa131c74.png"
IMG_REGISTRATION = "https://i.ibb.co/3nLpry7/file-0000000059b072089f5ecf92bmessage.reply_text(t['error_digit'])
        return WAITING_FOR_ID

    keyboard = [
        [InlineKeyboardButton(t['btn_apple_hack'], web_app=WebAppInfo(url=APPLE_19ec92b.png"
FINAL_IMAGE_URL = "https://i.ibb.coHACK_URL))],
        [InlineKeyboardButton(t['btn_thimbles_hack'], web_app=WebAppInfo(url=THIMBLES_HACK_URL))],
        [InlineKeyboardButton(t['btn_crash_signal'], web_app=WebAppInfo(url=CRASH_SIGNAL_URL))],
        /3nLpry7/file-0000000059b072089f5ecf92b19ec92b.png"

TEXTS = {
    '[InlineKeyboardButton(t['btn_contact'], url=ADMIN_USER_LINK)]
    ]

    awaiten': {
        'choose_platform_caption': "🎮 CHOOSE YOUR PLATFORM",
        'btn_help': "🆘 Help",
        'reg_title': "🚀 {platform} REGISTRATION",
        ' safe_send_photo(context, update.effective_chat.id, FINAL_IMAGE_URL, t['success_caption'].format(uid=uid), InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END

#reg_msg': "⚠️ WARNING: Use promo {promo}.",
        'btn_reg_link': "🔗 Register {platform}",
        'btn_next': "✅ I Registered",
        'wait_msg': "⏳ Connecting...",
        'ask_id': "📩 SEND YOUR NEW ID",
        'error_digit': " ================= অ্যাডমিন অ্যাসিস্ট্যান্ট ফাংশনস =================

def parse_buttons(text: str):
    """
❌ Invalid ID.",
        'success_caption': "✅ VERIFIED!\n🆔 ID: {uid}",
    টেক্সট থেকে বাটন ও লিংক আলাদা করার ফাংশন।
    ফাইল ক্যাপশন বা টেক্স        'btn_apple_hack': "🍎 APPLE HACK",
        'btn_thimbles_hack': "🎲 THIMBLES HACK",
        'btn_crash_signal': "🚀 CRASH SIGNALটের নিচে 'BUTTONS:' লিখে বাটন যোগ করার অপশন দেয়।
    """
    if not text:
        ",
        'btn_contact': "👨‍💻 Admin"
    },
    'bn': {
        'choose_platform_caption': "🎮 প্ল্যাটফর্ম নির্বাচন করুন",
        'btn_help': "🆘 সাহায্য",
        'reg_title': "🚀 {platform} রেজিস্ট্রেশন",
        'reg_msg':return None, None
    
    marker = "BUTTONS:"
    if marker in text:
        parts = text.split(marker)
        clean_text = parts[0].strip()
        button_lines = parts[1].strip().split('\n')
        
        keyboard = []
        for line in button_lines:
            if '|' in line:
                btn_parts = line.split('|', 1)
 "⚠️ সতর্কতা: প্রোমো ব্যবহার করুন: {promo}.",
        'btn_reg_link': "🔗 {platform}                btn_name = btn_parts[0].strip()
                btn_url = btn_parts[1].strip()
                if btn_name and btn_url.startswith(('http://', 'https://')):
 রেজিস্ট্রেশন",
        'btn_next': "✅ রেজিস্ট্রেশন করেছি",
        'wait_msg': "⏳ সার্ভারে কানেক্ট হচ্ছে...",
        'ask_id': "📩 আপনার আইডি পাঠান",
        'error                    keyboard.append([InlineKeyboardButton(btn_name, url=btn_url)])
        
        if keyboard_digit': "❌ ভুল আইডি।",
        'success_caption': "✅ ভেরিফাইড সফল!\:
            return clean_text, InlineKeyboardMarkup(keyboard)
        return clean_text, None
        
    return text, None

async def send_broadcast_to_user(bot, chat_id, bc_n🆔 ID: {uid}",
        'btn_apple_hack': "🍎 অ্যাপেল হ্যাক",
        'btn_thimbles_hack': "🎲 থাম্বস হ্যাক",
        'btn_crash_signaldata):
    """
    ইউজারের কাছে মিডিয়াসহ মেসেজ পাঠানোর হেল্পার।
    """
    ': "🚀 ক্র্যাশ সিগন্যাল",
        'btn_contact': "👨‍💻 এডমিন"m_type = bc_data['type']
    file_id = bc_data['file_id']
    text = bc_data['text']
    markup = bc_data['markup']
    
    
    }
}

CHECK_JOIN, SELECT_LANGUAGE, CHOOSE_PLATFORM, WAITING_FOR_ID = range(4)
# অ্যাডমিন সেকশনের নতুন স্ট্যাটাস কোড
ADMIN_GET_CONTENT, ADMIN_GET_BUTTONS, ADMIN_CONFIRM = range(10, 13)

# =if m_type == 'photo':
        await bot.send_photo(chat_id=chat_id, photo=file_id, caption=text, reply_markup=markup, parse_mode='HTML')
================ হ্যান্ডলার ফাংশনস =================

async def check_membership(update: Update, context: ContextTypes.DEFAULT    elif m_type == 'video':
        await bot.send_video(chat_id=chat__TYPE):
    try:
        for channel in REQUIRED_CHANNELS:
            member = await context.bot.get_chat_member(chat_id=channel["id"], user_id=update.effective_user.id, video=file_id, caption=text, reply_markup=markup, parse_mode='HTML')
    elif m_type == 'document':
        await bot.send_document(chat_id=chatid)
            if member.status not in ['creator', 'administrator', 'member']:
                return False
        return True
    except:
        return False

async def safe_send_photo(context, chat__id, document=file_id, caption=text, reply_markup=markup, parse_mode='HTMLid, photo, caption=None, reply_markup=None):
    try:
        await context.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup')
    else:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode='HTML')

# ================= অ্যাডমিন সেকশন =================

async def admin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    # মোট ইউজার সংখ্যা=reply_markup, parse_mode='HTML')
    except:
        await context.bot.send_ গণনা করা হচ্ছে
    user_ids = get_all_users()
    total_users = len(user_ids)message(chat_id=chat_id, text=caption, reply_markup=reply_markup, parse_
    
    instruction = (
        f"👑 *অ্যাডমিন প্যানেল*\n\n"mode='HTML')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
        f"📊 *মোট একটিভ ইউজার:* {total_users} জন\n\n"
        f"📢 *ব্রডকাস্ট পাঠানোর নিয়ম:*\n"
        f"যেকোনো মেসেজ (টেক্সটuser = update.effective_user
    save_user_to_firebase(user)
    context.user_data.clear()
    
    if not await check_membership(update, context):
        keyboard = []
        for channel in REQUIRED_CHANNELS:
            keyboard.append([InlineKeyboardButton(channel["name"], url=channel["link"])])
            
        keyboard.append([InlineKeyboardButton("✅ I Have Joined", callback_data='check_join_status')])
        
        await safe_send_photo(context, update, ছবি, ভিডিও বা ফাইল) লিখে পাঠান।\n\n"
        f"🔗 *বাটন যুক্ত করতে.effective_chat.id, IMG_START, f"👋 Hello {user.first_name}!\nJoin all channels to use this bot.", InlineKeyboardMarkup(keyboard))
        return CHECK_JOIN
        
    await show_ চাইলে:* মেসেজ বা ক্যাপশনের নিচে এভাবে লিখুন:\n"
        f"```\n"
        f"এখানে আপনার মেইন টেক্সট\n\n"
        f"BUTTONS:\n"
        f"Google | https://google.com\n"
        f"Join Channel | https://t.me/language_menu(update, context)
    return SELECT_LANGUAGE

async def check_join_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if await check_membership(update, context):
        await show_languageyourchannel\n"
        f"```"
    )
    
    await update.message.reply_text(_menu(update, context)
        return SELECT_LANGUAGE
    else:
        await query.message.reply_text("❌ Join both channels first!")
        return CHECK_JOIN

async def show_language_menuinstruction, parse_mode='Markdown')
    return ADMIN_GET_CONTENT

async def admin_get_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    bc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard =_data = {
        'type': 'text',
        'file_id': None,
        ' [
        [InlineKeyboardButton("🇺🇸 English", callback_data='lang_en'), InlineKeyboardButton("🇧🇩 বাংলা", callback_data='lang_bn')]
    ]
    if update.callback_query:
        try: await update.callbacktext': None,
        'markup': None
    }

    raw_text = msg.text or msg.caption or ""
    clean_text, markup = parse_buttons(raw_text)

    # মিডিয়া টাইপ সনাক্ত_query.message.delete()
        except: pass
        
    await safe_send_photo(context, update.effective_chat.id, IMG_LANG, "🌐 Select Language:", InlineKeyboardMarkup(keyboard))

করণ
    if msg.photo:
        bc_data['type'] = 'photo'
        bc_dataasync def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['lang'] = query.['file_id'] = msg.photo[-1].file_id
        bc_data['text'] = clean_text
        bc_data['markup'] = markup
    elif msg.video:
        bc_data.split('_')[1]
    
    lang = context.user_data['lang']
    t = TEXTS[lang]
    keyboard =data['type'] = 'video'
        bc_data['file_id'] = msg.video.file_id
        bc_data['text'] = clean_text
        bc_data['markup'] = markup [
        [InlineKeyboardButton("🔵 1XBET", callback_data='platform_1XBET'), InlineKeyboardButton("🟡 MELBET", callback_data='platform_MELBET')],
        [InlineKeyboardButton(t['btn_help'], url=ADMIN_USER_LINK)]
    ]
    
    try: await query.message.delete()
    except: pass
    await safe_send
    elif msg.document:
        bc_data['type'] = 'document'
        bc_data['file_id'] = msg.document.file_id
        bc_data['text'] = clean_text
        bc_data['markup'] = markup
    else:
        bc_data['type'] =_photo(context, update.effective_chat.id, IMG_CHOOSE_PLATFORM, t['choose_platform_caption'], InlineKeyboardMarkup(keyboard))
    return CHOOSE_PLATFORM

async def platform_choice 'text'
        bc_data['text'] = clean_text
        bc_data['markup'] = markup

    context.user_data['bc_data'] = bc_data

    # প্রিভিউ পাঠানো
    await update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
.message.reply_text("📥 *আপনার ব্রডকাস্ট মেসেজের প্রিভিউ:*", parse_mode='Markdown')
    
    if bc_data['type'] == 'photo':
        await update.message.    await query.answer()
    
    platform = query.data.split('_')[1]
    context.user_data['chosen_platform'] = platform
    lang = context.user_data.get('langreply_photo(photo=bc_data['file_id'], caption=bc_data['text'], reply_', 'en')
    t = TEXTS[lang]
    promo = PROMO_CODES.get(platform)
    
    text = f"{t['reg_title'].format(platform=platform)}\n\markup=markup, parse_mode='HTML')
    elif bc_data['type'] == 'video':
        await update.message.reply_video(video=bc_data['file_id'], caption=bc_datan{t['reg_msg'].format(promo=promo)}"
    keyboard = [
        [InlineKeyboardButton(t['btn_reg_link'].format(platform=platform), url=LINK_REGISTRATION)],
        ['text'], reply_markup=markup, parse_mode='HTML')
    elif bc_data['type'] == 'document':
        await update.message.reply_document(document=bc_data['file_id'], caption[InlineKeyboardButton(t['btn_next'], callback_data='account_created')]
    ]
    
    try: await query.message.delete()
    except: pass
    await safe_send_photo(=bc_data['text'], reply_markup=markup, parse_mode='HTML')
    else:
        await update.message.reply_text(text=bc_data['text'], reply_markup=markup,context, update.effective_chat.id, IMG_REGISTRATION, text, InlineKeyboardMarkup(keyboard))
    return CHOOSE_PLATFORM

async def wait_and_ask_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
     parse_mode='HTML')

    confirm_keyboard = [
        [InlineKeyboardButton("✅ ব্রডকাস্ট শুরু করুন", callback_data='bc_confirm')],
       
    lang = context.user_data.get('lang', 'en')
    msg = await query. [InlineKeyboardButton("❌ বাতিল করুন", callback_data='bc_cancel')]
    ]
    await update.message.reply_text("আপনি কি এই মেসেজটি সবার কাছে পাঠাতে চান?", reply_markup=InlineKeyboardMarkup(confirm_keyboard))
    return ADMIN_CONFmessage.reply_text(TEXTS[lang]['wait_msg'], parse_mode='HTML')
    await asyncio.sleep(2)
    
    try: await msg.delete()
    except: pass
    await query.IRM

async def admin_broadcast_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'bc_cancelmessage.reply_text(TEXTS[lang]['ask_id'], parse_mode='HTML')
    return WAITING_FOR_ID

async def receive_id(update: Update, context: ContextTypes.DEFAULT_':
        await query.edit_message_text("❌ ব্রডকাস্ট বাতিল করা হয়েছে।")
        return ConversationHandler.END
        
    if query.data == 'bc_confirm':
        await query.TYPE):
    uid = update.message.text.strip()
    lang = context.user_data.get('lang', 'en')
    t = TEXTS[lang]
    
    if not uid.edit_message_text("🚀 ব্রডকাস্ট শুরু হয়েছে, দয়া করে অপেক্ষা করুন...")
        user_ids = get_all_users()
        bc_data = context.user_data.get('bc_isdigit() or len(uid) < 9:
        await update.message.reply_text(t['error_digit'])
        return WAITING_FOR_ID

    keyboard =data')
        
        if not bc_data:
            await query.message.reply_text("❌ কোনো মেসেজ পাওয়া যায়নি।")
            return ConversationHandler.END
            
        success_count = 0
        fail_count = 0
        
        for uid in user_ids:
            try:
                await send [
        [InlineKeyboardButton(t['btn_apple_hack'], web_app=WebAppInfo(url=APPLE_HACK_URL))],
       _broadcast_to_user(context.bot, uid, bc_data)
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to send to {uid}: {e [InlineKeyboardButton(t['btn_thimbles_hack'], web_app=WebAppInfo(url=THIMBLES_HACK_URL))],
        [InlineKeyboardButton(t['btn_crash_signal'], web_}")
                fail_count += 1
            await asyncio.sleep(0.05) # অ্যান্টি-app=WebAppInfo(url=CRASH_SIGNAL_URL))],
        [InlineKeyboardButton(t['btn_contact'], url=ADMIN_USER_LINK)]
    ]

    await safe_send_photo(context,ফ্লাড বিরতি
            
        final_text = f"✅ ব্রডকাস্ট সম্পন্ন হয়েছে!\n\n👥 মোট ইউজার: {len(user_ids)}\nসফলভাবে পাঠানো হয়েছে: {success_ update.effective_chat.id, FINAL_IMAGE_URL, t['success_caption'].format(uid=uid), InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END

# ================= অ্যাডমিন সেকশন =================

asynccount} জনকে\nব্যর্থ হয়েছে: {fail_count} জনের কাছে।"
        await query.message.reply_text(final_text)
        return ConversationHandler.END

# ================= মেইন রানার =================

if def admin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    user_conv = ConversationHandler(
_user.id != ADMIN_ID:
        return
    
    # ডেটাবেস থেকে ইউজারের মোট সংখ্যা সংগ্রহ করা হচ্ছে
    all_users = get_all_users()
    total_users = len(all_users        entry_points=[CommandHandler('start', start)],
        states={
            CHECK_JOIN: [CallbackQueryHandler(check_join_callback, pattern='^check_join_status$')],
            SELECT_LANGUAGE:)
    
    welcome_text = (
        "👑 <b>অ্যাডমিন কন্ট্রোল প্যানেল</b>\n\n"
        f"📊 <b>মোট সচল ইউজার:</b> {total_users} জন\ [CallbackQueryHandler(set_language, pattern='^lang_')],
            CHOOSE_PLATFORM:n\n"
        "📢 ব্রডকাস্ট করার জন্য যেকোনো মেসেজ (টেক্সট, ফটো, ভিডিও, ফাইল ইত্যাদি) লিখে পাঠান অথবা ফরোয়ার্ড করুন।"
    )
    await update.message.reply_text(welcome_text, parse_mode='HTML')
    return ADMIN_GET_CONTENT

async [
                CallbackQueryHandler(platform_choice, pattern='^platform_'),
                CallbackQueryHandler(wait_and_ask_id, pattern='^account_created$')
            ],
            WAITING_FOR_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_id)],
        },
        fall def admin_get_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # পাঠানো বা ফরোয়ার্ড করা মেসেজটি সংরক্ষণ করা হচ্ছে
    context.user_data['bc_msg'] = update.backs=[CommandHandler('start', start)],
        allow_reentry=True
    )

    admin_conv = ConversationHandler(
        entry_points=[CommandHandler('admin', admin_start)],
        states={
            ADMIN_GET_CONTENT: [MessageHandler(filters.ALL & ~filters.COMMAND, admin_get_content)],message
    
    instruction_text = (
        "🔗 <b>আপনি কি মেসেজটির সাথে কোনো বাটন যুক্ত করতে
            ADMIN_CONFIRM: [CallbackQueryHandler(admin_broadcast_action, pattern='^bc_')]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    application.add_handler(user_conv)
    application.add_handler(admin_conv)
    print("Bot is starting চান?</b>\n\n"
        "যদি বাটন এড করতে চান, তাহলে নিচের ফরমেটে লিখে পাঠান:\n"
        "<code>বাটনের নাম | লিংক</code>\n\n"
        "<i>উদাহরণ ( with 2 Channels requirement...")
    application.run_polling()

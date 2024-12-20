import telebot
import os
import threading
import time
import random
import string

# استخدام متغير البيئة لتخزين توكن البوت
bot_token = os.getenv('BOT_TOKEN')
if not bot_token:
    raise ValueError("الرجاء تعيين متغير البيئة BOT_TOKEN")

bot = telebot.TeleBot(bot_token)

# Dictionary لتخزين بيانات المستخدمين
user_data = {}

# قائمة المستخدمين الرباعيين لفحصها
all_possible_users = [
    ''.join(comb) for comb in (
        (a+b+c+d) for a in string.ascii_lowercase for b in string.ascii_lowercase 
        for c in string.ascii_lowercase for d in string.ascii_lowercase
    )
]

# رسالة الترحيب وزرين لإضافة الحساب
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('إضافة حساب إنستغرام', 'إضافة حساب تيك توك')
    bot.send_message(message.chat.id, "اختر نوع الحساب الذي تريد إضافته:", reply_markup=markup)

# إضافة حساب إنستغرام
@bot.message_handler(func=lambda message: message.text == 'إضافة حساب إنستغرام')
def add_instagram_account(message):
    bot.send_message(message.chat.id, "رجاءً أدخل اسم المستخدم لحساب إنستغرام الخاص بك:")
    bot.register_next_step_handler(message, save_instagram_username)

def save_instagram_username(message):
    username = message.text
    user_data[message.chat.id] = {'instagram': username}
    bot.send_message(message.chat.id, f"تم تسجيل حساب إنستغرام الخاص بك: {username}")
    # بدء الفحص الخاص بإنستغرام
    threading.Thread(target=check_instagram_users, args=(message.chat.id, username)).start()

# إضافة حساب تيك توك
@bot.message_handler(func=lambda message: message.text == 'إضافة حساب تيك توك')
def add_tiktok_account(message):
    bot.send_message(message.chat.id, "رجاءً أدخل اسم المستخدم لحساب تيك توك الخاص بك:")
    bot.register_next_step_handler(message, save_tiktok_username)

def save_tiktok_username(message):
    username = message.text
    user_data[message.chat.id] = {'tiktok': username}
    bot.send_message(message.chat.id, f"تم تسجيل حساب تيك توك الخاص بك: {username}")
    # بدء الفحص الخاص بتيك توك
    threading.Thread(target=check_tiktok_users, args=(message.chat.id, username)).start()

# فحص المستخدمين في إنستغرام
def check_instagram_users(chat_id, username):
    checked_users = 0
    available_users = []
    for user in all_possible_users:
        # محاكاة عملية الفحص
        time.sleep(0.1)
        checked_users += 1
        if random.choice([True, False]):  # اعتبر أن المستخدم متاح عشوائيًا
            available_users.append(user)
            # تسجيله وربطه بالحساب
            print(f"ربط المستخدم {user} بحساب {username}")
        if checked_users >= 1000:  # التوقف بعد 1000 فحص
            break
    bot.send_message(chat_id, f"تم فحص {checked_users} مستخدم. وجدنا {len(available_users)} مستخدم متاح.")

# فحص المستخدمين في تيك توك
def check_tiktok_users(chat_id, username):
    checked_users = 0
    available_users = []
    for user in all_possible_users:
        # محاكاة عملية الفحص
        time.sleep(0.1)
        checked_users += 1
        if random.choice([True, False]):  # اعتبر أن المستخدم متاح عشوائيًا
            available_users.append(user)
            # تسجيله وربطه بالحساب
            print(f"ربط المستخدم {user} بحساب {username}")
        if checked_users >= 1000:  # التوقف بعد 1000 فحص
            break
    bot.send_message(chat_id, f"تم فحص {checked_users} مستخدم. وجدنا {len(available_users)} مستخدم متاح.")

# تشغيل البوت
print("Bot is running...")
bot.infinity_polling()
                     

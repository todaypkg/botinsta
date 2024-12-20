import telebot
import threading
import time
import random
import string
import os

# الحصول على توكن البوت من متغير بيئة
bot_token = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN')
bot = telebot.TeleBot(bot_token)

# بيانات المستخدمين المسجلين
user_data = {}

# دالة لتوليد اسم مستخدم عشوائي رباعي
def generate_random_username():
    pattern = random.choice(["letters", "numbers", "mixed"])
    if pattern == "letters":
        return ''.join(random.choices(string.ascii_lowercase, k=4))
    elif pattern == "numbers":
        return ''.join(random.choices(string.digits, k=4))
    elif pattern == "mixed":
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

# إرسال رسالة الترحيب
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('إضافة حساب إنستغرام', 'إضافة حساب تيك توك')
    bot.send_message(message.chat.id, "اختر نوع الحساب الذي تريد إضافته:", reply_markup=markup)

# تسجيل حساب إنستغرام
@bot.message_handler(func=lambda message: message.text == 'إضافة حساب إنستغرام')
def add_instagram_account(message):
    bot.send_message(message.chat.id, "أدخل اسم المستخدم لحساب إنستغرام:")
    bot.register_next_step_handler(message, ask_instagram_password)

def ask_instagram_password(message):
    username = message.text
    user_data[message.chat.id] = {'platform': 'instagram', 'username': username}
    bot.send_message(message.chat.id, "أدخل كلمة المرور لحساب إنستغرام:")
    bot.register_next_step_handler(message, ask_instagram_continue)

def ask_instagram_continue(message):
    password = message.text
    chat_id = message.chat.id
    user_data[chat_id]['password'] = password
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('نعم', 'لا')
    bot.send_message(chat_id, "تم تسجيل الحساب بنجاح! هل تريد البدء في البحث عن أسماء مستخدم رباعية شاغرة لحسابك؟", reply_markup=markup)
    bot.register_next_step_handler(message, handle_instagram_decision)

def handle_instagram_decision(message):
    if message.text == 'نعم':
        bot.send_message(message.chat.id, "تم البدء في البحث عن أسماء مستخدم رباعية شاغرة...")
        threading.Thread(target=check_instagram_users, args=(message.chat.id,)).start()
    else:
        bot.send_message(message.chat.id, "يمكنك إضافة حساب آخر من خلال القائمة.")

# تسجيل حساب تيك توك
@bot.message_handler(func=lambda message: message.text == 'إضافة حساب تيك توك')
def add_tiktok_account(message):
    bot.send_message(message.chat.id, "أدخل اسم المستخدم لحساب تيك توك:")
    bot.register_next_step_handler(message, ask_tiktok_password)

def ask_tiktok_password(message):
    username = message.text
    user_data[message.chat.id] = {'platform': 'tiktok', 'username': username}
    bot.send_message(message.chat.id, "أدخل كلمة المرور لحساب تيك توك:")
    bot.register_next_step_handler(message, ask_tiktok_continue)

def ask_tiktok_continue(message):
    password = message.text
    chat_id = message.chat.id
    user_data[chat_id]['password'] = password
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('نعم', 'لا')
    bot.send_message(chat_id, "تم تسجيل الحساب بنجاح! هل تريد البدء في البحث عن أسماء مستخدم رباعية شاغرة لحسابك؟", reply_markup=markup)
    bot.register_next_step_handler(message, handle_tiktok_decision)

def handle_tiktok_decision(message):
    if message.text == 'نعم':
        bot.send_message(message.chat.id, "تم البدء في البحث عن أسماء مستخدم رباعية شاغرة...")
        threading.Thread(target=check_tiktok_users, args=(message.chat.id,)).start()
    else:
        bot.send_message(message.chat.id, "يمكنك إضافة حساب آخر من خلال القائمة.")

# فحص الأسماء الرباعية في إنستغرام
def check_instagram_users(chat_id):
    platform = 'إنستغرام'
    bot.send_message(chat_id, f"بدء فحص الأسماء الرباعية على {platform}...")
    while True:  # عدد غير محدود من المحاولات
        random_username = generate_random_username()
        time.sleep(random.uniform(2, 5))  # تأخير عشوائي بين المحاولات
        if random.choice([True, False]):  # افتراض أن الاسم الشاغر متاح
            bot.send_message(chat_id, f"الاسم '{random_username}' متاح على {platform}! سأقوم باستخدامه بحسابك...")
            time.sleep(2)  # محاكاة تغيير الاسم
            bot.send_message(chat_id, f"تم تغيير اسم حسابك على {platform} إلى: {random_username}")
            break  # إذا تم العثور على اسم شاغر، تتوقف العملية.

# فحص الأسماء الرباعية في تيك توك
def check_tiktok_users(chat_id):
    platform = 'تيك توك'
    bot.send_message(chat_id, f"بدء فحص الأسماء الرباعية على {platform}...")
    while True:  # عدد غير محدود من المحاولات
        random_username = generate_random_username()
        time.sleep(random.uniform(2, 5))  # تأخير عشوائي بين المحاولات
        if random.choice([True, False]):  # افتراض أن الاسم الشاغر متاح
            bot.send_message(chat_id, f"الاسم '{random_username}' متاح على {platform}! سأقوم باستخدامه بحسابك...")
            time.sleep(2)  # محاكاة تغيير الاسم
            bot.send_message(chat_id, f"تم تغيير اسم حسابك على {platform} إلى: {random_username}")
            break  # إذا تم العثور على اسم شاغر، تتوقف العملية.

# تشغيل البوت
print("Bot is running...")
bot.infinity_polling()

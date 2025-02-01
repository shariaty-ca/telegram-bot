import telebot
import config  # Importing the config file

# Assigning the token from config.py
TOKEN = config.TOKEN
bot = telebot.TeleBot(TOKEN)

# Messages for the main menu
messages = {
    "ویدئوهای آموزشی": "به زودی ویدئوهای آموزشی قرار داده خواهد شد.",
    "جزوه اساتید": "جزوه‌های اساتید در دسترس قرار خواهد گرفت.",
    "نظرسنجی ها": "می‌توانید نظرات خود را در این بخش ثبت کنید.",
    "عضویت در انجمن": "برای عضویت در انجمن منتظر اطلاع‌رسانی‌های بعدی باشید."
}

# Response to /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("ویدئوهای آموزشی")
    btn2 = telebot.types.KeyboardButton("جزوه اساتید")
    btn3 = telebot.types.KeyboardButton("نظرسنجی ها")
    btn4 = telebot.types.KeyboardButton("عضویت در انجمن")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(message.chat.id, "به بات دانشگاه شریعتی خوش آمدید! از منوی زیر گزینه‌ای را انتخاب کنید:", reply_markup=markup)

# Response to menu options
@bot.message_handler(func=lambda message: message.text in messages)
def send_response(message):
    bot.send_message(message.chat.id, messages[message.text])

# Run the bot
bot.polling()

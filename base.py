import telebot
import config
import difflib

# Initialize the bot with the token from the config file
TOKEN = config.TOKEN
bot = telebot.TeleBot(TOKEN)

# Initial role of the user (for testing)
user_role = "normal user"

# Predefined responses for each menu option
section_messages = {
    "ویدئوهای آموزشی": "این بخش درحال تکمیل است",
    "جزوه اساتید": "ین بخش درحال تکمیل است",
    "نظرسنجی ها": "این بخش درحال تکمیل است.",
    "عضویت در انجمن": "این بخش درحال تکمیل است.",
    "نشریه": "این بخش درحال تکمیل است.",
    "کارگاه ها": "این بخش درحال تکمیل است.",
    "اضافه کردن ویدئو": "این بخش درحال تکمیل است.",
    "اضافه کردن جزوه": "این بخش درحال تکمیل است.",
    "اطلاعیه": "این بخش درحال تکمیل است.",
    "نشریه ها": "این بخش درحال تکمیل است.",
    "کارگاه": "این بخش درحال تکمیل است.",
    "رفتن به پنل عادی": "شما وارد پنل کاربری عادی شدید.",
    "برگشت به پنل ادمین": "شما وارد پنل ادمین شدید."
}

# Find the closest match to handle slight typos
def find_closest_match(user_input, options):
    matches = difflib.get_close_matches(user_input, options, n=1, cutoff=0.7)
    return matches[0] if matches else None

# Handles the /start command and displays appropriate menus based on user roles
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global user_role

    if user_role == "normal user":
        welcome_message = "خوش اومدید دانشجوی عزیز، لطفا یکی از گزینه های زیر را انتخاب کنید، برای دسترسی به امکانات بیشتر میتونید در انجمن علمی کامپیوتر عضو بشید تا بتونید در کارگاه ها نیز شرکت کنید."
        buttons = ["ویدئوهای آموزشی", "جزوه اساتید", "نظرسنجی ها", "عضویت در انجمن"]
    elif user_role == "member":
        welcome_message = "خوش اومدید عضو عزیز، چه کاری میتونم براتون انجام بدم؟"
        buttons = ["ویدئوهای آموزشی", "جزوه اساتید", "نظرسنجی ها", "نشریه", "کارگاه ها"]
    elif user_role == "admin member":
        welcome_message = "شما وارد حالت ممبر های معمولی شدید، برای برگشت به حالت ادمین، از گزینه برگشت به پنل ادمین استفاده کنید."
        buttons = ["ویدئوهای آموزشی", "جزوه اساتید", "نظرسنجی ها", "نشریه", "کارگاه ها", "برگشت به پنل ادمین"]
    elif user_role == "admin":
        welcome_message = "خوش اومدید ادمین عزیز، چه کاری میخواید انجام بدید؟ این لیست گزینه های شماست:"
        buttons = ["اضافه کردن ویدئو", "اضافه کردن جزوه", "اطلاعیه", "نشریه ها", "کارگاه", "رفتن به پنل عادی"]

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for button in buttons:
        markup.add(telebot.types.KeyboardButton(button))

    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

# Handle /help command
@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = """به قسمت راهنمای ربات انجمن علمی کامپیوتر دانشگاه شریعتی خوش اومدید. این لیست توضیحات برای هر گزینه موجود در پنل هست:

1- ویدئوهای آموزشی: در صورتی که به محتوای آموزشی آزاد برای مطالعات خودتون در حوزه کامپیوتر نیاز دارید، میتونید از این گزینه استفاده کنید.
2- جزوه اساتید: جزوه تمامی اساتید مربوط به حوزه کامپیوتر و منابع امتحانی اون‌ها اینجا قرار گرفته.
3- نظرسنجی ها: اینجا میتونید نظرات خودتون رو وارد کنید تا به مدیران این ربات ارسال بشه.
4- عضویت در انجمن: با زدن این گزینه لینک ثبت‌نام در انجمن برای شما ارسال میشه.

گزینه‌های اضافی پنل عضو:
1- نشریه: فایل‌های مختلف نشریه فانوس اینجا قرار داده میشن.
2- کارگاه‌ها: مشاهده کارگاه‌های فعال و ثبت‌نام در آنها.
"""
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

# Handle /about command
@bot.message_handler(commands=['about'])
def show_about(message):
    about_text = """این ربات، ربات مخصوص انجمن علمی کامپیوتر دانشگاه شریعتی هستش. ما یک انجمن هستیم که در کنار هم دوستانه چیزهای جدید یاد می‌گیریم و تلاش می‌کنیم خاطرات خوبی رو در دانشگاه رقم بزنیم.
    
برای اطلاعات بیشتر می‌تونید در کانال رسمی ما عضو بشید:
➡️ [کانال رسمی انجمن](https://t.me/sca_shariaty) ⬅️
"""
    bot.send_message(message.chat.id, about_text, parse_mode='Markdown')
    # Handle menu options and role transitions with typo handling
@bot.message_handler(func=lambda message: True)
def handle_menu_option(message):
    global user_role

    matched_option = find_closest_match(message.text, section_messages.keys())

    if matched_option:
        # Switch to admin member panel
        if matched_option == "رفتن به پنل عادی" and user_role == "admin":
            user_role = "admin member"
            send_welcome(message)

        # Switch back to admin panel
        elif matched_option == "برگشت به پنل ادمین" and user_role == "admin member":
            user_role = "admin"
            send_welcome(message)

        # Display the predefined response for the selected option
        else:
            bot.send_message(message.chat.id, section_messages[matched_option])
    else:
        bot.send_message(message.chat.id, "گزینه نامعتبر است! لطفاً یکی از گزینه‌های منو را انتخاب کنید.")

# Run the bot
bot.polling()

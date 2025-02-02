import telebot
import config

# Initialize the bot with the token from the config file
TOKEN = config.TOKEN
bot = telebot.TeleBot(TOKEN)

# Initial role of the user (for testing)
user_role = "normal user"

# Predefined responses for each menu option
section_messages = {
    "ویدئوهای آموزشی": "This section is under development.",
    "جزوه اساتید": "This section is under development.",
    "نظرسنجی ها": "This section is under development.",
    "عضویت در انجمن": "This section is under development.",
    "نشریه": "This section is under development.",
    "کارگاه ها": "This section is under development.",
    "اضافه کردن ویدئو": "This section is under development.",
    "اضافه کردن جزوه": "This section is under development.",
    "اطلاعیه": "This section is under development.",
    "نشریه ها": "This section is under development.",
    "کارگاه": "This section is under development.",
    "رفتن به پنل عادی": "Switching to admin member panel.",
    "برگشت به پنل ادمین": "Switching back to admin panel."
}

# Handles the /start command and displays appropriate menus based on user roles
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global user_role

    # Define messages and menu options for each role
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

    # Create the keyboard with buttons
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for button in buttons:
        markup.add(telebot.types.KeyboardButton(button))

    # Send the welcome message with the appropriate menu
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

# Handle /help command
@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = """به قسمت راهنمای ربات انجمن علمی کامپیوتر دانشگاه شریعتی خوش اومدید. این لیست توضیحات برای هر گزینه موجود در پنل هست:

1- **ویدئوهای آموزشی:** در صورتی که به محتوای آموزشی آزاد برای مطالعات خودتون در حوزه کامپیوتر نیاز دارید، میتونید از این گزینه استفاده کنید.
2- **جزوه اساتید:** جزوه تمامی اساتید مربوط به حوزه کامپیوتر و منابع امتحانی اون‌ها اینجا قرار گرفته.
3- **نظرسنجی ها:** اینجا میتونید نظرات خودتون رو وارد کنید تا به مدیران این ربات ارسال بشه.
4- **عضویت در انجمن:** با زدن این گزینه لینک ثبت‌نام در انجمن برای شما ارسال میشه.

گزینه‌های اضافی پنل عضو:
1- **نشریه:** فایل‌های مختلف نشریه فانوس اینجا قرار داده میشن.
2- **کارگاه‌ها:** مشاهده کارگاه‌های فعال و ثبت‌نام در آنها.
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

# Handle menu options and role transitions
@bot.message_handler(func=lambda message: message.text in section_messages)
def handle_menu_option(message):
    global user_role

    # Switch to admin member panel
    if message.text == "رفتن به پنل عادی" and user_role == "admin":
        user_role = "admin member"
        send_welcome(message)

    # Switch back to admin panel
    elif message.text == "برگشت به پنل ادمین" and user_role == "admin member":
        user_role = "admin"
        send_welcome(message)

    # Display the predefined response for the selected option
    else:
        bot.send_message(message.chat.id, section_messages[message.text])

# Run the bot
bot.polling()
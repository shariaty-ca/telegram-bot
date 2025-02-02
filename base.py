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
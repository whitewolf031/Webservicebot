import time
from telebot import TeleBot
from db.employees_db import *
from db.user_id import *
from keyboards import *
from localisation.lang import *
from dotenv import load_dotenv

load_dotenv()

token = Config().token
bot = TeleBot(token)

user_langs = {}

canal_id = os.getenv("CANAL_ID")
owner_id = os.getenv("OWNER_ID")
instagram_link = os.getenv("INSTAGRAM_URL")
youtube_link = os.getenv("YOUTUBE_URL")
telegram_link = os.getenv("TELEGRAM_URL")
employees_details = {}
personal_details = {}
request_details = {}
db = UserIDsDB()

@bot.message_handler(func=lambda message: True)
def testing(message):
    if message.text == '/start':
        return start(message)

    if message.text == '/admin':
        return admin(message)

#---------------------------------Admin panel--------------------------------------
# Adminlarning ID ro'yxati
admin_id = list(map(int, os.getenv("ADMIN_ID").split(',')))

@bot.message_handler(commands=["admin"])
def admin(message):
    chat_id = message.chat.id
    if chat_id in admin_id:
        bot.send_message(chat_id, "Admin panelga xush kelibsiz!", reply_markup=admin_panel_markup())
        bot.register_next_step_handler(message, handle_admin_panel)
    else:
        bot.send_message(chat_id, "Siz admin emassiz!")

@bot.message_handler(func=lambda message: message.chat.id in admin_id)
def handle_admin_panel(message):
    chat_id = message.chat.id

    if message.text == "Yangilik qo'shish":
        create_news = bot.send_message(chat_id, "Yangilik ni yuboring")
        bot.register_next_step_handler(create_news, send_announcement)

    elif message.text == "Bo'limlarni ko'rish":
        bot.send_message(chat_id, "Bu bo'lim vaqtinchalik ishlamaydi.")
        time.sleep(1)
        bot.send_message(chat_id, "Bo'limlardan birini tanlang", reply_markup=admin_panel_markup())

@bot.message_handler(content_types=["photo", "text"])
def send_announcement(message):
    chat_id = message.chat.id

    if chat_id in admin_id:  # Faqat adminlarga ruxsat
        if message.content_type == "photo":
            # Rasm va captionni olish
            photo_id = message.photo[-1].file_id
            caption = message.caption if message.caption else "📢 Yangilik!"

            # Foydalanuvchilarga yuborish
            users = db.get_all_users()

            if users:
                for user_id in users:
                    try:
                        bot.send_photo(user_id, photo_id, caption=caption)
                    except Exception as e:
                        print(f"Xatolik {user_id} ga yuborishda: {e}")
                bot.send_message(chat_id, "📸 Rasmli yangilik muvaffaqiyatli yuborildi!")
                bot.send_message(chat_id, "bo'limlardan birini tanlang", reply_markup=admin_panel_markup())
            else:
                bot.send_message(chat_id, "Hozircha foydalanuvchilar ro'yxati bo'sh.")

        elif message.content_type == "text":
            # Textli yangilikni olish
            news_text = message.text

            # Foydalanuvchilarga yuborish
            users = db.get_all_users()

            if users:
                for user_id in users:
                    try:
                        bot.send_message(user_id, news_text)
                    except Exception as e:
                        print(f"Xatolik {user_id} ga yuborishda: {e}")
                bot.send_message(chat_id, "✉️ Textli yangilik muvaffaqiyatli yuborildi!")
                bot.send_message(chat_id, "bo'limlardan birini tanlang", reply_markup=admin_panel_markup())
            else:
                bot.send_message(chat_id, "Hozircha foydalanuvchilar ro'yxati bo'sh.")
    else:
        bot.send_message(chat_id, "⛔ Siz admin emassiz, yangilik yuborolmaysiz!")

#---------------------------------start--------------------------------------------
@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    db.insert_user(chat_id)
    bot.send_message(chat_id, star_message[lang], reply_markup=generate_language())

@bot.callback_query_handler(func=lambda call: call.data in ["uz","en","ru"])
def Language(call):
    chat_id = call.message.chat.id
    lang = user_langs.get(chat_id, "uz")
    if call.data == "uz":
        lang = "uz"

    elif call.data == "en":
        lang = "en"

    elif call.data == "ru":
        lang = "ru"

    bot.send_message(chat_id, category[lang], reply_markup=menu_keyboards(lang))
    bot.register_next_step_handler(call.message, menu)
    user_langs[chat_id] = lang


def menu(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    photo = open("Media/img1.jpg", "rb")
    photo2 = open("Media/img2.jpg", "rb")

    if message.text == about[lang]:
        bot.send_photo(chat_id, photo, caption=about_us[lang],
                           parse_mode="HTML", reply_markup=generate_back(lang))
        bot.register_next_step_handler(message, back)

    elif message.text == freelancer[lang]:
        bot.send_message(chat_id, "Bo'limlardan birini tanlang", reply_markup=request_keyboards(lang))
        bot.register_next_step_handler(message, freelance_cat)

    elif message.text == zakaz[lang]:
        bot.send_message(chat_id, choose[lang], reply_markup=request_keyboards(lang))
        bot.register_next_step_handler(message, request_shart)

    elif message.text == internet[lang]:
        bot.send_message(chat_id, text[lang], reply_markup=accaunt(lang, instagram_link, youtube_link, telegram_link))

    elif message.text == founder[lang]:
        bot.send_photo(chat_id, photo2, about_me[lang], reply_markup=perehodlar())
        bot.send_message(chat_id, category[lang], reply_markup=menu_keyboards(lang))
        time.sleep(2)
        bot.register_next_step_handler(message, menu)

    elif message.text == svq[lang]:
        bot.send_message(chat_id, name[lang])
        bot.register_next_step_handler(message, user_email)

    elif message.text == orqaga[lang]:
        return start(message)

    else:
        bot.send_message(chat_id, "Kechirasiz, men bu buyruqni tushunmadim.")
        bot.register_next_step_handler(message, menu)


#--------------------------------freelancerlik---------------------------------

def freelance_cat(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    if message.text == fronted[lang]:
        bot.send_message(chat_id, name[lang])
        bot.register_next_step_handler(message, freelancer_user_email)

    elif message.text == backend[lang]:
        bot.send_message(chat_id, name[lang])
        bot.register_next_step_handler(message, freelancer_user_email)

    elif message.text == design[lang]:
        bot.send_message(chat_id, name[lang])
        bot.register_next_step_handler(message, freelancer_user_email)

    elif message.text == other[lang]:
        bot.send_message(chat_id, name[lang])
        bot.register_next_step_handler(message, freelancer_user_email)

    elif message.text == orqaga[lang]:
        bot.send_message(chat_id, back_menu[lang], reply_markup=menu_keyboards(lang))
        bot.register_next_step_handler(message, menu)


def freelancer_user_email(message):
    fio = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, users_email[lang])
    bot.register_next_step_handler(message, freelancer_email,fio)

def freelancer_email(message, fio):
    emaill = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    if "@" in emaill:
        bot.send_message(chat_id, proffesion[lang])
        bot.register_next_step_handler(message, user_phone, fio, emaill)

    else:
        bot.send_message(chat_id, mistake[lang])
        time.sleep(1)
        bot.send_message(chat_id, users_email[lang])
        bot.register_next_step_handler(message, user_phone, fio)

def user_phone(message, fio, emaill):
    profi = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, number[lang], reply_markup=contact(lang))
    bot.register_next_step_handler(message, send_group_message, fio, profi, emaill)

def send_group_message(message, fio, profi, email):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    if message.text:
        phone = message.text
        employees_details['fio'] = fio
        employees_details['email'] = email
        employees_details['profi'] = profi
        employees_details['phone'] = phone
        bot.send_message(chat_id, f"{confirm_lang[lang]}: {fio}\n"
                                  f"{confirm_email[lang]} {email}\n"
                                  f"{profession[lang]} {profi}\n"
                                  f"{phone_number[lang]} {phone}", reply_markup=commit(lang))


    elif message.contact:
        phone = message.contact.phone_number
        employees_details['fio'] = fio
        employees_details['email'] = email
        employees_details['profi'] = profi
        employees_details['phone'] = phone
        bot.send_message(chat_id, f"{confirm_lang[lang]} {fio}\n"
                                  f"{confirm_email[lang]} {email}\n"
                                  f"{profession[lang]} {profi}\n"
                                  f"{phone_number[lang]} {phone}", reply_markup=commit(lang))


@bot.callback_query_handler(func=lambda call: call.data in ["yes", "no"])
def callback_handler(call):
    chat_id = call.message.chat.id
    lang = user_langs.get(chat_id, "uz")

    fio = employees_details['fio']
    email = employees_details['email']
    profi = employees_details['profi']
    phone = employees_details['phone']

    if call.data == "yes":
        employee_db = Employees_db()  # Employees_db sinfidin bir nusxa yaratamiz
        employee_db.create_table()  # Jadvalni yaratamiz

        if employee_db.check_chat_id_exists(chat_id):
            employee_db.update_data(chat_id, fio, email, profi, phone)  # Ma'lumotlarni yangilaymiz
            bot.send_message(chat_id, update[lang])

        else:
            username = call.message.from_user.username  # Foydalanuvchi nomini olish
            bot.send_message(chat_id, contacted[lang])
            bot.send_message(owner_id, f"Bizda yangi freelancer bor @{username}\n"
                                       f"{new_worker[lang]}\n"
                                       f"{your_name[lang]} {fio}\n"
                                       f"{your_email[lang]} {email}\n"
                                       f"{your_profession[lang]} {profi}\n"
                                       f"{phone_number[lang]} {phone}"
                                       f" unga dostup berasizmi",
                             reply_markup=owner_permission())
            bot.register_next_step_handler(call.message, permission_for_user)
            print(206)

        bot_user = bot.send_message(chat_id, category[lang], reply_markup=menu_keyboards(lang))
        bot.register_next_step_handler(bot_user, menu)


    elif call.data == "no":
        bot.send_message(chat_id, category[lang], reply_markup=request_keyboards(lang))
        bot.register_next_step_handler(call.message, freelance_cat)

def permission_for_user(call):
    print(217)
    chat_id = call.message.chat.id
    lang = user_langs.get(chat_id, "uz")

    if call.data == "yes":
        print(222)
        user_select = bot.send_message(chat_id, f"{access_granted[lang]}", reply_markup=request_keyboards(lang))
        bot.send_message(owner_id, f"qoshildi")
        bot.register_next_step_handler(user_select, send_group_message)


    elif call.data == "no":
        print(229)
        bot.send_message(chat_id, f"{permissions[lang]}", reply_markup=menu_keyboards(lang))
        bot.register_next_step_handler(call.message, menu)




#-------------------------------tg-guruhga-jonatish----------------------------------

def user_email(message):
    fio = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, users_email[lang])
    bot.register_next_step_handler(message, user_question, fio)

def user_question(message, fio):
    email = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    if "@" in email:
        bot.send_message(chat_id, questions[lang])
        bot.register_next_step_handler(message, send_group_message2, fio, email)

    else:
        bot.send_message(chat_id, mistake[lang])
        time.sleep(1)
        bot.send_message(chat_id, users_email[lang])
        bot.register_next_step_handler(message, user_question, fio)

def send_group_message2(message, fio, email):
    quest = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    personal_details['fio'] = fio
    personal_details['email'] = email
    personal_details['quest'] = quest

    bot.send_message(chat_id, f"{confirm_lang[lang]}  {fio}\n"
                              f"{confirm_email[lang]} {email}\n"
                              f"{question[lang]} {quest}", reply_markup=commit_reply(lang))
    bot.register_next_step_handler(message, message_commit)


def message_commit(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    fio = personal_details['fio']
    email = personal_details['email']
    quest = personal_details['quest']

    if message.text == yes_commit[lang]:
        bot.send_message(chat_id, take_info[lang])
        bot.send_message(canal_id, f"{send[lang]} {fio} tomonidan\n"
                                   f"{send_email[lang]} {email}\n"
                                   f"{savol[lang]} {quest}\n")

        time.sleep(1)
        bot.send_message(chat_id, category[lang], reply_markup=menu_keyboards(lang))
        bot.register_next_step_handler(message, menu)

    elif message.text == no_commit[lang]:
        bot.send_message(chat_id, name[lang])
        bot.send_message(chat_id, category[lang], reply_markup=menu_keyboards(lang))
        bot.register_next_step_handler(message, menu)

#--------------------------------------Zakas--------------------------------------

def request_shart(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    if message.text == fronted[lang]:
        bot.send_message(chat_id, name[lang])
        bot.register_next_step_handler(message, request)

    elif message.text == backend[lang]:
        bot.send_message(chat_id, name[lang])
        bot.register_next_step_handler(message, request)

    elif message.text == design[lang]:
        bot.send_message(chat_id, name[lang])
        bot.register_next_step_handler(message, request)

    elif message.text == other[lang]:
        bot.send_message(chat_id, name[lang])
        bot.register_next_step_handler(message, request)

    elif message.text == orqaga[lang]:
        bot.send_message(chat_id, back_menu[lang], reply_markup=menu_keyboards(lang))
        bot.register_next_step_handler(message, menu)


def request(message):
    fio = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, users_email[lang])
    bot.register_next_step_handler(message, request_email, fio)


def request_email(message, fio):
    email3 = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    if "@" in email3:
        bot.send_message(chat_id, order[lang])
        bot.register_next_step_handler(message, request_phone, fio, email3)

    else:
        bot.send_message(chat_id, mistake[lang])
        time.sleep(1)
        bot.send_message(chat_id, users_email[lang])
        bot.register_next_step_handler(message, request_email, fio)


def request_phone(message, fio, email3):
    quest = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, number[lang], reply_markup=contact(lang))
    bot.register_next_step_handler(message, send_group_message3, fio, quest, email3)


def send_group_message3(message, fio, quest, email3):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    if message.text:
        phone = message.text
        request_details['fio'] = fio
        request_details['email'] = email3
        request_details['quest'] = quest
        request_details['phone'] = phone
        bot.send_message(chat_id, f"{confirm_lang[lang]} {fio}\n"
                                  f"{confirm_email[lang]} {email3}\n"
                                  f"{profession[lang]} {quest}\n"
                                  f"{phone_number[lang]} {phone}", reply_markup=commit_reply(lang))
        bot.register_next_step_handler(message, request_handler)

    elif message.contact:
        phone = message.contact.phone_number
        request_details['fio'] = fio
        request_details['email'] = email3
        request_details['quest'] = quest
        request_details['phone'] = phone
        bot.send_message(chat_id, f"{confirm_lang[lang]} {fio}\n"
                                  f"{confirm_email[lang]} {email3}\n"
                                  f"{profession[lang]} {quest}\n"
                                  f"{phone_number[lang]} {phone}", reply_markup=commit_reply(lang))
        bot.register_next_step_handler(message, request_handler)


def request_handler(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    fio = request_details['fio']
    email = request_details['email']
    quest = request_details['quest']
    phone = request_details['phone']

    if message.text == yes_commit[lang]:
        bot.send_message(chat_id, take_info[lang])
        bot.send_message(canal_id, f"{new_order[lang]}"
                                           f"{your_name[lang]} {fio}\n"
                                           f"{your_email[lang]}{email}\n"
                                           f"{orderi[lang]} {quest}\n"
                                           f"{your_phone[lang]} {phone}")

        time.sleep(1)
        bot.send_message(chat_id, category[lang], reply_markup=menu_keyboards(lang))
        bot.register_next_step_handler(message, menu)

    elif message.text == no_commit[lang]:
        bot.send_message(chat_id, category[lang], reply_markup=request_keyboards(lang))
        bot.register_next_step_handler(message, request_shart)

#----------------------------------------------------------------------------

@bot.callback_query_handler(func=lambda call: call.data == "orqaga")
def handle_back(call):
    chat_id = call.message.chat.id
    lang = user_langs.get(chat_id, "uz")
    bot.send_message(call.message.chat.id, back_menu[lang], reply_markup=menu_keyboards(lang))

#----------------------------------------------------------------------------

def back(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, category[lang], reply_markup=menu_keyboards(lang))
    bot.register_next_step_handler(message, menu)

bot.polling(non_stop=True)
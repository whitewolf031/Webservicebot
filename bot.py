import time
# import os
import json
from telebot import TeleBot
from db.employees_db import *
from db.user_id import *
from keyboards import *
from localisation.lang import *
from dotenv import load_dotenv
# from flask import Flask, request

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
pending_freelancers = []
current_page = {}
#----------------------------------------------------------------
# app = Flask(__name__)


# @app.route('/webhook', methods=['POST'])
# def webhook():
#     update = telegram.update.Update.de_json(request.get_json(force=True), bot)
#     chat_id = update.message.chat.id
#     bot.send_message(chat_id=chat_id, text="Salom! Men ishlayapman 🚀")
#     return 'OK', 200
#
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=8000)
#----------------------------------------------------------------

@bot.message_handler(func=lambda message: True)
def testing(message):
    if message.text == '/start':
        return start(message)

    if message.text == '/admin':
        return admin(message)

#---------------------------------Admin panel--------------------------------------
# Adminlarning ID ro'yxati
ADMIN_FILE = "admin_list.json"


# 📌 Adminlar ro‘yxatini JSON fayldan yuklash
def load_admins():
    try:
        with open(ADMIN_FILE, "r") as file:
            data = json.load(file)
            return data.get("admins", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# 📌 Adminlar ro‘yxatini JSON faylga yozish
def save_admins(admins):
    with open(ADMIN_FILE, "w") as file:
        json.dump({"admins": admins}, file, indent=4)


# 📌 Admin qo‘shish
def add_admin(admin_id, username):
    admins = load_admins()

    # Agar admin allaqachon bor bo‘lsa, qo‘shmaymiz
    for admin in admins:
        if admin["id"] == admin_id:
            return False

    admins.append({"id": admin_id, "username": username})
    save_admins(admins)
    return True


# 📌 Adminni o‘chirish
def remove_admin(admin_id):
    admins = load_admins()
    updated_admins = [admin for admin in admins if admin["id"] != admin_id]

    if len(updated_admins) == len(admins):
        return False

    save_admins(updated_admins)
    return True


# 📌 Foydalanuvchi admin ekanligini tekshirish
def is_admin(user_id):
    return any(admin["id"] == user_id for admin in load_admins())

# 📌 Adminlarni ko‘rish
@bot.message_handler(commands=["admin"])
def admin(message):
    chat_id = message.chat.id
    if is_admin(chat_id):
        bot.send_message(chat_id, "Admin panelga xush kelibsiz!", reply_markup=admin_panel_markup())
        bot.register_next_step_handler(message, handle_admin_panel)
    else:
        bot.send_message(chat_id, "⛔ Siz admin emassiz!")


# 📌 Admin panel ishlashi
@bot.message_handler(func=lambda message: is_admin(message.chat.id))
def handle_admin_panel(message):
    chat_id = message.chat.id

    if message.text == "Yangilik qo'shish":
        create_news = bot.send_message(chat_id, "Yangilikni yuboring (matn yoki rasm bilan)")
        bot.register_next_step_handler(create_news, send_announcement)

    elif message.text == "Adminlar ro'yxati":
        admins = load_admins()
        if admins:
            admin_list = "\n".join([f"🆔 {admin['id']} - @{admin['username']}" for admin in admins])
            bot.send_message(chat_id, f"👥 Adminlar ro'yxati:\n{admin_list}")
        else:
            bot.send_message(chat_id, "👥 Hozircha adminlar yo‘q.")
        bot.register_next_step_handler(message, handle_admin_panel)

    elif message.text == "Admin qo'shish":
        bot.send_message(chat_id, "bu bo'lim hozircha ishlamaydi")
        bot.send_message(chat_id, "Bo'limlardan birini tanlang")
        bot.register_next_step_handler(message, handle_admin_panel)
        # bot.send_message(chat_id, "Foydalanuvchi ID sini va username ni kiriting: (masalan: 123456789 admin1)")
        # bot.register_next_step_handler(message, add_admin_handler)

    elif message.text == "Admin o'chirish":
        bot.send_message(chat_id, "Bu bo'lim hozircha ishlamayapdi")
        bot.send_message(chat_id, "Bo'limlardan birini tanlang")
        bot.register_next_step_handler(message, handle_admin_panel)

    elif message.text == "orqaga":
        bot.send_message(chat_id, "Bo‘limlardan birini tanlang", reply_markup=admin_panel_markup())
        bot.register_next_step_handler(message, handle_admin_panel)


# 📌 Admin qo‘shish (Bot orqali)
@bot.message_handler(commands=["add_admin"])
def add_admin_handler(message):
    chat_id = message.chat.id
    if is_admin(chat_id):
        try:
            _, new_admin_id, username = message.text.split()
            new_admin_id = int(new_admin_id)
            if add_admin(new_admin_id, username):
                bot.send_message(chat_id, f"✅ @{username} (ID: {new_admin_id}) admin qilib qo‘shildi.")
            else:
                bot.send_message(chat_id, f"⚠️ @{username} allaqachon admin.")
        except:
            bot.send_message(chat_id, "❌ Xato! To‘g‘ri format: /add_admin 123456789 admin1")
    else:
        bot.send_message(chat_id, "⛔ Sizda bunday huquq yo‘q!")


# 📌 Adminni o‘chirish
@bot.message_handler(commands=["remove_admin"])
def remove_admin_handler(message):
    chat_id = message.chat.id
    if is_admin(chat_id):
        try:
            _, admin_id_to_remove = message.text.split()
            admin_id_to_remove = int(admin_id_to_remove)
            if remove_admin(admin_id_to_remove):
                bot.send_message(chat_id, f"✅ Admin (ID: {admin_id_to_remove}) o‘chirildi.")
            else:
                bot.send_message(chat_id, "⚠️ Bunday admin topilmadi.")
        except:
            bot.send_message(chat_id, "❌ Xato! To‘g‘ri format: /remove_admin 123456789")
    else:
        bot.send_message(chat_id, "⛔ Sizda bunday huquq yo‘q!")


# 📌 Yangilik yuborish
@bot.message_handler(content_types=["photo", "text"])
def send_announcement(message):
    chat_id = message.chat.id
    if is_admin(chat_id):
        users = db.get_all_users()

        if message.content_type == "photo":
            photo_id = message.photo[-1].file_id
            caption = message.caption if message.caption else "📢 Yangilik!"
            for user_id in users:
                try:
                    bot.send_photo(user_id, photo_id, caption=caption)
                except Exception as e:
                    print(f"Xatolik {user_id} ga yuborishda: {e}")
            bot.send_message(chat_id, "📸 Rasmli yangilik muvaffaqiyatli yuborildi!")
            
        elif message.content_type == "text":
            news_text = message.text
            for user_id in users:
                try:
                    bot.send_message(user_id, news_text)
                except Exception as e:
                    print(f"Xatolik {user_id} ga yuborishda: {e}")
            bot.send_message(chat_id, "✉️ Textli yangilik muvaffaqiyatli yuborildi!")
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
        bot.send_message(chat_id, category[lang], reply_markup=update_or_create(lang))
        bot.register_next_step_handler(message, date_update_create)

    elif message.text == zakaz[lang]:
        bot.send_message(chat_id, choose[lang], reply_markup=request_keyboards(lang))
        bot.register_next_step_handler(message, request_shart)

    elif message.text == internet[lang]:
        bot.send_message(chat_id, text[lang], reply_markup=accaunt(lang, instagram_link, youtube_link, telegram_link))

    elif message.text == founder[lang]:
        bot.send_photo(chat_id, photo2, about_me[lang], reply_markup=generate_back(lang))
        bot.register_next_step_handler(message, back)

    elif message.text == svq[lang]:
        bot.send_message(chat_id, name[lang])
        bot.register_next_step_handler(message, user_email)

    elif message.text == orqaga[lang]:
        return start(message)

    else:
        bot.send_message(chat_id, "Kechirasiz, men bu buyruqni tushunmadim.")
        bot.register_next_step_handler(message, menu)


#--------------------------------data update---------------------------------

def date_update_create(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    if message.text == update_info[lang]:
        employee_db = Employees_db()
        employee_db.create_table()

        if employee_db.check_chat_id_exists(chat_id):
            msg = bot.send_message(chat_id, name[lang])
            bot.register_next_step_handler(msg, update_user_email)

        else:
            msg = bot.send_message(chat_id, category[lang], reply_markup=menu_keyboards(lang))
            bot.register_next_step_handler(msg, menu)

    elif message.text == create[lang]:
        employee_db = Employees_db()
        employee_db.create_table()

        if employee_db.check_chat_id_exists(chat_id):
            bot.send_message(chat_id, "Sizning ma'lumotlaringiz mavjud")
            msg = bot.send_message(chat_id, category[lang], reply_markup=menu_keyboards(lang))
            bot.register_next_step_handler(msg, menu)

        else:
            msg = bot.send_message(chat_id, category[lang], reply_markup=request_keyboards(lang))
            bot.register_next_step_handler(msg, freelance_cat)

    elif message.text == orqaga[lang]:
        msg = bot.send_message(chat_id, category[lang], reply_markup=menu_keyboards(lang))
        bot.register_next_step_handler(msg, menu)

    else:
        bot.send_message(chat_id, "Noto‘g‘ri buyruq! Qaytadan urinib ko‘ring.")

def update_user_email(message):
    fio = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, users_email[lang])
    bot.register_next_step_handler(message, update_email,fio)

def update_email(message, fio):
    emaill = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    if "@" in emaill:
        bot.send_message(chat_id, proffesion[lang])
        bot.register_next_step_handler(message, update_user_phone, fio, emaill)

    else:
        bot.send_message(chat_id, mistake[lang])
        time.sleep(1)
        bot.send_message(chat_id, users_email[lang])
        bot.register_next_step_handler(message, update_user_phone, fio)

def update_user_phone(message, fio, emaill):
    profi = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, number[lang], reply_markup=contact(lang))
    bot.register_next_step_handler(message, update_send_group_message, fio, profi, emaill)

def update_send_group_message(message, fio, profi, email):
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
        employee_db = Employees_db()
        employee_db.create_table()

        #ma'lumotlar yangilash
        employee_db.check_chat_id_exists(chat_id)
        employee_db.update_data(chat_id, fio, email, profi, phone)
        bot.send_message(chat_id, update[lang])

        bot_user = bot.send_message(chat_id, category[lang], reply_markup=menu_keyboards(lang))
        bot.register_next_step_handler(bot_user, menu)

    elif call.data == "no":
        bot.send_message(chat_id, category[lang], reply_markup=request_keyboards(lang))
        bot.register_next_step_handler(call.message, update_user_email)

#-------------------------------freelancerlik------------------------------------------

def freelance_cat(message):
    print(287)
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
    print(313)
    fio = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, users_email[lang])
    bot.register_next_step_handler(message, freelancer_email, fio)


def freelancer_email(message, fio):
    print(323)
    emaill = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    if "@" in emaill:
        bot.send_message(chat_id, proffesion[lang])
        bot.register_next_step_handler(message, freelancer_user_phone, fio, emaill)

    else:
        bot.send_message(chat_id, mistake[lang])
        time.sleep(1)
        bot.send_message(chat_id, users_email[lang])
        bot.register_next_step_handler(message, freelancer_user_phone, fio)


def freelancer_user_phone(message, fio, emaill):
    print(340)
    profi = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, number[lang], reply_markup=contact(lang))
    bot.register_next_step_handler(message, freelancer_send_group_message, fio, profi, emaill)


def freelancer_send_group_message(message, fio, profi, email):
    print(350)
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
                                  f"{phone_number[lang]} {phone}", reply_markup=create_user_date())
        bot.register_next_step_handler(message, freelancer_callback_handler)
        print("hello")

    elif message.contact:
        phone = message.contact.phone_number
        employees_details['fio'] = fio
        employees_details['email'] = email
        employees_details['profi'] = profi
        employees_details['phone'] = phone
        bot.send_message(chat_id, f"{confirm_lang[lang]} {fio}\n"
                                  f"{confirm_email[lang]} {email}\n"
                                  f"{profession[lang]} {profi}\n"
                                  f"{phone_number[lang]} {phone}", reply_markup=create_user_date())
        bot.register_next_step_handler(message, freelancer_callback_handler)
        print("hello2")

def freelancer_callback_handler(message):
    print(374)
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    fio = employees_details['fio']
    email = employees_details['email']
    profi = employees_details['profi']
    phone = employees_details['phone']

    if message.text == "Ha":
        username = message.from_user.username
        bot.send_message(chat_id, contacted[lang])
        pending_freelancers.append(chat_id)
        bot.send_message(owner_id, f"Bizda yangi freelancer bor @{username}\n"
                                                f"{new_worker[lang]}\n"
                                                f"{your_name[lang]} {fio}\n"
                                                f"{your_email[lang]} {email}\n"
                                                f"{your_profession[lang]} {profi}\n"
                                                f"{phone_number[lang]} {phone}",
                                      reply_markup=owner_permission())
        print(394)

        bot_user = bot.send_message(chat_id, category[lang], reply_markup=menu_keyboards(lang))
        bot.register_next_step_handler(bot_user, menu)

    elif message.text == "Yo'q":
        cmd = bot.send_message(chat_id, category[lang], reply_markup=request_keyboards(lang))
        bot.register_next_step_handler(cmd, freelance_cat)

#------------------------------------permission------------------------------------

@bot.callback_query_handler(func=lambda call: call.data in ["Albatda", "To'g'ri kelmaydi"])
def permission_for_user(call):
    employee_db = Employees_db()
    employee_db.create_table()
    lang = user_langs.get(owner_id, "uz")

    fio = employees_details["fio"]
    email = employees_details["email"]
    profi = employees_details["profi"]
    phone = employees_details["phone"]

    if not pending_freelancers:
        bot.send_message(owner_id, "Hozirda hech qanday freelancer kutilmayapti.")
        return

    # ✅ Ro‘yxatdan eng birinchi freelancerni olish
    freelancer_id = pending_freelancers.pop(0)


    if call.data == "Albatda":
        bot.send_message(freelancer_id, f"{access_granted[lang]}", reply_markup=menu_keyboards(lang))
        employee_db.insert_data(freelancer_id, fio, email, profi, phone)
        mn = bot.send_message(owner_id, f"Yangi freelancer qo'shildi")
        bot.register_next_step_handler(call.message, menu)
        bot.register_next_step_handler(mn, menu)

    elif call.data == "To'g'ri kelmaydi":
        mn = bot.send_message(owner_id, f"freelancerga ruxsat berilmadi", reply_markup=menu_keyboards(lang))
        bot.send_message(freelancer_id, f"{permissions[lang]}", reply_markup=menu_keyboards(lang))
        bot.register_next_step_handler(call.message, menu)
        bot.register_next_step_handler(mn, menu)

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

#------------------------------------perehodlar-----------------------------------
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith("page_"))
# def change_page(call):
#     chat_id = call.message.chat.id
#     page_number = int(call.data.split("_")[1])
#     current_page[chat_id] = page_number
#     bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
#                           text=f"Siz {page_number}-sahifadasiz.", reply_markup=perehodlar())
#
# @bot.callback_query_handler(func=lambda call: call.data in ["prev", "next"])
# def navigate(call):
#     chat_id = call.message.chat.id
#     if call.data == "prev":
#         if current_page[chat_id] > 1:
#             current_page[chat_id] -= 1
#     elif call.data == "next":
#         if current_page[chat_id] < 3:
#             current_page[chat_id] += 1
#
#     bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
#                           text=f"Siz {current_page[chat_id]}-sahifadasiz.", reply_markup=perehodlar())
#
# @bot.callback_query_handler(func=lambda call: call.data == "menu")
# def back_to_menu(call):
#     chat_id = call.message.chat.id
#     bot.register_next_step_handler(chat_id, category[lang], )

#------------------------------------handle_back----------------------------------

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
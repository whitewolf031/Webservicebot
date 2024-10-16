import time
import os
from telebot import TeleBot
from keyboards import *
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

bot = TeleBot(token)

canal_id = os.getenv("CANAL_ID")
employees_details = {}
personal_details = {}



@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    bot.send_message(chat_id, f"Assalomu aleykum {first_name} web xizmatlar botimizga xush kelibsiz.", reply_markup=generate_language())

@bot.callback_query_handler(func=lambda call: call.data in ["uz","eng","ru"])
def Language(call):
    chat_id = call.message.chat.id
    if call.data == "uz":
        bot.send_message(chat_id, "uz")

    elif call.data == "eng":
        bot.send_message(chat_id, "eng")

    elif call.data == "ru":
        bot.send_message(chat_id, "ru")

    bot.send_message(chat_id, "Bo'limlardan birini tanlang", reply_markup=menu_keyboards())
    bot.register_next_step_handler(call.message, menu)


def menu(message):
    chat_id = message.chat.id
    photo = open("media/img1.jpg", "rb")
    if message.text == "biz haqimizda":
        bot.send_photo(chat_id, photo, caption="Biz it boyicha xizmatlarni yo'lga qo'ygan yosh it jamoamiz",
                        parse_mode="HTML", reply_markup=generate_back())
        bot.register_next_step_handler(message, back)


    elif message.text == "freelancerlik":
        bot.send_message(chat_id, "Freelancerlik bo'yicha ismingizni kiriting:")
        bot.register_next_step_handler(message, freelancer_user_email)


    elif message.text == "Zakaz":
        bot.send_message(chat_id, "Zakaz berish uchun @marguba7913")
        bot.register_next_step_handler(message, back)

    elif message.text == "ijtimoiy tarmoqlar":
        bot.send_message(chat_id, "bizning ijtimoiy tarmoq saxifalari", reply_markup=accaunt())

    elif message.text == "Loyiha asoschi haqida":
        bot.send_message(chat_id, "Loyiha asoschisi men")

    elif message.text == "Savol/takliflar":
        bot.register_next_step_handler(message, user_email)

    elif message.text == "Orqaga":
        return start(message)


# def freelancerlik(message):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, "Ismingizni to'liq yozing:")

#--------------------------------freelancerlik---------------------------------
def freelancer_user_email(message):
    fio = message.text
    chat_id = message.chat.id
    # lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, "elektron pochtangizni jonating")
    bot.register_next_step_handler(message, freelancer_email,fio)

def freelancer_email(message, fio):
    emaill = message.text
    chat_id = message.chat.id

    if "@" in emaill:
        bot.send_message(chat_id, "Yonalishingiz")
        bot.register_next_step_handler(message, user_phone, fio, emaill)

    else:
        bot.send_message(chat_id, "Elektron pochtangiz xato")
        time.sleep(1)
        bot.send_message(chat_id, "elektron pochtangizni kiriting")
        bot.register_next_step_handler(message, user_phone, fio)

def user_phone(message, fio, emaill):
    quest = message.text
    chat_id = message.chat.id
    # lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, "Telefon raqamingizni kiritng", reply_markup=contact())
    bot.register_next_step_handler(message, send_group_message, fio, quest, emaill)

def send_group_message(message, fio, quest, email):
    chat_id = message.chat.id
    # lang = user_langs.get(chat_id, "uz")

    if message.text:
        phone = message.text
        employees_details['fio'] = fio
        employees_details['email'] = email
        employees_details['quest'] = quest
        employees_details['phone'] = phone
        bot.send_message(chat_id, f"Tasdiqlaysizmi: {fio}\n"
                                  f"Elektron pochtangiz: {email}\n"
                                  f"Yo'nalishingiz: {quest}\n"
                                  f"telefon raqamingiz: {phone}", reply_markup=commit())

    elif message.contact:
        phone = message.contact.phone_number
        employees_details['fio'] = fio
        employees_details['email'] = email
        employees_details['quest'] = quest
        employees_details['phone'] = phone
        bot.send_message(chat_id, f"tasdiqlaysizmi: {fio}\n"
                                  f"Elektron pochtangiz: {email}\n"
                                  f"Yo'nalishingiz: {quest}\n"
                                  f"telefon raqamingiz: {phone}", reply_markup=commit())



@bot.callback_query_handler(func=lambda call: call.data in ["yes", "no"])
def message_commit(call):
    chat_id = call.message.chat.id
    fio = employees_details['fio']
    email = employees_details['email']
    quest = employees_details['quest']
    phone = employees_details['phone']

    if call.data == 'yes':
        # Foydalanuvchiga xabar yuborish
        bot.send_message(chat_id, "Ma'lumotlar qabul qilindi!")

        # Ma'lumotlarni Telegram guruhiga yuborish
        bot.send_message(canal_id, f"Jo'natildi: {fio}\n"
                                   f"Elektron pochtangiz: {email}\n"
                                   f"Yo'nalishingiz: {quest}\n"
                                   f"Telefon raqamingiz: {phone}")

        time.sleep(3)
        bot.send_message(chat_id, "Bo'limni tanlang", reply_markup=menu_keyboards())
        bot.register_next_step_handler(call.message, menu)

    elif call.data == "no":
        bot.send_message(chat_id, "Ismingizni kiriting:")
        bot.register_next_step_handler(call.message, freelancer_user_email)



#-------------------------------tg-guruhga-jonatish----------------------------------

def user_email(message):
    fio = message.text
    chat_id = message.chat.id

    bot.send_message(chat_id, "Elektron pochtangizni yuboring")
    bot.register_next_step_handler(message, user_question, fio)

def user_question(message, fio):
    email = message.text
    chat_id = message.chat.id

    if "@" in email:
        bot.send_message(chat_id, "savol yo taklifingizni yuboring")
        bot.register_next_step_handler(message, send_group_message2, fio, email)

    else:
        bot.send_message(chat_id, "email xato")
        time.sleep(1)
        bot.send_message(chat_id, "elektron pochtangizni yuboring")
        bot.register_next_step_handler(message, user_question, fio)

def send_group_message2(message, fio, quest, email):
    chat_id = message.chat.id
    # lang = user_langs.get(chat_id, "uz")

    personal_details['fio'] = fio
    personal_details['email'] = email
    personal_details['quest'] = quest

    bot.send_message(chat_id, f"tasdiqlaysizmi:  {fio}\n"
                              f"Elektron pochtangiz: {email}\n"
                              f"telefon raqamingiz: {quest}", reply_markup=commit())



def back(message):
    chat_id = message.chat.id
    # lang = user_langs.get(chat_id, "uz")
    if message.text == "Orqaga":
        bot.send_message(chat_id, "Quyidagilarni birini tanlang", reply_markup=menu_keyboards())

        bot.register_next_step_handler(message, menu)

bot.polling(non_stop=True)
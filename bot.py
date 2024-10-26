import time
import os
from telebot import TeleBot
from keyboards import *
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

bot = TeleBot(token)

canal_id = os.getenv("CANAL_ID")
group_id = os.getenv("GROUP_ID")
employees_details = {}
personal_details = {}
request_details = {}


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
    photo2 = open("media/img2.jpg", "rb")
    if message.text == "biz haqimizda":
        bot.send_photo(chat_id, photo, caption="Biz it boyicha xizmatlarni yo'lga qo'ygan yosh it jamoamiz",
                        parse_mode="HTML", reply_markup=generate_back())
        bot.register_next_step_handler(message, back)


    elif message.text == "freelancerlik":
        bot.send_message(chat_id, "bo'limlardan birini tanlang", reply_markup=request_keyboards())
        bot.register_next_step_handler(message, freelance)


    elif message.text == "Zakaz":
        bot.send_message(chat_id, "Tanlang:", reply_markup=request_keyboards())
        bot.register_next_step_handler(message, request_shart)

    elif message.text == "ijtimoiy tarmoqlar":
        bot.send_message(chat_id, "bizning ijtimoiy tarmoq saxifalari", reply_markup=accaunt())
        bot.send_message(chat_id, "Bo'limlardan birini tanlang", reply_markup=menu_keyboards())
        time.sleep(2)
        bot.register_next_step_handler(message, menu)

    elif message.text == "Loyiha asoschi haqida":
        bot.send_message(chat_id, f"Asoschining Ismi: Ergashev Sardorbek\n"
                        f"Tug'ilgan Yili: 2006\n"
                        f"Ta'lim: Olmaliq Shahar Itech academy da backend dasturchilikni bitirgan\n\n"
                                  
                        f"Tajribasi:"
                        f"2024-2024 - by november - IT Solutions, Backend Dasturchi"
                        f"2024-2025 - ITech Academy, Mentor sifatida\n\n"
                                  
                        f"Loyiha Haqida:"
                        f"Ergashev Sardorbek 'WebServices' IT xizmatlari kanali asoschisi bo'lib, "
                                  f"u internetda xizmat ko'rsatish va texnologiyalarni rivojlantirish maqsadida tashkil etilgan. Loyihaning asosiy maqsadi, "
                                  f"mijozlarga eng so'nggi texnologiyalar va xizmatlar orqali o'z ehtiyojlarini qondirishdir.\n\n"
                        
                        f"Qiziqishlari:"
                        f"Dasturlash"
                        f"Sun'iy intellekt"
                        f"Sayohat qilish"
                        f"Kitob o'qish\n\n"
                                  
                        f"Aloqa:"
                        f"Email: anvar.karimov@example.com"
                        f"Telefon: +998 90 123 45 67"
                        f"Ijtimoiy Tarmoqlar: LinkedIn, Twitter\n\n")

    elif message.text == "Savol/takliflar":
        bot.send_message(chat_id, "Ismingizni kiriting")
        bot.register_next_step_handler(message, user_email)

    elif message.text == "Orqaga":
        return start(message)

#--------------------------------freelancerlik---------------------------------

def freelance(message):
    chat_id = message.chat.id
    if message.text == "Fronted":
        bot.send_message(chat_id, "Ismingiz kiriting")
        bot.register_next_step_handler(message, freelancer_user_email)

    elif message.text == "Backend":
        bot.send_message(chat_id, "Ismingiz kiriting")
        bot.register_next_step_handler(message, freelancer_user_email)

    if message.text == "Grafik dizay":
        bot.send_message(chat_id, "Ismingiz kiriting")
        bot.register_next_step_handler(message, freelancer_user_email)

    if message.text == "Orqaga":
        bot.send_message(chat_id, "Orqaga qaytdingiz. Bo'limni tanlang:", reply_markup=menu_keyboards())
        bot.register_next_step_handler(message, menu)


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
def callback_handler(call):
    chat_id = call.message.chat.id
    fio = employees_details['fio']
    email = employees_details['email']
    quest = employees_details['quest']
    phone = employees_details['phone']

    if call.data == "yes":
        bot.send_message(chat_id, "ma'lumot qabul qilindi")
        bot.send_message(canal_id, f'Yangi freelancer:\n'
                                   f"Ismi {fio}\n"
                                   f"Elektron pochtasi {email}\n"
                                   f"Yo'nalishi {quest}\n"
                                   f"telefon raqami {phone}")

        time.sleep(3)
        bot.send_message(chat_id, "Bo'limlardan birini tanlang", reply_markup=menu_keyboards())
        bot.register_next_step_handler(call.message, menu)



    elif call.data == "no":
        bot.send_message(chat_id, "Bo'limlardan birini tanlang", reply_markup=request_keyboards())
        bot.register_next_step_handler(call.message, freelance)


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

def send_group_message2(message, fio, email):
    quest = message.text
    chat_id = message.chat.id
    # lang = user_langs.get(chat_id, "uz")

    personal_details['fio'] = fio
    personal_details['email'] = email
    personal_details['quest'] = quest

    bot.send_message(chat_id, f"tasdiqlaysizmi:  {fio}\n"
                              f"Elektron pochtangiz: {email}\n"
                              f"Savol/taklifingiz: {quest}", reply_markup=commit_reply())
    bot.register_next_step_handler(message, message_commit)


def message_commit(message):
    chat_id = message.chat.id
    fio = personal_details['fio']
    email = personal_details['email']
    quest = personal_details['quest']

    if message.text == 'yes':
        # Foydalanuvchiga xabar yuborish
        bot.send_message(chat_id, "Ma'lumotlar qabul qilindi!")

        # Ma'lumotlarni Telegram guruhiga yuborish
        bot.send_message(canal_id, f"Jo'natildi: {fio} tomonidan\n"
                                   f"Elektron pochtasi: {email}\n"
                                   f"Savoli: {quest}\n")

        time.sleep(3)
        bot.send_message(chat_id, "Bo'limni tanlang", reply_markup=menu_keyboards())
        bot.register_next_step_handler(message, menu)

    elif message.text == "no":
        bot.send_message(chat_id, "Ismingizni kiriting:")
        bot.register_next_step_handler(message, user_email)

#--------------------------------------Zakas--------------------------------------

def request_shart(message):
    chat_id = message.chat.id

    if message.text == "Fronted":
        bot.send_message(chat_id, "Ismingiz kiriting")
        bot.register_next_step_handler(message, request)

    elif message.text == "Backend":
        bot.send_message(chat_id, "Ismingiz kiriting")
        bot.register_next_step_handler(message, request)

    if message.text == "Grafik dizay":
        bot.send_message(chat_id, "Ismingiz kiriting")
        bot.register_next_step_handler(message, request)

    if message.text == "Orqaga":
        bot.send_message(chat_id, "Orqaga qaytdingiz. Bo'limni tanlang:", reply_markup=menu_keyboards())
        bot.register_next_step_handler(message, menu)


def request(message):
    fio = message.text
    chat_id = message.chat.id
    # lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, "elektron pochtangizni jonating")
    bot.register_next_step_handler(message, request_email, fio)


def request_email(message, fio):
    email3 = message.text
    chat_id = message.chat.id

    if "@" in email3:
        bot.send_message(chat_id, "Qanday turdago zakaz (yozing)")
        bot.register_next_step_handler(message, request_phone, fio, email3)

    else:
        bot.send_message(chat_id, "Elektron pochtangiz xato")
        time.sleep(1)
        bot.send_message(chat_id, "elektron pochtangizni kiriting")
        bot.register_next_step_handler(message, request_phone, fio)


def request_phone(message, fio, email3):
    quest = message.text
    chat_id = message.chat.id
    # lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, "Telefon raqamingizni kiritng", reply_markup=contact())
    bot.register_next_step_handler(message, send_group_message3, fio, quest, email3)


def send_group_message3(message, fio, quest, email3):
    chat_id = message.chat.id
    # lang = user_langs.get(chat_id, "uz")

    if message.text:
        phone = message.text
        request_details['fio'] = fio
        request_details['email'] = email3
        request_details['quest'] = quest
        request_details['phone'] = phone
        bot.send_message(chat_id, f"Tasdiqlaysizmi: {fio}\n"
                                  f"Elektron pochtangiz: {email3}\n"
                                  f"Yo'nalishingiz: {quest}\n"
                                  f"telefon raqamingiz: {phone}", reply_markup=commit_reply())
        bot.register_next_step_handler(message, request_handler)

    elif message.contact:
        phone = message.contact.phone_number
        request_details['fio'] = fio
        request_details['email'] = email3
        request_details['quest'] = quest
        request_details['phone'] = phone
        bot.send_message(chat_id, f"tasdiqlaysizmi: {fio}\n"
                                  f"Elektron pochtangiz: {email3}\n"
                                  f"Yo'nalishingiz: {quest}\n"
                                  f"telefon raqamingiz: {phone}", reply_markup=commit_reply())
        bot.register_next_step_handler(message, request_handler)


def request_handler(message):
    chat_id = message.chat.id
    fio = request_details['fio']
    email = request_details['email']
    quest = request_details['quest']
    phone = request_details['phone']

    if message.text == "yes":
        bot.send_message(chat_id, "ma'lumot qabul qilindi")
        bot.send_message(canal_id, f"Yangi zakaz"
                                           f"Ismi {fio}\n"
                                           f"Elektron pochtasi{email}\n"
                                           f"Zakazi {quest}\n"
                                           f"telefon raqami {phone}")
        time.sleep(3)
        bot.send_message(chat_id, "Bo'limlardan birini tanlang", reply_markup=menu_keyboards())
        bot.register_next_step_handler(message, menu)

    elif message.text == "no":
        bot.send_message(chat_id, "Bo'limlardan birini tanlang", reply_markup=request_keyboards())
        bot.register_next_step_handler(message, request_shart)

#----------------------------------------------------------------------------

def back(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Quyidagilardan birini tanlang:", reply_markup=menu_keyboards())
    bot.register_next_step_handler(message, menu)


bot.polling(non_stop=True)
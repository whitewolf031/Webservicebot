from telebot import types


def generate_language():
    keyboard = types.InlineKeyboardMarkup()
    btn_uz = types.InlineKeyboardButton(text="🇺🇿Uz", callback_data="uz")
    btn_en = types.InlineKeyboardButton(text="🇺🇸En", callback_data="eng")
    btn_ru = types.InlineKeyboardButton(text="🇷🇺Ru", callback_data="ru")
    keyboard.row(btn_uz, btn_en, btn_ru)
    return keyboard

def menu_keyboards():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_about = types.KeyboardButton(text="biz haqimizda")
    btn_job = types.KeyboardButton(text="freelancerlik")
    btn_zakaz = types.KeyboardButton(text="Zakaz")
    btn_inte = types.KeyboardButton(text="ijtimoiy tarmoqlar")
    btn_about_me = types.KeyboardButton(text="Loyiha asoschi haqida")
    btn_questions = types.KeyboardButton(text="Savol/takliflar")
    btn_back = types.KeyboardButton(text="Orqaga")
    keyboard.row(btn_about, btn_job, btn_zakaz)
    keyboard.row(btn_inte, btn_about_me, btn_questions)
    keyboard.row(btn_back)
    return keyboard


def contact():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = types.KeyboardButton(text="contact share", request_contact=True)
    keyboard.row(btn)
    return keyboard

def commit():
    keyboard = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton(text="yes", callback_data="yes")
    btn_no = types.InlineKeyboardButton(text="no", callback_data="no")
    keyboard.row(btn_yes, btn_no)
    return keyboard

def accaunt():
    keyboard = types.InlineKeyboardMarkup()
    btn_instagram = types.InlineKeyboardButton(text="instagram", callback_data="instagram", url="https://www.youtube.com/")
    btn_youtube = types.InlineKeyboardButton(text="youtube", callback_data="youtube", url="https://www.youtube.com/")
    btn_telegram = types.InlineKeyboardButton(text="telegram", callback_data="telegram", url="https://t.me/webservices01")
    keyboard.row(btn_instagram)
    keyboard.row(btn_youtube)
    keyboard.row(btn_telegram)
    return keyboard

def request_keyboards():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_fronted = types.KeyboardButton(text="Fronted")
    btn_backend = types.KeyboardButton(text="Backend")
    btn_design = types.KeyboardButton(text="Grafik dizay")
    btn_back = types.KeyboardButton(text="Orqaga")
    keyboard.row(btn_fronted)
    keyboard.row(btn_backend)
    keyboard.row(btn_design)
    keyboard.row(btn_back)
    return keyboard

def generate_back():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_back = types.KeyboardButton(text="Orqaga")
    keyboard.row(btn_back)
    return keyboard

def commit_reply():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_yes = types.KeyboardButton(text="yes")
    btn_no = types.KeyboardButton(text="no")
    keyboard.row(btn_yes, btn_no)
    return keyboard

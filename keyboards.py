import os
from telebot import types
from localisation.lang_keyboards import *

instagram_link = os.getenv("INSTAGRAM_URL")
youtube_link = os.getenv("YOUTUBE_URL")
telegram_link = os.getenv("TELEGRAM_URL")


def admin_panel_markup():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_news = types.KeyboardButton("Yangilik qo'shish")
    btn_look = types.KeyboardButton("Bo'limlarni ko'rish")
    btn_admins = types.KeyboardButton("Adminlar ro'yxati")
    btn_add_admin = types.KeyboardButton("Admin qo'shish")
    keyboard.row(btn_news, btn_look)
    keyboard.row(btn_admins, btn_add_admin)
    return keyboard

def generate_language():
    keyboard = types.InlineKeyboardMarkup()
    btn_uz = types.InlineKeyboardButton(text="🇺🇿Uz", callback_data="uz")
    btn_en = types.InlineKeyboardButton(text="🇺🇸En", callback_data="en")
    btn_ru = types.InlineKeyboardButton(text="🇷🇺Ru", callback_data="ru")
    keyboard.row(btn_uz, btn_en, btn_ru)
    return keyboard

def menu_keyboards(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_about = types.KeyboardButton(text=about[lang])
    btn_job = types.KeyboardButton(text=freelancer[lang])
    btn_zakaz = types.KeyboardButton(text=zakaz[lang])
    btn_inte = types.KeyboardButton(text=internet[lang])
    btn_about_me = types.KeyboardButton(text=founder[lang])
    btn_questions = types.KeyboardButton(text=svq[lang])
    btn_back = types.KeyboardButton(text=orqaga[lang])
    keyboard.row(btn_about, btn_job, btn_zakaz)
    keyboard.row(btn_inte, btn_about_me, btn_questions)
    keyboard.row(btn_back)
    return keyboard


def contact(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = types.KeyboardButton(text=contact_number[lang], request_contact=True)
    keyboard.row(btn)
    return keyboard

def commit(lang):
    keyboard = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton(text=yes_commit[lang], callback_data="yes")
    btn_no = types.InlineKeyboardButton(text=no_commit[lang], callback_data="no")
    keyboard.row(btn_yes, btn_no)
    return keyboard

def accaunt(lang, instagram_link, youtube_link, telegram_link):
    keyboard = types.InlineKeyboardMarkup()
    btn_instagram = types.InlineKeyboardButton(text=Instagram[lang], url=instagram_link)
    btn_youtube = types.InlineKeyboardButton(text=youtube[lang], url=youtube_link)
    btn_telegram = types.InlineKeyboardButton(text=telegram[lang], url=telegram_link)
    btn_back = types.InlineKeyboardButton(text=orqaga[lang], callback_data="orqaga")
    keyboard.row(btn_instagram)  # Tugmani bir qatorda qo'shadi
    keyboard.row(btn_youtube)  # Tugmani bir qatorda qo'shadi
    keyboard.row(btn_telegram)  # Tugmani bir qatorda qo'shad
    keyboard.row(btn_back)
    return keyboard


def request_keyboards(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_fronted = types.KeyboardButton(text=fronted[lang])
    btn_backend = types.KeyboardButton(text=backend[lang])
    btn_design = types.KeyboardButton(text=design[lang])
    btn_other = types.KeyboardButton(text=other[lang])
    btn_back = types.KeyboardButton(text=orqaga[lang])
    keyboard.row(btn_fronted)
    keyboard.row(btn_backend)
    keyboard.row(btn_design)
    keyboard.row(btn_other)
    keyboard.row(btn_back)
    return keyboard

def generate_back(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_back = types.KeyboardButton(text=orqaga[lang])
    keyboard.row(btn_back)
    return keyboard

def commit_reply(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_yes = types.KeyboardButton(text=yes_commit[lang])
    btn_no = types.KeyboardButton(text=no_commit[lang])
    keyboard.row(btn_yes, btn_no)
    return keyboard

def owner_permission():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_yes = types.KeyboardButton(text="yes")
    btn_no = types.KeyboardButton(text="no")
    keyboard.row(btn_yes, btn_no)
    return keyboard

def perehodlar():
    keyboard = types.InlineKeyboardMarkup()
    btn_orqaga = types.InlineKeyboardButton(text="⬅️", callback_data="strelka")
    btn_1 = types.InlineKeyboardButton(text="1", callback_data="1")
    btn_2 = types.InlineKeyboardButton(text="2", callback_data="2")
    btn_3 = types.InlineKeyboardButton(text="3", callback_data="3")
    btn_oldinga = types.InlineKeyboardButton(text="➡️", callback_data="orqaga")
    keyboard.row(btn_orqaga, btn_1, btn_2, btn_3, btn_oldinga)
    return keyboard

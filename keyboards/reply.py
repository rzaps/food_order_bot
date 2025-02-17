# ✅ reply.py – кнопки главного меню (/menu, /cart, /order, /feedback)

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from bot import bot

# === Функция создания кнопок главного меню ===
def get_main_menu_buttons():
    """Создает кнопки главного меню"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("/menu"))
    markup.add(KeyboardButton("/cart"))
    markup.add(KeyboardButton("/order"))
    markup.add(KeyboardButton("/feedback"))
    return markup

# === Обработчик команды /start ===
@bot.message_handler(commands=['start'])
def start(message):
    """Отправляет пользователю главное меню"""
    bot.send_message(message.chat.id, "Привет! Выберите действие:", reply_markup=get_main_menu_buttons())

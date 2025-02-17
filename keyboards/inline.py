#Этот файл отвечает за интерактивные кнопки, которые появляются под сообщениями.
# ✅ inline.py – инлайн-кнопки для добавления, удаления и подтверждения заказа


import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot

# === Функция создания инлайн-кнопок для добавления в корзину ===
def get_dish_inline_buttons(dish_id):
    """Создает инлайн-кнопки 'Добавить' и 'Удалить' для блюда"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("➕ Добавить", callback_data=f"add_{dish_id}"))
    markup.add(InlineKeyboardButton("❌ Удалить", callback_data=f"remove_{dish_id}"))
    return markup

# === Кнопка подтверждения заказа ===
def get_order_confirmation_buttons():
    """Создает инлайн-кнопки для подтверждения или отмены заказа"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ Подтвердить заказ", callback_data="confirm_order"))
    markup.add(InlineKeyboardButton("❌ Отменить заказ", callback_data="cancel_order"))
    return markup

# === Обработчик подтверждения заказа ===
@bot.callback_query_handler(func=lambda call: call.data == "confirm_order")
def confirm_order(call):
    """Подтверждение заказа"""
    bot.send_message(call.message.chat.id, "✅ Ваш заказ принят! Спасибо за заказ.")

# === Обработчик отмены заказа ===
@bot.callback_query_handler(func=lambda call: call.data == "cancel_order")
def cancel_order(call):
    """Отмена заказа"""
    bot.send_message(call.message.chat.id, "❌ Ваш заказ отменен.")

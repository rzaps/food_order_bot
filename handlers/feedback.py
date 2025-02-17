# Этот файл отвечает за обработку отзывов пользователей:
# ✅ Оставление отзыва через команду /feedback
# ✅ Сохранение отзывов в базу данных
# ✅ Возможность просмотра отзывов (например, для админов)


import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from database.models import Feedback
from bot_instance import bot

# === Команда /feedback ===
@bot.message_handler(commands=['feedback'])
def ask_for_feedback(bot,message):
    """Запрашивает у пользователя отзыв и сохраняет его"""
    user_id = message.chat.id

    # Создаем клавиатуру с кнопками оценок
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("⭐️ 1"), KeyboardButton("⭐️ 2"), KeyboardButton("⭐️ 3"))
    markup.add(KeyboardButton("⭐️ 4"), KeyboardButton("⭐️ 5"))

    bot.send_message(user_id, "Оцените наш сервис от 1 до 5 ⭐️:", reply_markup=markup)
    bot.register_next_step_handler(message, save_feedback)

# === Сохранение отзыва ===
def save_feedback(message):
    """Сохраняет отзыв в базу данных"""
    user_id = message.chat.id
    rating = message.text.strip()

    # Проверяем, выбрал ли пользователь оценку от 1 до 5
    if rating in ["⭐️ 1", "⭐️ 2", "⭐️ 3", "⭐️ 4", "⭐️ 5"]:
        rating_value = int(rating[2])  # Получаем число из текста (например, "⭐️ 4" -> 4)

        bot.send_message(user_id, "Спасибо! Теперь напишите ваш отзыв текстом:")
        bot.register_next_step_handler(message, save_text_feedback, rating_value)
    else:
        bot.send_message(user_id, "Пожалуйста, выберите оценку от 1 до 5.")
        bot.register_next_step_handler(message, save_feedback)

# === Сохранение текстового отзыва ===
def save_text_feedback(message, rating):
    """Сохраняет текстовый отзыв в базу данных"""
    user_id = message.chat.id
    text_feedback = message.text.strip()

    # Сохраняем в БД
    Feedback.add_feedback(user_id, rating, text_feedback)

    bot.send_message(user_id, "✅ Ваш отзыв сохранен! Спасибо за обратную связь! 🙏")

# === Команда для просмотра отзывов (только для админа) ===
@bot.message_handler(commands=['view_feedback'])
def show_feedback(message):
    """Отображает все отзывы (для администратора)"""
    user_id = message.chat.id

    # Проверяем, является ли пользователь админом (замени ID на реальные)
    if user_id not in [123456789, 987654321]:
        bot.send_message(user_id, "❌ У вас нет доступа к отзывам.")
        return

    feedback_list = Feedback.get_all_feedback()

    if feedback_list:
        feedback_text = "\n\n".join([f"⭐️ {rating}/5 - {text}" for _, rating, text in feedback_list])
        bot.send_message(user_id, f"📢 Отзывы пользователей:\n\n{feedback_text}")
    else:
        bot.send_message(user_id, "Пока нет отзывов.")

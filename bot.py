#Разбор кода:
# Импортируем библиотеки и модули – используем telebot для работы с Telegram API и импортируем токен из config.py.
# Создаем объект бота – bot = telebot.TeleBot(TOKEN).
# Добавляем обработчики команд:
# /start – приветственное сообщение.
# /menu – показывает меню (логика в menu.py).
# /order – управление заказами (логика в order.py).
# /feedback – оставление отзывов (логика в feedback.py).
# Запускаем бота – bot.polling(none_stop=True), что позволяет боту работать непрерывно.


import telebot
from bot_instance import bot
from handlers.menu import show_menu
from handlers.order import place_order
from handlers.feedback import ask_for_feedback


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в сервис заказа еды! Используйте /menu для просмотра меню.")

# Обработчик команды /menu
@bot.message_handler(commands=['menu'])
def menu(message):
    show_menu(bot, message)

# Обработчик команды /order
@bot.message_handler(commands=['order'])
def order(message):
    place_order(bot, message)

# Обработчик команды /feedback
@bot.message_handler(commands=['feedback'])
def feedback(message):
    ask_for_feedback(bot, message)

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)



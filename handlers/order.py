#  Что делает этот файл?
#
# Позволяет пользователю добавлять блюда в корзину.
# Позволяет просмотреть корзину.
# Позволяет оформить заказ.
# Подключается к базе данных для хранения заказов.


# Добавление в корзину (add_to_cart)
#
# Получает ID блюда из нажатой кнопки.
# Проверяет, есть ли это блюдо в БД.
# Добавляет его в словарь user_cart.
# Отправляет уведомление.
# Просмотр корзины (show_cart)
#
# Загружает список блюд в корзине.
# Показывает их пользователю с итоговой суммой.
# Оформление заказа (place_order)
#
# Проверяет, есть ли что-то в корзине.
# Создает заказ в БД.
# Очищает корзину.
#
# Разбор новых функций
# 1️⃣ Добавление блюда в корзину (add_to_cart)
# ✅ Если блюдо уже есть, увеличиваем количество.
# ✅ Если нет – добавляем с количеством 1.
# ✅ Отправляем уведомление с текущим количеством.
#
# 2️⃣ Удаление блюда (remove_from_cart)
# ✅ Если в корзине >1 шт., уменьшаем количество.
# ✅ Если осталась 1 шт., удаляем полностью.
# ✅ Отправляем уведомление об изменении количества.
#
# 3️⃣ Просмотр корзины (show_cart)
# ✅ Показывает список блюд с их количеством.
# ✅ Добавляет кнопки "Удалить" напротив каждого блюда.
# ✅ Показывает итоговую сумму.




import telebot
from database.models import Order, MenuItem, User
from bot_instance import bot

user_cart = {}  # Временное хранилище корзин пользователей (user_id: {dish_name: (price, quantity)})


# === Добавление блюда в корзину ===
@bot.callback_query_handler(func=lambda call: call.data.startswith("add_"))
def add_to_cart(call):
    """Добавляет выбранное блюдо в корзину пользователя или увеличивает количество"""
    user_id = call.message.chat.id
    dish_id = int(call.data.split("_")[1])  # Получаем ID блюда из callback_data

    dish = MenuItem.get_dish_by_id(dish_id)
    if dish:
        name, price, _ = dish
        if user_id not in user_cart:
            user_cart[user_id] = {}

        if name in user_cart[user_id]:
            user_cart[user_id][name] = (
            price, user_cart[user_id][name][1] + 1)  # Увеличиваем количество
        else:
            user_cart[user_id][name] = (
            price, 1)  # Добавляем блюдо с количеством 1

        bot.answer_callback_query(call.id,
                                  f"➕ Добавлено: {name} (в корзине: {user_cart[user_id][name][1]} шт.)")
    else:
        bot.answer_callback_query(call.id, "❌ Ошибка: блюдо не найдено.")


# === Удаление блюда из корзины ===
@bot.callback_query_handler(func=lambda call: call.data.startswith("remove_"))
def remove_from_cart(call):
    """Уменьшает количество блюда в корзине или удаляет его полностью"""
    user_id = call.message.chat.id
    dish_name = call.data.split("_", 1)[1]  # Получаем название блюда

    if user_id in user_cart and dish_name in user_cart[user_id]:
        price, quantity = user_cart[user_id][dish_name]

        if quantity > 1:
            user_cart[user_id][dish_name] = (price, quantity - 1)
            bot.answer_callback_query(call.id,
                                      f"➖ Убрано: {dish_name} (осталось: {quantity - 1} шт.)")
        else:
            del user_cart[user_id][dish_name]
            bot.answer_callback_query(call.id,
                                      f"❌ {dish_name} удалено из корзины")

    else:
        bot.answer_callback_query(call.id,
                                  "❌ Ошибка: блюдо не найдено в корзине.")


# === Просмотр корзины ===
@bot.message_handler(commands=['cart'])
def show_cart(message):
    """Отображает содержимое корзины с кнопками управления"""
    user_id = message.chat.id
    cart_items = user_cart.get(user_id, {})

    if cart_items:
        total_price = sum(
            price * quantity for price, quantity in cart_items.values())
        cart_text = "\n".join(
            [f"{dish} - {price}₽ x {quantity}" for dish, (price, quantity) in
             cart_items.items()])

        # Создаем inline-кнопки для удаления блюд
        markup = telebot.types.InlineKeyboardMarkup()
        for dish in cart_items:
            markup.add(telebot.types.InlineKeyboardButton(f"❌ Удалить {dish}",
                                                          callback_data=f"remove_{dish}"))

        bot.send_message(user_id,
                         f"🛒 Ваша корзина:\n\n{cart_text}\n\n💰 Итого: {total_price}₽",
                         reply_markup=markup)
    else:
        bot.send_message(user_id, "🛒 Ваша корзина пуста.")


# === Оформление заказа ===
@bot.message_handler(commands=['order'])
def place_order(message):
    """Создает заказ и очищает корзину"""
    user_id = message.chat.id
    cart_items = user_cart.get(user_id, {})

    if cart_items:
        total_price = sum(
            price * quantity for price, quantity in cart_items.values())
        item_names = ", ".join([f"{dish} x{quantity}" for dish, (_, quantity) in
                                cart_items.items()])

        user = User.get_user(user_id)
        if user:
            Order.create_order(user[0], item_names,
                               total_price)  # user[0] – ID пользователя в БД
            bot.send_message(user_id,
                             f"✅ Заказ оформлен!\n📦 {item_names}\n💰 Сумма: {total_price}₽")
            user_cart[user_id] = {}  # Очищаем корзину
        else:
            bot.send_message(user_id, "❌ Ошибка: пользователь не найден.")
            print(user)
    else:
        bot.send_message(user_id,
                         "🛒 Ваша корзина пуста. Добавьте блюда перед заказом!")

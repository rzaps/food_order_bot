# Структура базы данных
# База данных хранится в локальном файле database.db и использует SQLite.
#
# Она состоит из 3 основных таблиц:
#
# users – информация о пользователях.
# menu – список доступных блюд.
# orders – заказы пользователей.


# Как база данных подключается в приложении
# Подключение к базе в коде:
#
# В каждом файле, где нужно работать с БД, создаем подключение sqlite3.connect("database.db").
# Создаем cursor для выполнения SQL-запросов.
# После работы закрываем соединение.
# Где хранится база:
#
# database.db хранится в корневой папке проекта.
# Это локальный файл SQLite, который работает без установки отдельного сервера базы данных.


# Вот полный код db.py, который:
#  Создает базу данных database.db, если она не существует.
#  Создает таблицы users, menu, orders.
#  Содержит все необходимые столбцы (включая image_url для картинок блюд).


import sqlite3

# Подключение к базе данных (если файла нет, он создастся автоматически)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# === Создание таблицы пользователей ===
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE NOT NULL,
    name TEXT NOT NULL
)
''')

# === Создание таблицы меню (блюда) ===
cursor.execute('''
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,         -- Название блюда
    category TEXT NOT NULL,     -- Категория блюда (например, Пицца, Суши)
    price REAL NOT NULL,        -- Цена блюда
    image_url TEXT NOT NULL     -- Ссылка на изображение блюда
)
''')

# === Создание таблицы заказов ===
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,   -- ID пользователя, оформившего заказ
    items TEXT NOT NULL,        -- Список блюд (JSON или строка)
    total_price REAL NOT NULL,  -- Итоговая стоимость заказа
    status TEXT DEFAULT 'pending', -- Статус заказа (pending, completed, cancelled)
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("База данных успешно создана!")

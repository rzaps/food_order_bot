import sqlite3
import os

DB_DIR = "database"  # Папка для базы данных
DB_NAME = os.path.join(DB_DIR, "database.db")  # Полный путь к базе данных

# === Проверка и создание папки для базы ===
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)  # Создаем папку, если её нет

# === Функция для создания всех таблиц ===
def create_tables():
    """Создает таблицы, если их нет"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            name TEXT
        )
    ''')

    # Таблица меню
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            price REAL,
            image_url TEXT
        )
    ''')

    # Таблица заказов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            items TEXT,
            total_price REAL,
            status TEXT
        )
    ''')

    # Таблица отзывов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            rating INTEGER,
            text TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Вызываем создание таблиц при запуске
create_tables()

# === Классы для работы с базой данных ===
class User:
    @staticmethod
    def add_user(telegram_id, name):
        """Добавляет нового пользователя в БД"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (telegram_id, name) VALUES (?, ?)", (telegram_id, name))
        conn.commit()
        conn.close()

    @staticmethod
    def get_user(telegram_id):
        """Получает пользователя по Telegram ID"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users WHERE telegram_id = ?", (telegram_id,))
        user = cursor.fetchone()
        conn.close()
        return user  # (id, name) или None

class MenuItem:
    @staticmethod
    def get_categories():
        """Получает список всех уникальных категорий блюд"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM menu")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories

    @staticmethod
    def get_dishes_by_category(category):
        """Получает блюда в указанной категории"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, image_url FROM menu WHERE category = ?", (category,))
        dishes = cursor.fetchall()
        conn.close()
        return dishes  # [(id, name, price, image_url), ...]

    @staticmethod
    def get_dish_by_id(dish_id):
        """Возвращает информацию о блюде по ID"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Запрос на получение блюда по ID
        cursor.execute("SELECT name, price, image_url FROM menu WHERE id = ?",
                       (dish_id,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return result  # Возвращаем данные блюда (name, price, image_url)
        else:
            return None  # Если блюдо не найдено, возвращаем None


class Order:
    @staticmethod
    def create_order(user_id, items, total_price):
        """Создает новый заказ"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (user_id, items, total_price, status) VALUES (?, ?, ?, 'pending')",
                       (user_id, items, total_price))
        conn.commit()
        conn.close()

    @staticmethod
    def get_orders(user_id):
        """Получает все заказы пользователя"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, items, total_price, status FROM orders WHERE user_id = ?", (user_id,))
        orders = cursor.fetchall()
        conn.close()
        return orders  # [(id, items, total_price, status), ...]

    @staticmethod
    def update_status(order_id, new_status):
        """Обновляет статус заказа"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
        conn.commit()
        conn.close()

class Feedback:
    @staticmethod
    def add_feedback(user_id, rating, text):
        """Добавляет новый отзыв в базу"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (user_id, rating, text) VALUES (?, ?, ?)", (user_id, rating, text))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_feedback():
        """Получает все отзывы из базы данных"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, rating, text FROM feedback")
        feedback_list = cursor.fetchall()
        conn.close()
        return feedback_list

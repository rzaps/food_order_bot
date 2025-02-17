import sqlite3
import os

DB_DIR = "database"
DB_NAME = os.path.join(DB_DIR, "database.db")

# Проверка и создание папки для базы данных
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)


# Функция для создания таблиц
def create_tables():
    """Создает таблицы, если их нет"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            price REAL,
            image_url TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Вызываем создание таблиц при запуске
create_tables()

# Подключение к базе данных
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Проверка на наличие данных в таблице menu
cursor.execute("SELECT COUNT(*) FROM menu")
if cursor.fetchone()[0] == 0:  # Если таблица пустая, добавляем тестовые данные
    menu_items = [
        # Пицца
        ("Пицца Маргарита", "Пицца", 550,
         "https://img.freepik.com/free-photo/top-view-pepperoni-pizza-with-mushroom-sausages-bell-pepper-olive-corn-black-wooden_141793-2158.jpg"),
        ("Пицца Пепперони", "Пицца", 600,
         "https://img.freepik.com/free-photo/pepperoni-pizza-close-up-shot-wooden-table_1150-4972.jpg"),
        ("Пицца 4 сыра", "Пицца", 650,
         "https://img.freepik.com/free-photo/four-cheese-pizza-italian-style-close-up_1150-4630.jpg"),

        # Паста
        ("Паста Карбонара", "Паста", 450,
         "https://img.freepik.com/free-photo/spaghetti-carbonara-with-bacon-parmesan-cheese_2829-11244.jpg"),
        ("Паста Болоньезе", "Паста", 480,
         "https://img.freepik.com/free-photo/spaghetti-bolognese-with-tomato-sauce-and-basil-leaves_1150-28478.jpg"),
        ("Паста Песто", "Паста", 500,
         "https://img.freepik.com/free-photo/spaghetti-pesto-dish-green-sauce-italian-cuisine_1150-4253.jpg"),

        # Бургеры
        ("Бургер Чизбургер", "Бургеры", 300,
         "https://img.freepik.com/free-photo/delicious-burger-with-many-ingredients-isolated-white-background-tasty-cheeseburger-sesame-bun_90220-1192.jpg"),
        ("Бургер с беконом", "Бургеры", 350,
         "https://img.freepik.com/free-photo/bacon-cheese-burger-black-background_1150-3373.jpg"),
        ("Вегетарианский бургер", "Бургеры", 400,
         "https://img.freepik.com/free-photo/vegetarian-burger-with-grilled-veggies_1150-4988.jpg"),

        # Суши
        ("Суши Филадельфия", "Суши", 700,
         "https://img.freepik.com/free-photo/sushi-set-with-salmon-rolls_140725-2292.jpg"),
        ("Суши Калифорния", "Суши", 750,
         "https://img.freepik.com/free-photo/canadian-sushi-set-freshly-made_1150-3076.jpg"),
        ("Суши Нигири", "Суши", 650,
         "https://img.freepik.com/free-photo/delicious-japanese-sushi-assortment-black-background_1150-4985.jpg")
    ]

    try:
        cursor.executemany(
            "INSERT INTO menu (name, category, price, image_url) VALUES (?, ?, ?, ?)",
            menu_items)
        conn.commit()
        print("Тестовые данные с изображениями добавлены!")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении данных: {e}")

conn.commit()  # Принудительное сохранение перед закрытием
conn.close()

print(f"База данных используется по пути: {DB_NAME}")

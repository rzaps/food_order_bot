import sqlite3


conn = sqlite3.connect("../database/database.db")
cursor = conn.cursor()

cursor.execute("SELECT name, image_url FROM menu")
rows = cursor.fetchall()

for row in rows:
    print(row)  # Выведет название блюда и ссылку на изображение

conn.close()

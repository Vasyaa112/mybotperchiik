# Підключаємось до бази даних
cnx = mysql.connector.connect(user='ch93f0bb7c_discord', password='g54tg45hGTu6',
                              host='yaris.cityhost.com.ua:3306',
                              database='ch93f0bb7c_discord')

# Отримуємо курсор для виконання запиту
cursor = cnx.cursor()

# Запит на оновлення балансу користувача
update_query = (f"UPDATE users SET balance = {balance} WHERE user_id = {ctx.author.id};")

# Виконуємо запит
cursor.execute(update_query)

# Зберігаємо зміни у базі даних
cnx.commit()

# Закриваємо з'єднання з базою даних
cursor.close()
cnx.close()

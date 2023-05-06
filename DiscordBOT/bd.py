import discord
import asyncio

# Создаем клиент с нужными нам интентами
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Создаем асинхронную функцию, которая будет менять цвет роли
async def change_role_color():
    await client.wait_until_ready()

    # Получаем гильдию и роль
    guild = client.get_guild(1091364118797226136)
    role = guild.get_role(1103033050960498809)

    # Создаем список цветов для переливания
    colors = [
        discord.Color.teal(),
        discord.Color.gold(),
        discord.Color.magenta(),
        discord.Color.purple(),
    ]

    # Индекс текущего цвета
    color_index = 0

    while not client.is_closed():
        # Получаем текущий цвет
        color = colors[color_index % len(colors)]

        # Изменяем цвет роли
        await role.edit(color=color)

        # Увеличиваем индекс цвета
        color_index += 1

        # Ждем 5 секунды перед следующей сменой цвета
        await asyncio.sleep(5)

# Функция, которая будет вызываться при успешном запуске клиента
@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

    # Запускаем функцию изменения цвета роли в отдельном таске
    client.loop.create_task(change_role_color())

# Асинхронная функция, которая запускает клиент и ожидает его завершения
async def main():
    # Токен вашего бота
    token = "MTEwMzAyNDk0OTA3OTMxODYwOQ.G6YU9x.tv-9ZaSbYOg8pIgsyEKxr6UtPHOj5JHt7zpmUE"

    await client.start(token)

# Запускаем основную асинхронную функцию
asyncio.run(main())
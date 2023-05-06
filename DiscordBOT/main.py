import discord
from discord import Intents
from discord import Activity, ActivityType, Client
import os
from dotenv import load_dotenv
import mysql.connector
from discord.ext import commands
from pathlib import Path
import re
import keep_alive

intents = discord.Intents().all()
intents.members = True

client = commands.Bot(command_prefix='p!', intents=intents)


@client.event
async def on_ready():
  activity = discord.Activity(name='PerchikRP | ПРОМОКОД 100 ГРН',
                              type=discord.ActivityType.playing)
  await client.change_presence(activity=activity)
  print('Бот готовий')


import mysql.connector

config = {
    'user': 'ch93f0bb7c_discord',
    'password': 'g54tg45hGTu6',
    'host': 'yaris.cityhost.com.ua',
    'database': 'ch93f0bb7c_discord',
    'raise_on_warnings': True,
}

try:
    cnx = mysql.connector.connect(**config)
    print("Успішне підключення до бази даних MySQL")
except mysql.connector.Error as err:
    print(f"Помилка підключення до бази даних MySQL: {err}")


@client.command()
async def balance(ctx):
  channel_id = 1091776353323450449
  channel = client.get_channel(channel_id)
  cursor = cnx.cursor()
  user_id = ctx.author.id
  # Запрос для получения баланса пользователя
  query = f"SELECT balance FROM users WHERE user_id = {user_id};"
  # Выполняем запрос и получаем результат
  cursor.execute(query)
  result = cursor.fetchone()
  # Если результат есть, выводим баланс, иначе добавляем нового пользователя с начальным балансом
  if result:
    balance = result[0]
    embed = discord.Embed(description=f"Твій баланс: {balance} Pcoin",
                          color=0x00bfff)
    embed.set_author(
      name="(P)economic",
      icon_url=
      "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
    )
    await ctx.author.send(embed=embed)  # Отправляем сообщение автору команды
    embed_bot = discord.Embed(
      description=
      f"Успіx! Інформацію про баланс відправлено в особисті повідомлення користувачу {ctx.author.name}",
      color=0x00ff00)
    embed_bot.set_author(
      name="Інформація",
      icon_url=
      "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
    )
    await channel.send(embed=embed_bot
                       )  # Отправляем сообщение в текстовый канал
  else:
    query = f"INSERT INTO users (user_id, balance) VALUES ({user_id}, 200)"
    cursor.execute(query)
    cnx.commit()
    embed = discord.Embed(
      description="Привіт друже! Тобі нараховано 200 Pcoin", color=0x00bfff)
    embed.set_author(
      name="(P)economic",
      icon_url=
      "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
    )
    await ctx.author.send(embed=embed)  # Отправляем сообщение автору команды
    embed_bot = discord.Embed(
      description=
      f"Створено нового користувача з балансом 200 Pcoin: {ctx.author.name}",
      color=0x00ff00)
    embed_bot.set_author(
      name="Інформація",
      icon_url=
      "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
    )
    await channel.send(embed=embed_bot
                       )  # Отправляем сообщение в текстовый канал
  # Закрываем соединение с базой данных
  cursor.close()


@client.command()
async def ping(ctx):
  await ctx.send('Pong!')


@client.command()
async def pay(ctx, member: discord.Member = None, amount: str = None):
  channel_id = 1091776353323450449
  channel = client.get_channel(channel_id)
  if member is None or amount is None:
    embed = discord.Embed(title="Укажіть ім'я користувача і суму!",
                          color=discord.Color.blue())
    embed.set_author(
      name="(P)economic",
      icon_url=
      "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
    )
    await ctx.send(embed=embed)
    return

  if not amount.isdigit():
    embed = discord.Embed(title="Помилка переказу", color=discord.Color.blue())
    embed.set_author(
      name="(P)economic",
      icon_url=
      "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
    )
    embed.add_field(
      name="Помилка",
      value="Ви можете вводити тільки прості цифри без математичних символів",
      inline=False)
    await ctx.send(embed=embed)
    return

  amount = int(amount)
  if cnx.is_connected():
    sender_id = ctx.author.id
    sender_balance_query = f"SELECT balance FROM users WHERE user_id = {sender_id}"
    sender_cursor = cnx.cursor()
    sender_cursor.execute(sender_balance_query)
    sender_balance_result = sender_cursor.fetchone()
    sender_balance = sender_balance_result[0] if sender_balance_result else None
    sender_cursor.close()

    if sender_balance is None or amount > sender_balance:
      embed = discord.Embed(title="Помилка переказу",
                            color=discord.Color.blue())
      embed.set_author(
        name="(P)economic",
        icon_url=
        "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
      )
      embed.add_field(
        name="Помилка",
        value="У вас недостатньо Pcoin для виконання цієї операції",
        inline=False)
      await ctx.send(embed=embed)
      return

    sender_update_query = f"UPDATE users SET balance = balance - {amount} WHERE user_id = {sender_id}"
    sender_update_cursor = cnx.cursor()
    sender_update_cursor.execute(sender_update_query)
    cnx.commit()
    sender_update_cursor.close()

    recipient_id = member.id
    recipient_update_query = f"INSERT INTO users (user_id, balance) VALUES ({recipient_id}, {amount}) ON DUPLICATE KEY UPDATE balance = balance + {amount}"
    recipient_update_cursor = cnx.cursor()
    recipient_update_cursor.execute(recipient_update_query)
    cnx.commit()
    recipient_update_cursor.close()

    embed = discord.Embed(title=f"Успіх! Ви успішно відправили Pcoin.",
                          color=discord.Color.blue())
    embed.set_author(
      name="(P)economic",
      icon_url=
      "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
    )
    embed.add_field(name="Відправник", value=ctx.author.mention, inline=False)
    embed.add_field(name="Одержувач", value=member.mention, inline=False)
    embed.add_field(name="Сума переказу", value=amount, inline=False)

    await ctx.send(embed=embed)
  else:
    await ctx.send("База даних не працює!")


@client.command()
async def setpcoin(ctx, member: discord.Member = None, amount: str = None):
  channel_id = 1091776353323450449
  channel = client.get_channel(channel_id)

  # Проверяем наличие необходимой роли у пользователя
  required_role1 = discord.utils.get(ctx.guild.roles, id=1091364118906294442)
  required_role2 = discord.utils.get(ctx.guild.roles, id=1101858209662259220)
  if required_role1 not in ctx.author.roles and required_role2 not in ctx.author.roles:
    embed = discord.Embed(
      title="Помилка",
      description="У вас недостатньо прав використовувати цю команду!",
      color=discord.Color.red())
    embed.set_author(
      name="(P)economic",
      icon_url=
      "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
    )
    await ctx.send(embed=embed)
    return

  if member is None or amount is None:
    embed = discord.Embed(title="Укажіть ім'я користувача і суму!",
                          color=discord.Color.blue())
    embed.set_author(
      name="(P)economic",
      icon_url=
      "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
    )
    await ctx.send(embed=embed)
    return

  if not amount.isdigit():
    embed = discord.Embed(title="Помилка",
                          description="Сума повинна складатися тільки з цифр!",
                          color=discord.Color.red())
    embed.set_author(
      name="(P)economic",
      icon_url=
      "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
    )
    await ctx.send(embed=embed)
    return

  amount = int(amount)

  if cnx.is_connected():
    cursor = cnx.cursor()
    user_id = member.id
    query = f"SELECT balance FROM users WHERE user_id = {user_id};"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
      balance = result[0]
      balance += amount
      query = f"UPDATE users SET balance = {balance} WHERE user_id = {user_id}"
      cursor.execute(query)
      cnx.commit()
      embed_bot = discord.Embed(
        description=f"Користувачу {member.name} було нараховано {amount} Pcoin",
        color=0x00ff00)
      embed_bot.set_author(
        name="Інформація",
        icon_url=
        "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
      )
      await ctx.send(embed=embed_bot)  # Отправляем сообщение в текстовый канал
    else:
      query = f"INSERT INTO users (user_id, balance) VALUES ({user_id}, {amount})"
      cursor.execute(query)
      cnx.commit()
      embed_bot = discord.Embed(
        description=
        f"Створено нового користувача {member.name} з балансом {amount} Pcoin",
        color=0x00ff00)
      embed_bot.set_author(
        name="Інформація",
        icon_url=
        "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
      )
      await ctx.send(embed=embed_bot)  # Отправляем сообщение в текстовый канал
    cursor.close()


@client.command()
async def rempcoin(ctx, member: discord.Member = None, amount: str = None):
  channel_id = 1091776353323450449
  channel = client.get_channel(channel_id)

  # Проверяем наличие необходимой роли у пользователя
  required_role1 = discord.utils.get(ctx.guild.roles, id=1091364118906294442)
  required_role2 = discord.utils.get(ctx.guild.roles, id=1101858209662259220)
  if required_role1 not in ctx.author.roles and required_role2 not in ctx.author.roles:
    embed = discord.Embed(
      title="Помилка",
      description="У вас недостатньо прав використовувати цю команду!",
      color=discord.Color.red())
    embed.set_author(
      name="(P)economic",
      icon_url=
      "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
    )
    await ctx.send(embed=embed)
    return

  if member is None or amount is None:
    embed = discord.Embed(title="Укажіть ім'я користувача і суму!",
                          color=discord.Color.blue())
    embed.set_author(
      name="(P)economic",
      icon_url=
      "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
    )
    await ctx.send(embed=embed)
    return

  # Проверяем, что сумма состоит только из цифр
  if not re.match(r"^\d+$", amount):
    embed = discord.Embed(title="Невірний формат суми!",
                          description="Укажіть коректну суму!",
                          color=discord.Color.red())
    await ctx.send(embed=embed)
    return

  if cnx.is_connected():
    cursor = cnx.cursor()
    user_id = member.id
    query = f"SELECT balance FROM users WHERE user_id = {user_id};"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
      balance = result[0]
      if balance <= int(amount):
        balance = 0
      else:
        balance -= int(amount)
      query = f"UPDATE users SET balance = {balance} WHERE user_id = {user_id}"
      cursor.execute(query)
      cnx.commit()
      embed_bot = discord.Embed(
        description=f"У користувача {member.name} було списано {amount} Pcoin",
        color=discord.Color.green())
      embed_bot.set_author(
        name="Інформація",
        icon_url=
        "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
      )
      await ctx.send(embed=embed_bot)  # Отправляем сообщение в текстовый канал
    else:
      embed_bot = discord.Embed(
        description=f"Користувач {member.name} не знайдений у базі даних",
        color=discord.Color.red())
      embed_bot.set_author(
        name="Помилка",
        icon_url="https://cdn.discordapp.com/attachments/1094564118549237760")
      await ctx.send(embed=embed_bot)  # Отправляем сообщение в текстовый канал
      cursor.close()


@client.command()
async def toplist(ctx):
  channel_id = 1091776353323450449
  channel = client.get_channel(channel_id)

  if cnx.is_connected():
    cursor = cnx.cursor()
    query = "SELECT * FROM users ORDER BY balance DESC LIMIT 10"
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
      embed = discord.Embed(
        title="Топ(10)-багачів",
        description="Топ-10 користувачів серверу з найбільшою кількістю Pcoin:",
        color=discord.Color.blue())
      embed.set_author(
        name="(P)economic",
        icon_url=
        "https://cdn.discordapp.com/attachments/1094564118549237760/1102885570415431742/2.png"
      )
      for i in range(len(result)):
        user = await client.fetch_user(result[i][0])
        embed.add_field(name=f"{i+1}. {user.name}",
                        value=f"{result[i][1]} Pcoin",
                        inline=False)
      await ctx.send(embed=embed)
    else:
      await ctx.send("Немає жодного користувача в базі даних.")
  else:
    await ctx.send("Помилка підключення до бази даних.")


keep_alive.keep_alive()
client.run(os.environ["Token"])
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()  # Убедитесь, что у вас установлен модуль python-dotenv
TOKEN = os.getenv('DISCORD_TOKEN')  # Сохраните токен в .env файле

if TOKEN is None:
    raise ValueError("Токен Discord не задан. Проверьте ваш файл .env.")

# Настраиваем намерения
intents = discord.Intents.default()
intents.message_content = True  # Включите это намерение

# Создаем экземпляр бота с префиксом "Кентовка,"
bot = commands.Bot(command_prefix="Кентовка, ", intents=intents)

@bot.event
async def on_ready():
    print(f'Бот запущен как {bot.user.name}')

# Список случайных фраз
phrases = [
    "РПКшни уебище РПшное, на твой выбор!",
    "Обнеси базу в ночь, пока админы спят.",
    "Выходной, отдыхай."
]

@bot.command(aliases=['дай'])
async def _rules(ctx, arg):
    if arg == 'задание':
        task = random.choice(phrases)
        await ctx.send(task)

@bot.command(name='пинг')
async def ping(ctx):
    await ctx.send('Понг!')

# Запуск бота
bot.run(TOKEN)
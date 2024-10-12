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

# Функция для загрузки фраз из файла
def load_phrases(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []

# Загрузка фраз из файла frazi.txt
phrases = load_phrases('frazi.txt')

# Загрузка фраз из файла dogmati.txt для команды "напомни правила"
rules_phrases = load_phrases('dogmati.txt')

@bot.command(aliases=['дай'])
async def _rules(ctx, arg):
    if arg == 'задание':
        if phrases:
            task = random.choice(phrases)
            await ctx.send(task)
        else:
            await ctx.send("Список фраз пуст или файл не найден.")

@bot.command(aliases=['напомни'])
async def rules(ctx, arg):
    if arg == 'правила':
        if rules_phrases:
            rules_list = "\n".join(rules_phrases)
            await ctx.send(f"Вот догматы кентовки. Тут все по сунне:\n{rules_list}")
        else:
            await ctx.send("Список фраз пуст или файл не найден.")

@bot.command(name='пинг')
async def ping(ctx):
    await ctx.send('Понг!')

# Запуск бота
bot.run(TOKEN)
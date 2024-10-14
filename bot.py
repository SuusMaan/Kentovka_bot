import os
import random
import asyncio
import discord
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
from phrase_loader import phrases, rules_phrases
from forbidden_words_loader import forbidden_words
from gif_manager import get_random_gif
import openai

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if TOKEN is None:
    raise ValueError("Токен Discord не задан. Проверьте ваш файл .env.")

if OPENAI_API_KEY is None:
    raise ValueError("API ключ OpenAI не задан. Проверьте ваш файл .env.")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="Кентовка, ", intents=intents)

# Путь к файлу для хранения данных
DATA_FILE = 'pidoras_list.txt'

# Список для хранения данных
pidoras_list = []

# Функция для загрузки данных из текстового файла
def load_data_txt():
    global pidoras_list
    pidoras_list = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                name, discord_id, reason, date_added = map(str.strip, line.strip().split(','))
                pidoras_list.append({'name': name, 'discord': discord_id, 'reason': reason, 'date_added': date_added})

# Функция для сохранения данных в текстовый файл
def save_data_txt():
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        for entry in pidoras_list:
            line = f"{entry['name']},{entry['discord']},{entry['reason']},{entry['date_added']}\n"
            file.write(line)

@bot.event
async def on_ready():
    load_data_txt()  # Загружаем данные при запуске бота
    print(f'Бот запущен как {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("Кентовка, "):
        content_without_prefix = message.content[len("Кентовка, "):].strip()

        if content_without_prefix.lower() == 'напиши мне квенту':
            await message.channel.send("Какие данные указать для квенты?")

            def check(m):
                return m.author == message.author and m.channel == message.channel

            try:
                response = await bot.wait_for('message', check=check, timeout=60.0)
                user_data = response.content.strip()
                await message.channel.send("Генерирую квенту...")

                # Запрос к ChatGPT 
                completion = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Напиши мне квенту с использованием следующих данных: {user_data}",
                    max_tokens=150 )

                story = completion.choices[0].text.strip()
                await message.channel.send(story)

            except asyncio.TimeoutError:
                await message.channel.send("Время ожидания истекло. Попробуйте снова.")
            return

        # Проверка на запрещенные слова
        if any(word in content_without_prefix.lower() for word in forbidden_words):
            try:
                await message.reply(f"{message.author.mention}, я снесу нахуй сообщение через 10 секунд, уебище. И ник тебе еще поменяю, уродец.", mention_author=True)
                await asyncio.sleep(10)
                await message.delete()
                new_nick = "Осел топай в стойло"
                await message.author.edit(nick=new_nick)
                print("Ник успешно изменен.")
            except discord.Forbidden:
                print("Ошибка: недостаточо прав для изменения ника.")
                await message.channel.send(f"{message.author.mention} Бля обознался, я снес сообщение но ник тебе уебище поменять не смогу. Сорян.")
            except discord.HTTPException as e:
                print(f"Ошибка при изменении ника: {e}")

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Хуйню пишешь, пиши как принято у нас в Кентовке, осел.")
    else:
        raise error

@bot.command(aliases=['дай'])
async def _rules(ctx, arg=None):
    if arg == 'задание':
        await ctx.send(random.choice(phrases) if phrases else "Список фраз пуст или файл не найден.")
    else:
        await ctx.send("Хули тебе дать? По ебалу? Или задание? Тогда так и пиши. Кентовка, дай задание")

@bot.command(aliases=['напомни'])
async def rules(ctx, arg=None):
    if arg == 'правила':
        if rules_phrases:
            rules_list = "\n".join(rules_phrases)
            await ctx.send(f"```diff\n- Вот догматы кентовки. Тут все по сунне:```\n```{rules_list}```")
        else:
            await ctx.send("Список фраз пуст или файл не найден.")
    else:
        await ctx.send("Чего тебе блять напомнить? Правила? Ну так и пиши как положено. Кентовка, напомни правила.")

@bot.command(name='гифку')
async def gif(ctx):
    await ctx.send(get_random_gif())

bot.run(TOKEN)

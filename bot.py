import os
import random
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Импортируем phrases и rules_phrases из phrase_loader.py
from phrase_loader import phrases, rules_phrases

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

# Загрузка списка запретных слов из файла
with open('forbidden_words.txt', 'r', encoding='utf-8') as f:
    forbidden_words = [line.strip().lower() for line in f.readlines()]
@bot.event
async def on_ready():
    print(f'Бот запущен как {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Проверяем, начинается ли сообщение с "Кентовка, "
    if message.content.startswith("Кентовка, "):
        # Удаляем префикс "Кентовка, " и получаем текст сообщения без него
        content_without_prefix = message.content[len("Кентовка, "):].strip()

        # Проверяем на наличие запретных слов
        if any(word in content_without_prefix.lower() for word in forbidden_words):
            try:
                await message.channel.send(f"{message.author.mention}, я снесу нахуй сообщение через 30 секунд, уебище.")
                await asyncio.sleep(30)  # Ожидание 30 секунд перед удалением сообщения
                await message.delete()
                new_nick = f"Осел топай в стойло {random.randint(1000, 9999)}" # Определяем новый ник для пользователя 
                await message.author.edit(nick=new_nick) # Изменение ника пользователя 
            except discord.Forbidden:
                await message.channel.send("Бля обознался, я снес сообщение но ник тебе уебище поменять не смогу. Сорян. А и насчет твоего вопроса. . . ")
            except discord.HTTPException as e:
                print(f"Ошибка при изменении ника: {e}")

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Хуйню пишешь, пиши как принято у нас в Кентовке, осел.")
    else:
        raise error  # Поднимите другие ошибки, чтобы их можно было отследить

@bot.command(aliases=['дай'])
async def _rules(ctx, arg=None):
    if arg == 'задание':
        if phrases:
            task = random.choice(phrases)
            await ctx.send(task)
        else:
            await ctx.send("Список фраз пуст или файл не найден.")
    else:
        await ctx.send("Хули тебе дать? По ебалу? Или задание? Тогда так и пиши. Кентовка, дай задание")

@bot.command(aliases=['напомни'])
async def rules(ctx, arg=None):
    if arg == 'правила':
        if rules_phrases:
            rules_list = "\n".join(rules_phrases)
            await ctx.send(f"```diff\n- Вот догматы кентовки. Тут все по сунне:\n{rules_list}```")
        else:
            await ctx.send("Список фраз пуст или файл не найден.")
    else:
        await ctx.send("Чего тебе блять напомнить? Правила? Ну так и пиши как положено. Кентовка, напомни правила.")

@bot.command(name='пинг')
async def ping(ctx):
    await ctx.send('Понг!')

# Запуск бота
bot.run(TOKEN)

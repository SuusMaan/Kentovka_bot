import os
import random
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Импортируем phrases и rules_phrases из phrase_loader.py
from phrase_loader import phrases, rules_phrases

# Загружаем переменные окружения из .env файла
load_dotenv()  # Убедитесь, что у вас установлен мдуль python-dotenv
TOKEN = os.getenv('DISCORD_TOKEN')  # Сохраните токен в .env файле

if TOKEN is None:
    raise ValueError("Токен Discord не задан. Проверьте ваш файл .env.")

# Настраиваем намерения
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="Кентовка, ", intents=intents)

# Загрузка списка запретных слов из файла
with open('forbidden_words.txt', 'r', encoding='utf-8') as f:
<<<<<<< HEAD
    forbidden_words = [line.strip().lower() for line in f.readlines()]

# Список гифок
gif_urls = [
    "https://media1.tenor.com/m/eQpw7DS4LSwAAAAC/%D0%B1%D0%B0%D0%B1%D0%B0%D0%B5%D0%B2%D1%81%D0%BA%D0%B8%D0%B9.gif",
    "https://media1.tenor.com/m/uWlz-LRz4HAAAAAd/%D0%B1%D0%B0%D0%B9-%D0%B1%D0%B0%D0%B9.gif",
    "https://media.discordapp.net/attachments/768189501918019617/1171558356993974332/prichina.gif?ex=670ce0fe&is=670b8f7e&hm=cfaac35c0b09860a3f9f68d6fad42c08a5e4f7aa19898e78615c6d41ff8b20a2&"
    # Добавьте сюда другие URL-адреса гифок
]

# Переменная для хранения последней отправленной гифки
last_gif_url = None

=======
    forbidden_words = [line.strip().lower() for line in f]
>>>>>>> 77a40fd3c1d1ed2b89b695fdbaaf0dec4ce21149
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
                await message.reply(f"{message.author.mention}, я снесу нахуй сообщение через 10 секунд, уебище. И ник тебе еще поменяю, уродец.", mention_author=True)
                await asyncio.sleep(10)  # Ожидание 10 секунд перед удалением сообщения
                await message.delete()
                new_nick = "Осел топай в стойло"
                await message.author.edit(nick=new_nick)  # Изменение ника пользователя
                print("Ник успешно изменен.")
            except discord.Forbidden:
                print("Ошибка: недостаточно прав для изменения ника.")
                await message.channel.send(f"{message.author.mention} Бля обознался, я снес сообщение но ник тебе уебище поменять не смогу. Сорян. А и насчет твоего вопроса. . .")
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
    global last_gif_url 
    gif_url = random.choice(gif_urls)
    
    # Проверяем, чтобы новая гифка не совпадала с последней
    while gif_url == last_gif_url:
        gif_url = random.choice(gif_urls)
 # Отправляем гифку
    await ctx.send(gif_url)
    
    # Обновляем последнюю отправленную гифку
    last_gif_url = gif_url



# Запуск бота
bot.run(TOKEN)

import os
import random
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from phrase_loader import phrases, rules_phrases
from forbidden_words_loader import forbidden_words
from gif_manager import get_random_gif
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Загрузка токена Discord из файла .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    raise ValueError("Токен Discord не задан. Проверьте ваш файл .env.")

# Настройка интентов и бота
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="Кентовка, ", intents=intents)

DATA_FILE = 'pidoras_list.txt'
pidoras_list = []

# Функция для загрузки данных из файла
def load_data_txt():
    global pidoras_list
    pidoras_list = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                name, discord_id, reason, date_added = map(str.strip, line.strip().split(','))
                pidoras_list.append({'name': name, 'discord': discord_id, 'reason': reason, 'date_added': date_added})

# Функция для сохранения данных в файл
def save_data_txt():
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        for entry in pidoras_list:
            line = f"{entry['name']},{entry['discord']},{entry['reason']},{entry['date_added']}\n"
            file.write(line)

@bot.event
async def on_ready():
    load_data_txt()
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

                # Использование Selenium для отправки запроса в веб-чат
                chrome_options = Options()
                chrome_options.add_argument("--headless")  # Запуск без графического интерфейса
                chrome_options.add_argument("--disable-gpu")  # Отключить аппаратное ускорение
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")

                driver_service = Service('path/to/chromedriver')  # Укажите путь к вашему chromedriver
                driver = webdriver.Chrome(service=driver_service, options=chrome_options)

                try:
                    driver.get('https://gpt-chatbot.ru/')  # URL

                    # Ждем пока элемент текстового поля станет доступным
                    input_box = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '#chat-input'))  # Проверьте корректность селектора
                    )

                    # Устанавливаем фокус на поле ввода
                    input_box.click()

                    # Ввод данных в поле
                    input_box.send_keys(f"Напиши мне квенту с использованием следующих данных: {user_data}")

                    # Небольшая пауза перед отправкой
                    time.sleep(0.5)

                    # Отправка сообщения
                    input_box.send_keys(Keys.RETURN)

                    # Подождите, пока ответ появится
                    response_element = WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, '.response-class'))  # Проверьте селектор для ответа
                    )

                    # Получение текста ответа
                    story = response_element.text
                    await message.channel.send(story)

                except Exception as e:
                    print(f"Ошибка при работе с Selenium: {str(e)}")
                    await message.channel.send("Произошла ошибка при получении квенты.")
                finally:
                    driver.quit()

            except asyncio.TimeoutError:
                await message.channel.send("Время ожидания истекло. Попробуйте снова.")
                return

        if any(word in content_without_prefix.lower() for word in forbidden_words):
            try:
                await message.reply(f"{message.author.mention}, я снесу нахуй сообщение через 10 секунд, уебище. И ник тебе еще поменяю, уродец.", mention_author=True)
                await asyncio.sleep(10)
                await message.delete()
                new_nick = "Осел топай в стойло"
                await message.author.edit(nick=new_nick)
                print("Ник успешно изменен.")
            except discord.Forbidden:
                print("Ошибка: недостаточно прав для изменения ника.")
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
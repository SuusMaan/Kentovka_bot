import os
import random
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from phrase_loader import phrases, rules_phrases
from forbidden_words_loader import forbidden_words
from gif_manager import get_random_gif

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    raise ValueError("Токен Discord не задан. Проверьте ваш файл .env.")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="Кентовка, ", intents=intents)

@bot.event
async def on_ready():
    print(f'Бот запущен как {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("Кентовка, "):
        content_without_prefix = message.content[len("Кентовка, "):].strip()

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

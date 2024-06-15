import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from ai_model import get_class


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
MODEL_PATH = os.getenv("MODEL_PATH")
LABELS_PATH = os.getenv("LABELS_PATH")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен!')

@bot.command()
async def help(ctx):
    await ctx.send(f"Привет! Я {bot.user}, готов тебе помочь!")

@bot.command()
async def photo(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            if attachment.filename.endswith('.jpg') or attachment.filename.endswith('.jpeg') or attachment.filename.endswith('.png'):
                image_path = f'./images/{attachment.filename}'
                await attachment.save(image_path)
                await ctx.send('Фото успешно сохранено!')
                msg = await ctx.send('Фото обробатываеться...')
                class_name, confidence_procent = get_class(MODEL_PATH, LABELS_PATH, image_path)
                await msg.delete()
                if confidence_procent > 30:
                    await ctx.send(f'Кажется, на фото {class_name} с вероятностью {confidence_procent}%')
                else:
                    await ctx.send(f"Упс! Мне не понятно это изображение")
                os.remove(image_path)
            else:
                await ctx.send(f"Не тот формат файла {attachment.filename}, используйте jpg, jpeg или png")
                return
    else:
        await ctx.send('Вы забыли прикрепить фото =(') 

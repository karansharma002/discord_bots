import discord
from discord.ext import commands
import json
from googletrans import Translator
import os

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
translator = Translator()

def load_channels(file_name):
    try:
        with open(file_name) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_channels(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=3)

@bot.event
async def on_ready():
    print('----- TRANSLATOR BOT IS RUNNING ------')

@bot.command()
async def translate(ctx, action: str = None, channel1: discord.TextChannel = None, channel2: discord.TextChannel = None):
    if not action:
        await ctx.send(':information_source: Usage: !translate `<ACTION (ENABLE/DISABLE/ADD)>`')
        return

    if action == 'enable':
        await ctx.send(':white_check_mark: Translator Enabled')
        bot.running = True

    elif action == 'disable':
        await ctx.send(':white_check_mark: Translator Disabled')
        bot.running = False

    elif action == 'add':
        if not channel1 or not channel2:
            await ctx.send(':information_source: Usage: !translate `<add>` `<#CHANNEL1 ENGLISH>` `<#CHANNEL2 SPANISH>`')
            return

        en_channels = load_channels('EN.json')
        sp_channels = load_channels('SP.json')

        en_channels[str(channel1.id)] = channel2.id
        sp_channels[str(channel2.id)] = channel1.id

        save_channels(en_channels, 'EN.json')
        save_channels(sp_channels, 'SP.json')

        await ctx.send(':white_check_mark: Channel Added')

@bot.event
async def on_message(message):
    if message.content.startswith('&'):
        await bot.process_commands(message)
        return

    if not bot.running:
        return

    language_data = load_channels('Languages.json')
    en_channels = load_channels('EN.json')
    sp_channels = load_channels('SP.json')

    def get_language(value):
        return language_data[value]

    async def translate_message(message, from_lang, to_lang):
        to_channel = await bot.fetch_channel(to_lang[str(message.channel.id)])
        translated_message = translator.translate(message.content, src=get_language(from_lang), dest=get_language(to_lang))
        webhook = await to_channel.create_webhook(name=message.author.name)
        await webhook.send(content=translated_message.text, username=message.author.name, avatar_url=message.author.avatar_url, wait=True)
        for webhook in await to_channel.webhooks():
            await webhook.delete()

    if str(message.channel.id) in sp_channels:
        await translate_message(message, 'spanish', en_channels)

    elif message.channel.id in en_channels:
        await translate_message(message, 'english', sp_channels)

bot.run(os.getenv('BOT_TOKEN'))

import discord
from discord.ext import commands

import pymongo
import json
import os

bot = commands.Bot(command_prefix='!')

# Load configuration from config file
with open('config.json') as f:
    config = json.load(f)

# Connect to MongoDB
database = pymongo.MongoClient(config['host'], config['port'])
database_name = database[config['database']]
mycol = database_name[config['collection']]

# Event: Bot is ready
@bot.event
async def on_ready():
    print('------ BOT HAS STARTED -------')

# Event: Message received
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    for embed in message.embeds:
        if 'successful checkout' in embed.description.lower():
            result = 'exists'
            break
    else:
        return

    fields_to_remove = {'Promo Code', 'Item Price', 'Purchase Price', 'Order', 'Proxy', 'Email', 'Profile name',
                       'Offer ID', 'Password', 'Session Name', 'Account', 'Account:', 'Delay', 'Mode', 'Version'}

    fields_to_replace = {'Profile', 'Account', 'User', 'Session Name', 'Profile Name', 'email'}

    for field in embed.fields.copy():
        if any(character.lower() in field.name.lower() for character in fields_to_remove):
            embed.remove_field(embed.fields.index(field))
        elif any(character.lower() in field.name.lower() for character in fields_to_replace):
            for x in mycol.find():
                if 'Profiles' in x:
                    profiles = [email.strip("'\"") for email in x['Profiles'].split(',')]
                    if any(email in field.value for email in profiles):
                        field.value = x['User']
                        break

    target_channel = bot.get_channel(942795086742290433)
    if target_channel:
        await target_channel.send(embed=embed)

# Run the bot
bot_token = os.getenv('BOT_TOKEN')
bot.run(bot_token)

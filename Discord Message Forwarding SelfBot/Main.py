from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands
import json
import aiohttp
import os

bot = commands.Bot(command_prefix='!', self_bot=True)

@bot.event
async def on_ready():
    print('---SERVER STARTED----')
    await bot.wait_until_ready()
    with open('Data.json') as f:
        bot.data = json.load(f)

@bot.event
async def on_message(message):
    ch_id = str(message.channel.id)
    if ch_id in bot.data:
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(bot.data[ch_id], adapter=Webhook.AioHttpAdapter(session))
            if message.embeds:
                await webhook.send(embeds=message.embeds)
            else:
                files = [await attch.to_file() for attch in message.attachments]
                await webhook.send(content=message.content, tts=message.tts, files=files)

bot.run(os.environ['TOKEN'])

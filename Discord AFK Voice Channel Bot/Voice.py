import discord
from discord.ext import commands
import os

token = os.environ['TOKEN']

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command()
async def setchannel(ctx, channel: discord.VoiceChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !setchannel #AFKVOICECHANNEL')
        return
    else:
        bot.afk_channel_id = channel.id
        await ctx.send(':white_check_mark: Channel Set')

@bot.event
async def on_voice_state_update(member, before, after):
    try:
        if after.self_deaf and hasattr(bot, 'afk_channel_id'):
            afk_channel = await bot.fetch_channel(bot.afk_channel_id)
            await member.move_to(afk_channel)
    except Exception as e:
        print(f"Error handling voice state update: {e}")

@bot.event
async def on_ready():
    print('=== BOT STARTED ===')

bot.run(token)

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_components import (
    create_button,
    create_actionrow,
    wait_for_component,
)
from discord_slash.model import ButtonStyle
import json
import time
from youtube_search import YoutubeSearch
import youtube_dl
import random
import datetime
import asyncio
import os

# Initialize bot with all intents
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

ch = 0
song_queue = []
dupl_queue = []

def search_song(query):
    ydl_opts = {'format': 'bestaudio'}
    yt_results = YoutubeSearch(query, max_results=1).to_json()
    yt_id = json.loads(yt_results)['videos'][0]['id']
    yt_url = f'https://www.youtube.com/watch?v={yt_id}'

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(yt_url, download=False)
        URL = info['formats'][0]['url']

    duration = time.strftime('%H:%M:%S', time.gmtime(info['duration']))
    img_url = info['thumbnails'][0]['url']
    return {'source': URL, 'title': info['title'], 'duration': duration, 'url': yt_url, 'thumbnail': img_url}

async def skip_song(ctx):
    global song_queue
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if song_queue:
        song_queue.pop(0)
        if song_queue:
            voice.play(discord.FFmpegPCMAudio(song_queue[0]['source']), after=lambda e: asyncio.run_coroutine_threadsafe(skip_song(ctx), bot.loop))
        else:
            await voice.disconnect()

@slash.slash(name="application", description="Submits a whitelist application.")
async def application(ctx):
    global ch
    questions = [
        "Q1: What is your Minecraft Username? (Please make sure this is EXACT before you continue as you will be required to retake the entire application if it's incorrect.",
        "Q2: Have you ever been on any other hermit style or SMP servers before? If so please state the name(s). (Type them all within one message)",
        "Q3: What is your birth year and month? (For privacy reasons we will not request the day, though we need your year and month for security reasons)",
        "Q4: How did you find out about us? If you were invited by a friend please state their Discord User. (We just like to know which of our sites are doing well and which need some work)",
        "Q5: By clicking the final accept button you agree that you have read through the Rules provided here: cobalt-smp.com/rules-n-info (and accept any consequence to breaking them)"
    ]
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    replies = []
    for question in questions:
        embed = discord.Embed(description=question, color=discord.Color.green())
        msg = await ctx.send(embed=embed)
        try:
            reply = await bot.wait_for('message', check=check, timeout=120)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond. Please try again.")
            return
        replies.append(reply.content)
        await msg.delete()
        await reply.delete()

    buttons = [create_button(style=ButtonStyle.green, label="I Accept")]
    action_row = create_actionrow(*buttons)
    msg = await ctx.send(embed=embed, components=[action_row])

    try:
        interaction = await bot.wait_for("button_click", check=lambda i: i.component.label == "I Accept")
        await interaction.send(content="Your application has been successfully forwarded to the moderators.", hidden=True)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to accept. Please try again.")
        return

    embed = discord.Embed(description='Your application has been successfully forwarded to the moderators.', color=discord.Color.blurple())
    await ctx.author.send(embed=embed)

    embed = discord.Embed(title=f"{ctx.author} | Application")
    for question, reply in zip(questions, replies):
        embed.add_field(name=question, value=reply, inline=False)
    
    global ch
    channel = await bot.fetch_channel(ch)
    await channel.send(embed=embed, components=[action_row])

@slash.slash(name="giveaway", description="Starts the Giveaway")
async def giveaway(ctx, role: discord.Role, *, prize: str = None):
    global gw

    if role is None or prize is None:
        await ctx.send(':information_source: Usage: !giveaway `<#Role Mention>` `<Prize Name>`')
        return

    await ctx.message.delete()

    members = [member.id for member in ctx.guild.members if role in member.roles]

    if not members:
        await ctx.send('No members with the specified role found.')
        return

    winner_id = random.choice(members)
    winner = await bot.fetch_user(winner_id)

    embed = discord.Embed(color=discord.Color.blue(), title=f':tada: Congratulations {winner}, You have won the: **{prize}**')
    embed.add_field(name='Winners:', value=f"{winner}", inline=False)
    embed.add_field(name='Hosted By:', value=f"{ctx.author}", inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.channel.send(embed=embed)

@slash.slash(name="giveaway_vc", description="Starts the Giveaway")
@commands.has_permissions(administrator=True)
async def giveaway_vc(ctx, voice_channel: discord.VoiceChannel, *, prize: str = None):
    if voice_channel is None or prize is None:
        await ctx.send(':information_source: Usage: !giveaway_vc `<#VOICE CHANNEL>` `<Prize Name>`')
        return

    await ctx.message.delete()

    members = [member.id for member in voice_channel.members]

    if not members:
        await ctx.send('No members in the specified voice channel found.')
        return

    winner_id = random.choice(members)
    winner = await bot.fetch_user(winner_id)

    embed = discord.Embed(color=discord.Color.blue(), title=f':tada: Congratulations {winner}, You have won the: **{prize}**')
    embed.add_field(name='Winners:', value=f"{winner}", inline=False)
    embed.add_field(name='Hosted By:', value=f"{ctx.author}", inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.channel.send(embed=embed)

@slash.slash(name="quote", description="Saves the Quote")
async def quote(ctx, user: discord.User, date: str, *, quote: str):
    if not date.count('-') == 2:
        embed = discord.Embed(color=discord.Color.blue(), description='Invalid Format - Please use: DD-MM-YY')
        await ctx.send(embed=embed, hidden=True)
        return

    try:
        datetime.datetime.strptime(date, "%d-%m-%y")
    except ValueError:
        embed = discord.Embed(color=discord.Color.blue(), description='Invalid Date - Please use: DD-MM-YY')
        await ctx.send(embed=embed, hidden=True)
        return

    with open('Quotes.json', 'r') as f:
        quotes = json.load(f)

    if str(user.id) not in quotes:
        quotes[str(user.id)] = {}
    quotes[str(user.id)][date] = quote

    with open('Quotes.json', 'w') as f:
        json.dump(quotes, f, indent=4)

    embed = discord.Embed(color=discord.Color.blue(), description='Quote Saved')
    await ctx.channel.send(embed=embed)

@slash.slash(name="quote_random", description="Gets a random quote from a specific user or everyone")
async def quote_random(ctx, user: discord.User = None):
    with open('Quotes.json', 'r') as f:
        quotes = json.load(f)

    if user:
        if str(user.id) not in quotes:
            await ctx.send('No quotes found for this user.')
            return
        user_quotes = quotes[str(user.id)]
    else:
        user_quotes = {k: v for user_quotes in quotes.values() for k, v in user_quotes.items()}

    if not user_quotes:
        await ctx.send('No quotes found.')
        return

    random_date = random.choice(list(user_quotes.keys()))
    random_quote = user_quotes[random_date]

    if user:
        user_name = user
    else:
        user_id = random.choice(list(quotes.keys()))
        user = await bot.fetch_user(int(user_id))
        user_name = user

    embed = discord.Embed(color=discord.Color.blue(), description=random_quote, title=random_date)
    embed.set_author(name=f"{user_name} | QUOTE", icon_url=user.avatar_url)
    await ctx.channel.send(embed=embed)

bot.run(os.getenv('TOKEN'))

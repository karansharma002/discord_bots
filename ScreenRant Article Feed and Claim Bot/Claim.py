import discord
from discord.ext import commands, tasks
import json
import feedparser

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready')
    feed_fetch.start()

@tasks.loop(seconds=60)
async def feed_fetch():
    url = 'https://screenrant.com/feed/'
    feed = feedparser.parse(url)
    sent_titles = []

    try:
        with open('sent_titles.json', 'r') as f:
            sent_titles = json.load(f)
    except FileNotFoundError:
        pass

    channel = await bot.fetch_channel(886983311535247361)

    for entry in feed.entries:
        title = f":newspaper: **| {entry.title}**"
        if title not in sent_titles:
            msg = f"{title}\n\n{entry.link}"
            sent_titles.append(title)
            await channel.send(msg)
    
    with open('sent_titles.json', 'w') as f:
        json.dump(sent_titles, f, indent=3)

@bot.event
async def on_message(message):
    if not message.guild:
        return
    
    with open('Settings.json') as f:
        settings = json.load(f)
    
    if str(message.channel.id) in settings.get('Channels', []):
        await message.add_reaction('👍')

    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    with open('Settings.json') as f:
        settings = json.load(f)
    
    channel_id = str(payload.channel_id)
    if channel_id not in settings.get('Channels', []):
        return
    
    guild = await bot.fetch_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)

    if channel_id in settings:
        return
    
    for role_id in settings.get('Roles', []):
        role = discord.utils.get(guild.roles, id=int(role_id))
        if role in user.roles:
            settings[channel_id] = user.id
            with open('Settings.json', 'w') as f:
                json.dump(settings, f, indent=3)
            for member in guild.members:
                if member.guild_permissions.administrator:
                    try:
                        await member.send(f'{user} has claimed the article. ID: {payload.message_id} in <#{channel_id}>')
                    except Exception as e:
                        print(f"Error sending message to {member}: {e}")
            return

@bot.command()
async def addchannel(ctx, channel: discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !addchannel `#CHANNEL`')
        return

    with open('Settings.json') as f:
        settings = json.load(f)
    
    if str(channel.id) not in settings.get('Channels', []):
        settings.setdefault('Channels', []).append(str(channel.id))
        with open('Settings.json', 'w') as f:
            json.dump(settings, f, indent=3)
        await ctx.send(':white_check_mark: Channel Added')
    else:
        await ctx.send(':warning: Channel already exists in the database.')

@bot.command()
async def removechannel(ctx, channel: discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !removechannel `#CHANNEL`')
        return

    with open('Settings.json') as f:
        settings = json.load(f)
    
    if str(channel.id) in settings.get('Channels', []):
        settings['Channels'].remove(str(channel.id))
        with open('Settings.json', 'w') as f:
            json.dump(settings, f, indent=3)
        await ctx.send(':white_check_mark: Channel Removed')
    else:
        await ctx.send(':warning: Channel does not exist in the database.')

@bot.command()
async def addrole(ctx, role: discord.Role = None):
    if not role:
        await ctx.send(':information_source: Usage: !addrole `@ROLE`')
        return

    with open('Settings.json') as f:
        settings = json.load(f)
    
    if str(role.id) not in settings.get('Roles', []):
        settings.setdefault('Roles', []).append(str(role.id))
        with open('Settings.json', 'w') as f:
            json.dump(settings, f, indent=3)
        await ctx.send(':white_check_mark: Role Added')
    else:
        await ctx.send(':warning: Role already exists in the database.')

@bot.command()
async def removerole(ctx, role: discord.Role = None):
    if not role:
        await ctx.send(':information_source: Usage: !removerole `@ROLE`')
        return

    with open('Settings.json') as f:
        settings = json.load(f)
    
    if str(role.id) in settings.get('Roles', []):
        settings['Roles'].remove(str(role.id))
        with open('Settings.json', 'w') as f:
            json.dump(settings, f, indent=3)
        await ctx.send(':white_check_mark: Role Removed')
    else:
        await ctx.send(':warning: Role does not exist in the database.')

bot.run('YOUR_BOT_TOKEN')

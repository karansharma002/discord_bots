import discord
from discord.ext import commands, tasks
import requests
import json
import base64
import datetime

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('----------- BOT HAS STARTED --------------')
    update_post.start()

@tasks.loop(minutes=2)
async def update_post():
    with open('Config.json') as f:
        config = json.load(f)

    dt = datetime.datetime.today().strftime('%d-%m-%Y')
    dt2 = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%d-%m-%Y')

    if dt2 in config:
        for x in config[dt2]:
            content = ''
            for y in config[dt2][x]:
                content += f"{x}\n\n".replace('<replacestrongwithstart>', '<strong>').replace('<replacestrongwithend>', '</strong>')

            for guild in config['Guilds']:
                if y in config['Guilds'][guild]['Channels']:
                    url = config['Guilds'][guild]['URL']
                    user = config['Guilds'][guild]['Name']
                    password = config['Guilds'][guild]['Password']

                    title = f"stepn - {dt}"
                    url = f"{url}/wp-json/wp/v2/posts"
                    user = f"{user}"
                    password = f"{password}"
                    credentials = user + ':' + password
                    token = base64.b64encode(credentials.encode())
                    header = {'Authorization': 'Basic ' + token.decode('utf-8')}
                    post = {
                        'title': title,
                        'status': 'publish',
                        'content': content,
                        'categories': 6
                    }

                    response = requests.post(url, headers=header, json=post)

                    config.pop(dt2)
                    with open('Config.json', 'w') as f:
                        json.dump(config, f, indent=3)

                    break

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.guild is None:
        return

    channel = str(message.channel.id)
    with open('Config.json') as f:
        config = json.load(f)

    guild = str(message.guild.id)

    if guild not in config['Guilds']:
        return

    if int(channel) not in config['Guilds'][guild]['Channels']:
        return

    try:
        dt = datetime.datetime.today().strftime('%d-%m-%Y')
        dt2 = datetime.datetime.today().strftime('%H:%M')

        if dt not in config:
            config[dt] = {}

        if channel not in config[dt]:
            config[dt][channel] = []

        content = f"<replacestrongwithstart>{message.author.id}: {dt2}<replacestrongwithend>\n"

        if message.content == '':
            embed = message.embeds[0].to_dict()
            ct = embed['description']
        else:
            ct = message.content

        content += ct

        config[dt][channel].append(content)
        with open('Config.json', 'w') as f:
            json.dump(config, f, indent=3)

    except Exception as e:
        print(e)

@commands.has_permissions(administrator=True)
@bot.command()
async def setup(ctx):
    with open('Config.json') as f:
        config = json.load(f)

    guild = str(ctx.guild.id)

    try:
        await ctx.author.send('Please follow the following instructions to setup the BOT')
    except discord.Forbidden:
        await ctx.send(':warning: `---- USER DM ARE DISABLED ----')
        return

    def check(m):
        return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

    await ctx.author.send(':one: Please enter the website URL including http or https:')
    url = await bot.wait_for('message', check=check, timeout=120)
    url = url.content

    await ctx.author.send(':two: Please enter the website Username')
    username = await bot.wait_for('message', check=check, timeout=120)
    username = username.content

    await ctx.author.send(':three: Please enter the Application Password Generated from Plugin')
    password = await bot.wait_for('message', check=check, timeout=120)
    password = password.content

    config['Guilds'][guild] = {
        'URL': url,
        'Name': username,
        'Password': password,
        'Channels': []
    }

    await ctx.author.send(':white_check_mark: Website added. You can now set the channels using !addchannel COMMAND')

    with open('Config.json', 'w') as f:
        json.dump(config, f, indent=3)

@bot.command()
async def addchannel(ctx, channel: discord.TextChannel = None):
    if channel is None:
        await ctx.send(':warning: Command Usage: !addchannel #CHANNEL MENTION')
        return

    guild = str(ctx.guild.id)
    with open('Config.json') as f:
        config = json.load(f)

    if guild not in config['Guilds']:
        await ctx.send(':warning: Guild is not SET. Please setup using !setup')
        return

    if channel.id not in config['Guilds'][guild]['Channels']:
        config['Guilds'][guild]['Channels'].append(channel.id)
        with open('Config.json', 'w') as f:
            json.dump(config, f, indent=3)

    await ctx.send(':white_check_mark: Channel Added')

bot.run('TOKEN_ID')

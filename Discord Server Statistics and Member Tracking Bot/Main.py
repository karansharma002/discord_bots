import discord
from discord.ext import commands, tasks
import json
from datetime import datetime
import asyncio
import os

token = os.environ['TOKEN']
prefix = "-"

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

async def fetch():
    await bot.wait_until_ready()
    while True:
        try:
            guild = await bot.fetch_guild(gld)
            invs = await guild.invites()
        except:
            await asyncio.sleep(2)
            continue

        tmp = []
        for i in invs:
            for s in inv:
                if s[0] == i.code:
                    if int(i.uses) > s[1]:
                        gld = str(guild.id)
                        usr = guild.get_member(int(last))

                        channels = {"968840912560082984": 969506351648755766, "969506351426449458": 968840913042407435}
                        channel = await bot.fetch_channel(channels[gld])

                        msg = f"{usr.name} **joined**; Invited by **{i.inviter.name}**, Now Has (**{str(i.uses)}** invites)"
                        embed = discord.Embed(color=discord.Color.green())
                        embed.set_author(name=f"{usr.name} has Joined.", avatar=usr.avatar_url)
                        embed.add_field(name='Invited By', value=i.inviter.name, inline=False)
                        embed.add_field(name=f"{i.inviter.name} | Total Invites", value=i.uses, inline=False)

                        with open('Data.json') as f:
                            data = json.load(f)

                        if gld not in data:
                            break

                        inviter = str(i.inviter)

                        data[gld]['Most Invites'][inviter] = data[gld]['Most Invites'].get(inviter, 0) + 1

                        with open('Data.json', 'w') as f:
                            json.dump(data, f, indent=3)

            tmp.append(tuple((i.code, i.uses)))

        inv = tmp
        await asyncio.sleep(2)

@bot.event
async def on_member_join(member):
    welcome_channel = bot.get_channel(id)
    print(f"{member} has joined!")
    await welcome_channel.send(f"{member.mention} has joined the server! Thank you")
    try:
        embed = discord.Embed(title="Thank you for joining the Cross Tower Server",
                              description=f"Hey {member.display_name}! This server will keep you updated with all the new alerts and changes!",
                              colour=0xFF0000, timestamp=datetime.utcnow())
        fields = [("abcd", True), ("abcd", "abcd", True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.add_field(name="Joined On", value=str(datetime.now()))

        embed.set_author(name="CrossTower Bot", icon_url="")
        embed.set_footer(text="Cross Tower. Copyright ")
        embed.set_thumbnail(url="https://crosstower.com/wp-content/themes/crosstower/assets/dist/img/hero-logo.png")
        embed.set_image(url="https://crosstower.com/wp-content/themes/crosstower/assets/dist/img/hero-logo.png")
        await member.send(embed=embed)
        await member.send(file=discord.File("./data/images/giphy.gif"))

    except:
        await welcome_channel.send(f"{member.mention} I can't dm you, but thank you for joining!")

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    guild = str(message.guild.name)

    with open('Data.json') as f:
        data = json.load(f)

    if guild not in data:
        data[guild] = {}
        data[guild]['Total Messages'] = 0
        data[guild]['First_Message'] = message.content
        data[guild]['Most Active Channel'] = 'None'
        data[guild]['Most Active Users'] = []
        data[guild]['Channels'] = {}
        data[guild]['Most Invites'] = {}
        data[guild]['Most Active Voice'] = 'None'
        data[guild]['Word_Frequency'] = {}
        data[guild]['Online_Members'] = {}

    total_text_channels = len(message.guild.text_channels)
    total_voice_channels = len(message.guild.voice_channels)
    total_channels = total_text_channels + total_voice_channels

    data[guild]['Total Users'] = len(message.guild.members)
    data[guild]['Total Channels'] = total_channels
    data[guild]['Total Messages'] += 1

    if message.channel.name not in data[guild]['Channels']:
        data[guild]['Channels'][message.channel.name] = 1
    else:
        data[guild]['Channels'][message.channel.name] += 1

    with open('Cache.json') as f:
        cache = json.load(f)

    if guild not in cache:
        cache[guild] = {}
        cache[guild]['Users'] = {}

    author = str(message.author)

    if author not in cache[guild]['Users']:
        cache[guild]['Users'][author] = 0
    else:
        cache[guild]['Users'][author] += 1

    sorted_list = sorted(cache[guild]['Users'], key=cache[guild]['Users'].get, reverse=True)
    list1 = []
    for num, x in enumerate(sorted_list):
        if num == 2:
            break

        list1.append(x)

    data[guild]['Most Active Users'] = list1
    sorted_list = sorted(data[guild]['Channels'], key=data[guild]['Channels'].get, reverse=True)
    list1 = []
    for num, x in enumerate(sorted_list):
        if num == 1:
            break

        list1.append(x)

    data[guild]['Most Active Channel'] = list1
    data[guild]['Last_Message'] = message.content

    if 'Words' not in cache[guild]:
        cache[guild]['Words'] = []

    for x in cache[guild]['Words']:
        for y in message.content.split(' '):
            if y in x:
                data[guild]['Word_Frequency'][y] = data[guild]['Word_Frequency'].get(y, 0) + 1

    if message.content.split(' ') not in cache[guild]['Words']:
        cache[guild]['Words'].append(message.content.split(' '))

    with open('Data.json', 'w') as f:
        json.dump(data, f, indent=3)

    with open('Cache.json', 'w') as f:
        json.dump(cache, f, indent=3)

@bot.command()
async def send_message(ctx, user: discord.User = None, *, content: str = None):
    if not user or not content:
        await ctx.send(':information_source: Command Usage: !send_message @User <Content>')
        return
    try:
        await user.send(content)
    except:
        pass

    await ctx.send(':white_check_mark: Message Sent')

@bot.event
async def on_ready():
    print('---- The Bot Is Ready ----')
    await asyncio.gather(check_online_users.start(), fetch())

@tasks.loop(minutes=5)
async def check_online_users():
    for guild in bot.guilds:
        with open('Data.json') as f:
            data = json.load(f)

        online = sum(1 for member in guild.members if not member.bot and member.status in [discord.Status.online, discord.Status.do_not_disturb, discord.Status.idle])
        gld = str(guild.name)
        if gld not in data:
            continue

        time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        data[gld]['Online_Members'][time] = f"Total Online: {online}"

        with open('Data.json', 'w') as f:
            json.dump(data, f, indent=3)

bot.run(token)

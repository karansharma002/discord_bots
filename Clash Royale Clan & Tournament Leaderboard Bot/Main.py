import json
import requests
from discord.ext import commands, tasks
import discord
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CLASH_ROYALE_API_TOKEN = os.getenv('CLASH_ROYAL_API_TOKEN') #'your_clash_royale_api_token_here'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Bot is ready.')

@tasks.loop(hours=23)
async def extract():
    season = ''  # Define your season variable here
    if not season:
        return

    with open('Settings.json') as f:
        settings = json.load(f)

    if 'Channel' not in settings:
        return

    channel_id = settings['Channel']
    channel = bot.get_channel(channel_id)

    clan_tag = settings.get('Clan', '')
    headers = {'Authorization': f"Bearer {CLASH_ROYALE_API_TOKEN}"}
    params = {'clantag': clan_tag}

    # Extract clan members data
    r = requests.get(f'https://api.clashroyale.com/v1/clans/%23{clan_tag}/members', headers=headers, params=params)
    content = r.json()
    embed = discord.Embed(color=discord.Color.green(), title='TOP 10 CLAN MEMBERS', icon_url=bot.user.avatar_url)
    for x, user in enumerate(content['items'][:10]):
        name = user['name']
        tag = user['tag']
        trophies = user['trophies']
        rank = user['clanRank']
        donations = user['donations']
        role = user['role']
        embed.add_field(name=f'{x + 1}: {name.upper()}',
                        value=f"**Tag:** {tag}\n**Trophies:** {trophies}\n**Rank:** {rank}\n**Donations**: {donations}\n**Role:** {role}",
                        inline=False)

    await channel.send(embed=embed)

    # Extract tournament players data
    with open('Tournament.json') as f:
        tournament_data = json.load(f)

    sorted_tournament_data = sorted(tournament_data.items(), key=lambda x: x[1]['Score'], reverse=True)
    embed = discord.Embed(color=discord.Color.red(), title='TOP 3 Tournament Players', icon_url=bot.user.avatar_url)
    for x, (tag, data) in enumerate(sorted_tournament_data[:3]):
        name = data['Name']
        score = data['Score']
        embed.add_field(name=f'{x + 1}: {name.upper()}',
                        value=f"**Tag:** {tag}\n**Score:** {score}\n",
                        inline=False)

    await channel.send(embed=embed)

@commands.has_permissions(administrator=True)
@bot.command()
async def test(ctx):
    with open('ST.json') as f:
        settings = json.load(f)

    clan_tag = settings.get('Clan', '')
    headers = {'Authorization': f"Bearer {CLASH_ROYALE_API_TOKEN}", 'limit': 5}
    params = {'clantag': clan_tag}

    # Test clan members command
    r = requests.get(f'https://api.clashroyale.com/v1/clans/%23{clan_tag}/members', headers=headers, params=params)
    content = r.json()
    embed = discord.Embed(color=discord.Color.green(), title='TOP 5 RANKS')
    for x, user in enumerate(content['items'][:5]):
        name = user['name']
        tag = user['tag']
        trophies = user['trophies']
        rank = user['clanRank']
        embed.add_field(name=f'{x + 1}: {name.upper()}',
                        value=f"**Tag:** {tag}\n**Trophies:** {trophies}\n**Rank:** {rank}",
                        inline=False)

    await ctx.send(embed=embed)

    # Test tournament command
    tournament_id = settings.get('ID', '')
    r = requests.get(f'https://api.clashroyale.com/v1/tournaments/%23{tournament_id}', headers=headers, params=params)
    content = r.json()
    embed = discord.Embed(color=discord.Color.green(), title='TOP 3 TOURNAMENT PLAYERS')
    for x, user in enumerate(content['membersList'][:3]):
        tag = user['tag']
        name = user['name']
        score = user['score']
        rank = user['rank']
        embed.add_field(name=f'{x + 1}: {name.upper()}',
                        value=f"**Tag:** {tag}\n**Score:** {score}\n**Rank:** {rank}",
                        inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def setclan(ctx, clan: str = None):
    if not clan:
        await ctx.send(':information_source: !setclan `<CLAN ID>`')
        return

    with open('ST.json') as f:
        data = json.load(f)

    if '#' in clan:
        clan = clan.replace('#', '')
    data['Clan'] = clan

    with open('ST.json', 'w') as f:
        json.dump(data, f, indent=3)

    await ctx.send(':white_check_mark: Clan ID has been SET!')

@bot.command()
async def setchannel(ctx, channel: discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: !setchannel `#CHANNEL`')
        return

    with open('ST.json') as f:
        data = json.load(f)

    data['Channel'] = channel.id

    with open('ST.json', 'w') as f:
        json.dump(data, f, indent=3)

    await ctx.send(':white_check_mark: CHANNEL has been SET!')

@bot.command()
async def settournament(ctx, id_: str = None):
    if not id_:
        await ctx.send(':information_source: Usage: !settournament `<TOURNAMENT ID>`')
        return

    with open('ST.json') as f:
        data = json.load(f)

    if '#' in id_:
        id_ = id_.replace('#', '')

    data['ID'] = id_

    with open('ST.json', 'w') as f:
        json.dump(data, f, indent=3)

    await ctx.send(':white_check_mark: TOURNAMENT ID has been SET!')

    # Fetch and store the data of the new tournament
    headers = {'Authorization': f"Bearer {CLASH_ROYALE_API_TOKEN}"}
    params = {'clantag': id_}
    r = requests.get(f'https://api.clashroyale.com/v1/tournaments/%23{id_}', headers=headers, params=params)
    content = r.json()

    with open('Tournament.json') as f:
        tournament_data = json.load(f)

    for user in content['membersList']:
        tag = user['tag']
        name = user['name']
        score = user['score']
        if tag not in tournament_data:
            tournament_data[tag] = {}
            tournament_data[tag]['Name'] = name
            tournament_data[tag]['Score'] = int(score)
        else:
            tournament_data[tag]['Name'] = name
            tournament_data[tag]['Score'] += int(score)

    with open('Tournament.json', 'w') as f:
        json.dump(tournament_data, f, indent=3)

bot.run(TOKEN)

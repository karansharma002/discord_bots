import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import requests
import json
import random
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

DATA_FILE = 'Data.json'
KEYS_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = 'YOUR_SPREADSHEET ID'
SHEET_RANGE = 'Sheet1!A2:E'
TRIVIA_EMOJIS = ['🇦', '🇧', '🇨', '🇩']

@bot.event
async def on_ready():
    print('-- SERVER IS READY --')

def load_data():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=3)

def get_creds():
    return service_account.Credentials.from_service_account_file(KEYS_FILE, scopes=SCOPES)

@slash.slash(name="addbeca", description="Register the USER")
async def addbeca(ctx: SlashContext, user: discord.User, address: str, manager: discord.User):
    data = load_data()
    data[str(user.id)] = {'Address': address, 'Manager': manager.id}
    save_data(data)
    await ctx.send(':white_check_mark: User Registered')

@slash.slash(name="deletebeca", description="Remove the USER From Database")
async def deletebeca(ctx: SlashContext, user: discord.User):
    data = load_data()
    if str(user.id) in data:
        data.pop(str(user.id))
        save_data(data)
        await ctx.send(':white_check_mark: User Removed')
    else:
        await ctx.send(':warning: User is not Registered')

@slash.slash(name="beca", description='View the User Stats')
async def beca(ctx: SlashContext, user: discord.User):
    data = load_data()
    if str(user.id) not in data:
        await ctx.send(':warning: User is not registered.')
        return

    address = data[str(user.id)]['Address']
    manager = await bot.fetch_user(data[str(user.id)]['Manager'])

    try:
        mmr = requests.get(f'https://game-api.axie.technology/mmr/{address}').json()[0]['items'][0]['elo']
        r = requests.get(f'https://game-api.axie.technology/slp/{address}').json()
        last_games = requests.get(f'https://game-api.axie.technology/logs/pvp/{address}').json()

        last_matches = ''.join(['🟢 ' if game['winner'] == r[0]['client_id'] else '🔴 ' for game in last_games['battles'][:3]])

        tm1 = r[0]['blockchain_related']['signature']['timestamp']
        claim_date = datetime.utcfromtimestamp(int(tm1)) + timedelta(days=15)
        claim_status = 'Claim Available' if datetime.utcfromtimestamp(int(tm1)) >= datetime.now() else claim_date.strftime('%Y-%m-%d %H:%M:%S')

        embed = discord.Embed(color=discord.Color.green(), description=f"**{user.mention} | Stats**")
        embed.add_field(name='Wallet', value=f"> {address}", inline=False)
        embed.add_field(name='Manager', value=f"> {manager}", inline=False)
        embed.add_field(name='Last Matches', value=f"> {last_matches}", inline=False)
        embed.add_field(name='MMR', value=f"> {mmr}", inline=False)
        embed.add_field(name='Claimable', value=f"> {r[0]['claimable_total']}", inline=False)
        embed.add_field(name='Next Claim', value=f"> {claim_status}", inline=False)
        embed.add_field(name='Axies', value=f"[See axies](https://marketplace.axieinfinity.com/profile/{address}/axie/)", inline=False)

        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
        await ctx.send(':warning: Failed to fetch user stats.')

@slash.slash(name="leaderboard", description='View the Top Scholars')
async def leaderboard(ctx: SlashContext):
    data = load_data()
    latest_data = {}

    for user_id, info in data.items():
        address = info['Address']
        try:
            mmr = requests.get(f'https://game-api.axie.technology/mmr/{address}').json()[0]['items'][0]['elo']
            latest_data[user_id] = mmr
        except:
            latest_data[user_id] = 0

    sorted_data = sorted(latest_data.items(), key=lambda item: item[1], reverse=True)
    data_msg = '\n'.join([f"{num + 1}: <@{user_id}> | [{mmr}](https://marketplace.axieinfinity.com/profile/{data[user_id]['Address']})" for num, (user_id, mmr) in enumerate(sorted_data)])

    embed = discord.Embed(title='Top Scholars', description=data_msg, color=discord.Color.blurple())
    await ctx.send(embed=embed)

@slash.slash(name="scholars", description='View all the registered Scholars')
async def scholars(ctx: SlashContext):
    data = load_data()
    msg = '\n'.join([f"{num + 1}: <@{user_id}>: [View team](https://marketplace.axieinfinity.com/profile/{info['Address']}/axie/)" for num, (user_id, info) in enumerate(data.items())])

    embed = discord.Embed(title='Scholars List', description=msg, color=discord.Color.dark_grey())
    await ctx.send(embed=embed)

@slash.slash(name='reset', description='Reset the Trivia Progress and Start from the beginning')
async def reset(ctx: SlashContext):
    global participants, current_question, current_channel, current_list
    participants = []
    current_question = 0
    current_channel = 0
    current_list = []
    await ctx.send(':white_check_mark: Trivia Question Reset')

@slash.slash(name='trivia', description='Start the Trivia in the Given Channel')
async def trivia(ctx: SlashContext):
    global current_channel, current_list, current_question

    service = build('sheets', 'v4', credentials=get_creds())
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_RANGE).execute()
    values = result.get('values', [])

    if not values or current_question >= len(values):
        await ctx.send(':warning: No trivia questions available.')
        return

    current_channel = ctx.channel.id
    question_data = values[current_question]
    question, correct_answer, *choices = question_data
    random.shuffle(choices)

    embed = discord.Embed(color=discord.Color.dark_magenta(), description='\n'.join([f"{emoji} {choice}" for emoji, choice in zip(TRIVIA_EMOJIS, choices)]))
    embed.set_author(name=question, icon_url=bot.user.avatar_url)
    embed.set_footer(text='React Below with the CHOICE')

    msg = await ctx.send(embed=embed)
    for emoji in TRIVIA_EMOJIS:
        await msg.add_reaction(emoji)
    
    current_list = choices

@bot.event
async def on_raw_reaction_add(payload):
    global current_channel, current_question, participants, current_list

    if payload.user_id == bot.user.id or payload.channel_id != current_channel:
        return

    emoji = str(payload.emoji)
    if emoji not in TRIVIA_EMOJIS:
        return

    user = await bot.fetch_user(payload.user_id)
    if user.id in participants:
        await user.send('You have already submitted the answers for this question.')
        return

    service = build('sheets', 'v4', credentials=get_creds())
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_RANGE).execute()
    values = result.get('values', [])

    correct_answer = values[current_question][1]
    if current_list[TRIVIA_EMOJIS.index(emoji)] == correct_answer:
        channel = await bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.delete()
        await channel.send(f":tada: {user} has the correct answer. [{correct_answer}]")
        current_question += 1
    else:
        participants.append(user.id)
        await user.send('Oops, Wrong Answer.')

bot.run('YOUR_BOT_TOKEN')

import discord
from discord.ext import commands, tasks
import json
import asyncio
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Constants
NUMBER_START = 62
ST1_FILE = 'ST1.json'
ST2_FILE = 'ST2.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'keys.json'
FORM_1_SPREADSHEET_ID = '1F2Ho41gUDN0DOhihBl3b9GtTZjaApThIRDrLi267Iwc'
FORM_1_RANGE_NAME = 'Form Responses 1!A1:G'
FORM_2_SPREADSHEET_ID = '1ZDWSKyCMdTWAGCXUYbyOimBMOPPLHrof_EEOxztD4b0'
FORM_2_RANGE_NAME = 'Form Responses 1!A1:F'
GUILD_ID = 899316660014579752
ROLE_NAME = 'Testers'
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'  # Replace with your actual bot token

# Initialize bot
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
number = NUMBER_START

@bot.event
async def on_ready():
    print('-------- SERVER HAS STARTED -----------')
    await bot.wait_until_ready()
    fetch_form_2.start()
    await asyncio.sleep(10)
    fetch_form_1.start()

def load_json(filename):
    with open(filename) as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def get_google_sheets_service():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=creds)

async def process_form_response(settings, channel_id, values, form_key, number):
    channel = await bot.fetch_channel(channel_id)
    for num, row in enumerate(reversed(values)):
        if num == 4:
            break
        if 'Discord ID' in row[1] or row[0] in settings[form_key]:
            continue
        embed = discord.Embed(color=discord.Color.blue(), title=f"Report Number: {number}")
        for field, header in zip(row, values[0]):
            if 'Email ID' in header:
                continue
            embed.add_field(name=header, value=field or 'N/A', inline=False)
        message = await channel.send(embed=embed)
        settings[form_key].append(row[0])
        settings[str(number)] = message.id
        save_json(ST1_FILE, settings)
        number += 1

@tasks.loop(seconds=10)
async def fetch_form_1():
    try:
        settings = load_json(ST1_FILE)
        if 'Channel_1' not in settings:
            return
        service = get_google_sheets_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=FORM_1_SPREADSHEET_ID, range=FORM_1_RANGE_NAME).execute()
        values = result.get('values', [])
        if values:
            await process_form_response(settings, settings['Channel_1'], values, 'FORM_1', number)
    except Exception as e:
        print(f"Error in fetch_form_1: {e}")

@tasks.loop(minutes=1)
async def fetch_form_2():
    try:
        settings = load_json(ST2_FILE)
        if 'Channel_2' not in settings:
            return
        service = get_google_sheets_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=FORM_2_SPREADSHEET_ID, range=FORM_2_RANGE_NAME).execute()
        values = result.get('values', [])
        if values:
            await handle_form_2_responses(settings, values)
    except Exception as e:
        print(f"Error in fetch_form_2: {e}")

async def handle_form_2_responses(settings, values):
    channel = await bot.fetch_channel(settings['Channel_2'])
    guild = bot.get_guild(GUILD_ID)
    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    for num, row in enumerate(reversed(values)):
        if num >= 10 or row[1] in settings['FORM_2']:
            continue
        discord_id = [field for field, header in zip(row, values[0]) if 'Discord ID' in header][0]
        user = discord.utils.get(guild.members, name=discord_id.split('#')[0], discriminator=discord_id.split('#')[1]) if '#' in discord_id else await bot.fetch_user(discord_id)
        if user in guild.members and role not in user.roles:
            await user.add_roles(role)
            await channel.send(f'Added Role to {user}')
            settings['FORM_2'].append(row[1])
            save_json(ST2_FILE, settings)

@bot.command()
async def setchannel_1(ctx, channel: discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Command Usage: !setchannel_1 `<CHANNEL>`')
        return
    settings = load_json(ST1_FILE)
    settings['Channel_1'] = channel.id
    save_json(ST1_FILE, settings)
    await ctx.send(':white_check_mark: Channel has been added')

@bot.command()
async def setchannel_2(ctx, channel: discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Command Usage: !setchannel_2 `<CHANNEL>`')
        return
    settings = load_json(ST2_FILE)
    settings['Channel_2'] = channel.id
    save_json(ST2_FILE, settings)
    await ctx.send(':white_check_mark: Channel has been added')

bot.run(TOKEN)

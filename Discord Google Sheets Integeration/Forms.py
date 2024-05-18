import discord
from discord.ext import commands, tasks
from discord import Webhook, RequestsWebhookAdapter
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import json
import asyncio
import os
import itertools
import traceback

with open('api_tokens.json') as f:
    tokens = json.load(f)

# Discord bot token
TOKEN = tokens['discord_token']
# Google Sheets API credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'keys.json'
SAMPLE_SPREADSHEET_ID = '1aq9FHNnXJVVgFfXCL00tDHWhgnYoZ6itJXQ2H-yUByo'
SAMPLE_RANGE_NAME = 'Form responses 1!A1:G'

# Initialize bot
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('-------- SERVER HAS STARTED -----------')
    await bot.wait_until_ready()
    fetch_form_2.start()
    await asyncio.sleep(10)
    fetch_form_1.start()

@tasks.loop(seconds=50000)
async def fetch_form_1():
    try:
        with open('ST1.json') as f:
            settings = json.load(f)
        
        if 'Channel_1' not in settings:
            return

        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        
        if not values:
            return
        
        else:
            for num, x in enumerate(values[4:]):
                embed = discord.Embed(color=discord.Color.blue(), title='New Bug Report')
                for y, z in zip(x, values[0]):
                    if 'Email ID' in z or 'Timestamp' in z:
                        continue
                    
                    if y == '':
                        y = 'N/A'

                    embed.add_field(name=z, value=y, inline=False)
                
                try:
                    url = 'https://discord.com/api/webhooks/945351916228055110/ORSzfSArUQXkz8SuIEiWYL2wv30ZCAyhmVWUVWjgwfGZ0cvoKA4QS8E6XPhfWPg0Bln1'
                    webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
                    webhook.send(embed=embed)
                    settings['FORM_1'].append(x[0])
                    settings[str(number)] = msg.id
                    with open('ST1.json', 'w') as f:
                        json.dump(settings, f, indent=3)
                
                except:
                    pass
    except Exception as e:
        print(e)
        return

@bot.command()
async def status(ctx, num: str = None, type_: str = None):
    role1 = discord.utils.get(ctx.guild.roles, name='Developers')
    role2 = discord.utils.get(ctx.guild.roles, name='Administrators')
    role3 = discord.utils.get(ctx.guild.roles, name='Owners')

    if role1 in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles:
        if not num or not type_:
            await ctx.send(':information_source: Usage: !status `<REPORT NUMBER>` <`Status Name> `[Accepted/Rejected/Processing/Fixed]`')
            return

        keys_ = {'accepted': "⚪", 'rejected': '🔴', 'processing': '🔵', 'fixed': '✅'}

        with open('ST1.json') as f:
            settings = json.load(f)

        if num not in settings:
            await ctx.send(':warning: Invalid Report Number')
            return

        type_ = type_.lower()

        if type_ not in keys_:
            await ctx.send(':warning: Invalid Status Name')
            return

        ch = await bot.fetch_channel(909714201294028810)
        msg = await ch.fetch_message(settings[num])
        await msg.clear_reactions()
        await msg.add_reaction(keys_[type_])
        await ctx.message.add_reaction('✅')

@tasks.loop(hours=6)
async def fetch_form_2():
    try:
        vall = []
        list0 = os.listdir('ankles')
        list1 = os.listdir('extreme')
        list2 = os.listdir('fitness')
        list3 = os.listdir('gaming')
        list4 = os.listdir('Kindergarten')
        list5 = os.listdir('spring')
        list6 = os.listdir('street')
        list7 = os.listdir('swing')

        for combination in itertools.zip_longest(list0, list1, list2, list3, list4, list5, list6, list7):
            vall.append(combination)

        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        value_range_body = {
            'majorDimension': 'ROWS',
            'values': vall
        }

        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"Sheet1!A{gnum}", valueInputOption="USER_ENTERED", body={"values": vall}).execute()

    except Exception as e:
        traceback.print_exc()
        print(e)
        return

@bot.command()
async def setchannel_1(ctx, channel: discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Command Usage: !setchannel_1 `<CHANNEL WHERE FORMS ARE SENT>`')
        return

    with open('ST1.json') as f:
        settings = json.load(f)

    settings['Channel_1'] = channel.id
    with open('ST1.json', 'w') as f:
        json.dump(settings, f, indent=2)

    await ctx.send(':white_check_mark: Channel has been Added')

@bot.command()
async def setchannel_2(ctx, channel: discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Command Usage: !setchannel_2 `<CHANNEL WHERE FORMS ARE SENT>`')
        return

    with open('ST2.json') as f:
        settings = json.load(f)

    settings['Channel_2'] = channel.id
    with open('ST2.json', 'w') as f:
        json.dump(settings, f, indent=2)

    await ctx.send(':white_check_mark: Channel has been Added')

bot.run(TOKEN)

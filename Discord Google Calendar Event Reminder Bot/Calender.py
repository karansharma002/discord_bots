from discord.ext import commands, tasks
import json
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
from dateutil import parser

sent_events = []
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('===== STARTED SERVER =======')
    await bot.wait_until_ready()
    fetch_data.start()

@tasks.loop(minutes=1)
async def fetch_data():
    with open('Config.json') as f:
        cf = json.load(f)
    
    channel_id = cf.get('Channel')
    if not channel_id:
        return

    channel = await bot.fetch_channel(channel_id)
    service = build('calendar', 'v3', credentials=get_credentials())

    now = datetime.utcnow().isoformat() 
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=100, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    for event in events:
        start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date'))
        event_name = event.get('summary', 'Event')

        if start not in sent_events:
            start_time = parser.parse(start)
            time_diff = (start_time - datetime.now()).total_seconds() / 60

            if time_diff <= 30:
                embed = create_embed(cf.get('Text', ''), event_name)
                await channel.send(embed=embed)
                sent_events.append(start)

@bot.command()
async def addtext(ctx, *, text: str = None):
    if not text:
        await ctx.send(':information_source: Usage: !addtext TEXT')
        return

    with open('Config.json') as f:
        config = json.load(f)
    
    config['Text'] = text

    with open('Config.json', 'w') as f:
        json.dump(config, f, indent=3)
    
    await ctx.send('Text Modified!!')

@bot.command()
async def setchannel(ctx, channel: commands.TextChannelConverter = None):
    if not channel:
        await ctx.send(':information_source: Usage: !setchannel #CHANNEL')
        return

    with open('Config.json') as f:
        config = json.load(f)
    
    config['Channel'] = channel.id

    with open('Config.json', 'w') as f:
        json.dump(config, f, indent=3)
    
    await ctx.send('Channel Modified!!')

def create_embed(text, event_name):
    embed = discord.Embed(description=text, color=discord.Color.green())
    embed.set_author(name=f'Event Alert | {event_name}', icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.utcnow()
    return embed

def get_credentials():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    SERVICE_ACCOUNT_FILE = 'keys.json'
    return service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

bot.run('YOUR_TOKEN')

import discord
from discord.ext import commands, tasks
import json
from datetime import datetime, timedelta
from dateutil import parser
import os

bot = commands.Bot(command_prefix='%')

@bot.event
async def on_ready():
    print('---------- SERVER HAS STARTED ---------')
    trigger.start()

@tasks.loop(minutes=1)
async def trigger():
    with open('Settings.json') as f:
        s = json.load(f)
    
    for i in range(1, 3):
        time_key = f'TIME{i}'
        if time_key not in s or 'COMMAND' not in s or 'Channel' not in s:
            continue
        
        try:
            time_value = parser.parse(s[time_key])
            current_time = datetime.utcnow()
            if time_value <= current_time:
                cmd = s['COMMAND']
                channel = await bot.fetch_channel(s['Channel'])
                await channel.send(cmd)
                s[time_key] = (current_time + timedelta(days=1)).strftime('%d/%m/%y %H:%M:%S')
        except Exception as e:
            print(f"Error occurred: {e}")

    with open('Settings.json', 'w') as f:
        json.dump(s, f, indent=3)

@bot.command()
async def setchannel(ctx, channel: discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !setchannel `<CHANNEL WHERE THE COMMAND IS EXECUTED>`')
        return

    with open('Settings.json', 'r') as f:
        settings = json.load(f)

    settings['Channel'] = channel.id

    with open('Settings.json', 'w') as f:
        json.dump(settings, f, indent=3)
    
    await ctx.send(':white_check_mark: Channel has been set')  

@bot.command()
async def settime(ctx, var1: str = None, var2: str = None):
    if not var1 or not var2:
        await ctx.send(':information_source: Usage: !settime `<TIME1>` `<TIME2>` `(EXAMPLE: 04:10 HH:MM)`')
        return
    
    try:
        dt = datetime.utcnow()
        settings = {}
        for i, var in enumerate([var1, var2], start=1):
            time_val = parser.parse(var)
            time_str = (dt.replace(hour=time_val.hour, minute=time_val.minute) + timedelta(days=(1 if time_val < dt else 0))).strftime('%d/%m/%y %H:%M:%S')
            settings[f'TIME{i}'] = time_str

        with open('Settings.json', 'w') as f:
            json.dump(settings, f, indent=3)

        await ctx.send(':white_check_mark: Time has been set')
    except Exception as e:
        print(f"Error occurred: {e}")
        await ctx.send(':warning: Invalid Format')

@bot.command()
async def setcommand(ctx, *, var: str = None):
    if not var:
        await ctx.send(':information_source: Usage: !setcommand `<COMMAND NAME TO TRIGGER>`')
        return
    
    with open('Settings.json') as f:
        settings = json.load(f)
    
    settings['COMMAND'] = var

    with open('Settings.json', 'w') as f:
        json.dump(settings, f, indent=3)
    
    await ctx.send(':white_check_mark: Command has been set')

bot.run(os.getenv('BOT_TOKEN'))

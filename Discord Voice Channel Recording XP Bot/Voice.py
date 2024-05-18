import discord
import datetime
import json

from discord.ext import tasks

bot = discord.Bot(command_prefix='!')

guild_id = 0
channel_id = 0

@tasks.loop(minutes=45)
async def extract_data():
    try:
        dta = datetime.datetime.now().strftime('%H:%M')
        if dta == '12:00':
            
            guild = bot.get_guild(guild_id)  
            voice_channel = guild.get_channel(channel_id) 
            voice_client = await voice_channel.connect()
            voice_client.start_recording(discord.sinks.MP3Sink(), finished_callback)

    except Exception as e:
        print(e)

async def finished_callback(sink):
    print(sink.audio_data.items())
    print(sink.audio_data)
    recorded_users = [
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]

    data = {}
    for x in files:
        data[x.filename] = {
            'Duration': x.duration,
            'File': x
        }

    with open('Data.json', 'w') as f:
        json.dump(data, f, indent=3)

@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user:
        return

    if not before.channel and after.channel:
        try:
            guild = member.guild
            voice_channel = member.voice.channel
            voice_client = await voice_channel.connect()
            voice_client.start_recording(discord.sinks.MP3Sink(), finished_callback)

        except Exception as e:
            print(e)

bot.run('TOKEN_ID')

import os
import json
import requests
import discord
from discord.ext import commands, tasks
import tweepy
import asyncio
from discord import Webhook, RequestsWebhookAdapter
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
SUGARBOUNCE_EMAIL = os.getenv('SUGARBOUNCE_EMAIL')
SUGARBOUNCE_PASSWORD = os.getenv('SUGARBOUNCE_PASSWORD')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Initialize Discord bot
bot = commands.Bot(command_prefix='.')

# API endpoints
SUGARBOUNCE_AUTH_URL = 'https://streams.sugarbounce.com/api/auth/token'
SUGARBOUNCE_STREAMS_URL = 'https://streams.sugarbounce.com/api/discord/streams?type=public&active=true&order=date'
SUGARBOUNCE_TIPS_URL = 'https://streams.sugarbounce.com/api/discord/tips/'
COINGECKO_URL = 'https://api.coingecko.com/api/v3/coins/binance-smart-chain/contract/0x40f906e19b14100d5247686e08053c4873c66192'

# Global variables
online_streamers = []
lives_data = []
tips_data = []
now_online = {}
payload = {
    "email": SUGARBOUNCE_EMAIL,
    "password": SUGARBOUNCE_PASSWORD
}

@bot.event
async def on_ready():
    print('------- SERVER STARTED -------')
    update_status.start()
    bot.loop.create_task(fetch_lives())
    bot.loop.create_task(fetch_tips())

@tasks.loop(seconds=30)
async def update_status():
    response = requests.get(COINGECKO_URL)
    data = response.json()

    current_price = round(data['market_data']['current_price']['usd'], 2)
    price_change = round(data['market_data']['price_change_percentage_24h'], 1)
    price_change_str = f'↗ {price_change}' if price_change >= 0 else f'↙ {price_change}'

    description = f"${current_price} {price_change_str}%"
    await bot.change_presence(activity=discord.Game(name=description))

async def fetch_lives():
    global lives_data, now_online

    await bot.wait_until_ready()
    while True:
        token = get_sugarbounce_token()
        if not token:
            await asyncio.sleep(60)
            continue

        headers = {'authorization': token}
        while True:
            try:
                response = requests.get(SUGARBOUNCE_STREAMS_URL, headers=headers)
                data = response.json()['data']

                online_lives = []
                for stream in data:
                    process_live_stream(stream, online_lives)

                await update_online_status(online_lives)
                await asyncio.sleep(30)

            except Exception as e:
                print(f"Error fetching live streams: {e}")
                break

async def fetch_tips():
    global tips_data

    await bot.wait_until_ready()
    while True:
        token = get_sugarbounce_token()
        if not token:
            await asyncio.sleep(60)
            continue

        headers = {'authorization': token}
        while True:
            try:
                response = requests.get(SUGARBOUNCE_TIPS_URL, headers=headers)
                data = response.json()['data']

                for tip in data:
                    process_tip(tip)

                await asyncio.sleep(30)

            except Exception as e:
                print(f"Error fetching tips: {e}")
                break

def get_sugarbounce_token():
    try:
        response = requests.post(SUGARBOUNCE_AUTH_URL, data=payload)
        response_data = response.json()
        return response_data['data']
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

def process_live_stream(stream, online_lives):
    try:
        discord_id = stream['user']['discordId']
        guild = bot.fetch_guild(941159396128485376)
        role = discord.utils.get(guild.roles, id=956202133991092244)
        member = bot.fetch_member(int(discord_id))

        member.add_roles(role)
        now_online[stream['_id']] = discord_id

        online_lives.append(stream['_id'])
        if stream['_id'] not in lives_data:
            send_live_notification(stream)
            lives_data.append(stream['_id'])

    except Exception as e:
        print(f"Error processing live stream: {e}")

def send_live_notification(stream):
    try:
        user = stream['user']
        profile_img = user.get('profileImg', 'NONE')
        thumbnail = stream['image']
        link = f"https://streams.sugarbounce.com/stream/{stream['userId']}"

        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name=f"🎦 {user['name']} is now LIVE!!", icon_url=f"https://streams.sugarbounce.com/api{profile_img}")
        embed.set_image(url=f"https://streams.sugarbounce.com/api{thumbnail}")
        embed.add_field(name='Stream Name', value=stream['user']['name'], inline=False)
        embed.add_field(name='Gender', value=stream['gender'].title(), inline=False)
        embed.add_field(name='Stream URL', value=f"[Click Here]({link})", inline=False)

        webhook = Webhook.from_url(WEBHOOK_URL, adapter=RequestsWebhookAdapter())
        webhook.send(embed=embed)

    except Exception as e:
        print(f"Error sending live notification: {e}")

def process_tip(tip):
    try:
        if tip['_id'] not in tips_data:
            tip_receiver = tip['tipReceiver']['name']
            tip_payer = tip['tipPayer']['name']
            amount = tip['amount']

            embed = discord.Embed(color=discord.Color.green(), title=f"💵 {tip_payer} has tipped {tip_receiver} 💵")
            embed.add_field(name='$Tip Amount', value=amount, inline=False)

            webhook = Webhook.from_url(WEBHOOK_URL, adapter=RequestsWebhookAdapter())
            webhook.send(embed=embed)
            tips_data.append(tip['_id'])

    except Exception as e:
        print(f"Error processing tip: {e}")

async def update_online_status(online_lives):
    try:
        for stream_id in list(now_online):
            if stream_id not in online_lives:
                guild = await bot.fetch_guild(941159396128485376)
                role = discord.utils.get(guild.roles, id=956202133991092244)
                member = await guild.fetch_member(int(now_online[stream_id]))
                await member.remove_roles(role)
                now_online.pop(stream_id)

        for stream_id in list(lives_data):
            if stream_id not in online_lives:
                lives_data.remove(stream_id)

        print(lives_data)
        print(online_lives)

    except Exception as e:
        print(f"Error updating online status: {e}")

bot.run(DISCORD_TOKEN)

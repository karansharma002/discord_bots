import requests
import json
import discord
from discord.ext import commands
from aiohttp import ClientSession
import web3
import os

TOKEN = os.environ['TOKEN']

ETH_WEI_FACTOR = 10 ** 18

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

def convert_to_eth(amount):
    eth_amount = web3.Web3.fromWei(amount, 'ether')
    return float(eth_amount)

async def send_webhook(embed, webhook_url):
    async with ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_url, adapter=discord.AsyncWebhookAdapter(session))
        await webhook.send(embed=embed)

async def process_selene_message(message, uno_price):
    filtered_data = message.content.split('\n')
    filtered_data = [x.strip(' ') for x in filtered_data]
    amount = int(filtered_data[0].split(':')[1])
    am_eth = convert_to_eth(amount)
    amount_usd = round(am_eth * uno_price)
    pool, staker = filtered_data[1], filtered_data[2]
    capacity_change = 'reduced' if pool == staker else 'increased'
    await message.channel.send(f'**Selene** Capacity {capacity_change} by: {amount_usd} USD')
    await message.delete()

async def process_loan_message(message):
    pass

async def process_low_balance_message(message):
    pass

@bot.event
async def on_ready():
    print('READY')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == 978322782318387201:
        try:
            r = requests.get('https://api.coingecko.com/api/v3/coins/binance-smart-chain/contract/0x474021845c4643113458ea4414bdb7fb74a01a77')
            data = json.loads(r.content)
            uno_price = round(data['market_data']['current_price']['usd'], 2)
            filtered_data = message.content.split('\n')
            filtered_data = [x.strip(' ') for x in filtered_data]
            name = filtered_data[0].split(':')[0]
            if name == 'Selene':
                await process_selene_message(message, uno_price)
            else:
                amount = int(filtered_data[0].split(':')[1])
                am_eth = convert_to_eth(amount)
                amount_usd = round(am_eth * uno_price)
                pool, staker = filtered_data[1], filtered_data[2]
                capacity_change = 'reduced' if pool == staker else 'increased'
                await message.channel.send(f'**{name}** Capacity {capacity_change} by: {amount_usd} USD')
                await message.delete()
        except Exception as e:
            print(f"Error processing message in channel : {e}")

    elif message.channel.id == 0:
        try:
            await process_loan_message(message)
        except Exception as e:
            print(f"Error processing message in channel : {e}")

    elif message.channel.id == 0:
        try:
            await process_low_balance_message(message)
        except Exception as e:
            print(f"Error processing message in channel : {e}")

bot.run(TOKEN)

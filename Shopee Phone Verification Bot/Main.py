import requests
import time
import asyncio
import json
import pyshopee
import discord
from discord.ext import commands
import datetime


client = pyshopee.Client(0, 0, '')  # Replace with your Shopee credentials
COUNTY_CODE = '+'  # Adjust if needed

bot = commands.Bot(command_prefix='=')

@bot.event
async def on_ready():
    print('--------- STARTED SHOPEE SERVER -------------')

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=3)

async def send_embed(channel, description, color=discord.Color.blue()):
    embed = discord.Embed(description=description, color=color)
    return await channel.send(embed=embed)

async def wait_for_reaction(ctx, message, emoji_list):
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in emoji_list and reaction.message.id == message.id
    reaction, user = await bot.wait_for('reaction_add', check=check, timeout=60)
    return reaction.emoji

@bot.command()
async def purchase(ctx):
    global COUNTY_CODE
    KEY = 'b395149d4b5bb7cb969f5ce27d536Ae3'
    embed = discord.Embed(description=f'{ctx.author.mention}\nHi there, please create ticket with react 📩', color=discord.Color.blue())
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('📩')
    reaction = await wait_for_reaction(ctx, msg, ['📩'])

    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    channel = await ctx.guild.create_text_channel(f'{ctx.author.name}-transcript', overwrites=overwrites)

    while True:
        embed = discord.Embed(description=f'Hi, {ctx.author.mention}, how can I help you today? ^_^\n\n📱 Claim Number\n💰 Check Balance\n🔒 Close', color=discord.Color.blue())
        await msg.delete()
        msg = await channel.send(embed=embed)
        for x in ('📱', '💰', '🔒'):
            await msg.add_reaction(x)

        reaction = await wait_for_reaction(ctx, msg, ['📱', '💰', '🔒'])
        if reaction == '📱':
            data = load_json('Data.json')
            if str(ctx.author.id) not in data or data[str(ctx.author.id)] < 0.85:
                await send_embed(msg, 'INSUFFICIENT BALANCE', discord.Color.red())
                return

            embed = discord.Embed(description=f'May I know which country number should you take?\n\n🇮🇩 Indonesia\n🇻🇳 Vietnam\n🔒 Close', color=discord.Color.blue())
            await msg.delete()
            msg = await channel.send(embed=embed)
            for x in ('🇮🇩', '🇻🇳', '🔒'):
                await msg.add_reaction(x)

            reaction = await wait_for_reaction(ctx, msg, ['🇮🇩', '🇻🇳', '🔒'])
            if reaction == '🇮🇩':
                COUNTY = 6
            elif reaction == '🇻🇳':
                COUNTY = 10
            else:
                await send_embed(channel, 'TICKET CLOSED', discord.Color.red())
                await channel.delete()
                return

            CANCEL = -1
            CONFIRM = 1
            RESEND = 3
            END = 6

            while True:
                url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={KEY}&action=getNumber&service=nz&country={COUNTY}&freePrice=false&maxPrice=1000'
                r = requests.get(url)
                content = r.text.split(':')
                if len(content) < 3:
                    continue

                STATUS, ID, NUMBER = content[0], content[1], content[2]
                embed = discord.Embed(title=f"{COUNTY_CODE}{NUMBER}", description='Please click Waiting Code when you’re waiting for it.\n\nRemark:\n\nIf you do not want to use this number, click Reset. If not, we will deduct your balance after 20 mins.\n⏳ Waiting Code\n❌ Reset', color=discord.Color.blue())
                await msg.delete()
                msg = await channel.send(embed=embed)
                for x in ('⏳', '❌'):
                    await msg.add_reaction(x)

                reaction = await wait_for_reaction(ctx, msg, ['⏳', '❌'])
                if reaction == '❌':
                    url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={KEY}&action=setStatus&status=-1&id={ID}'
                    requests.get(url)
                    break

                elif reaction == '⏳':
                    url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={KEY}&action=setStatus&status=1&id={ID}'
                    requests.get(url)
                    embed = discord.Embed(description='Please wait for a moment ya. During seeking for your code.\n\nIt may take up to 30sec to 1 minute.', color=discord.Color.blue())
                    await msg.delete()
                    msg = await channel.send(embed=embed)
                    endTime = datetime.datetime.now() + datetime.timedelta(minutes=1)

                    while True:
                        url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={KEY}&action=getStatus&id={ID}'
                        r = requests.get(url)
                        status_response = r.text.split(':')
                        status = status_response[0]
                        code = status_response[1] if len(status_response) > 1 else None

                        if status == 'STATUS_OK':
                            embed = discord.Embed(title=f'Woahh! I found your code: [{code}]', description='Remember key in Voucher Code before page order ya.\n\nFor the voucher, you may refer to #VoucherChannel', color=discord.Color.blue())
                            await msg.delete()
                            msg = await channel.send(embed=embed)
                            await msg.add_reaction('🔒')
                            data[str(ctx.author.id)] -= 0.85 if COUNTY == 6 else 1
                            save_json('Data.json', data)

                            reaction = await wait_for_reaction(ctx, msg, ['🔒'])
                            if reaction == '🔒':
                                await send_embed(channel, 'TICKET CLOSED', discord.Color.red())
                                await channel.delete()
                                return

                            url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={KEY}&action=setStatus&status=6&id={ID}'
                            requests.get(url)

                        if datetime.datetime.now() >= endTime:
                            cont = 'Uh-Oh~ I did’t get your code. Can you press resend for 1 time?\n\nOr click Reset get another new number.\n\nThanks ^-^ Still no code? Please refer to #Help-Channel'
                            embed = discord.Embed(description=cont, color=discord.Color.blue())
                            await msg.delete()
                            msg = await channel.send(embed=embed)
                            for x in ('⏳', '❌'):
                                await msg.add_reaction(x)

                            reaction = await wait_for_reaction(ctx, msg, ['⏳', '❌'])
                            if reaction == '❌':
                                break

                        await asyncio.sleep(1)

        elif reaction == '🔒':
            await send_embed(channel, 'TICKET CLOSED', discord.Color.red())
            await channel.delete()
            return

        elif reaction == '💰':
            data = load_json('Data.json')
            bal = data.get(str(ctx.author.id), 0)
            embed = discord.Embed(description=f'Hi [{ctx.author.mention}], you have current [{bal} Points].\n\nMay I know what can I assist you? ^-^\n\n📱 Claim Number\n👛 Redeem Balance\n🔒 Close', color=discord.Color.blue())
            await msg.delete()
            msg = await channel.send(embed=embed)
            for x in ('📱', '👛', '🔒'):
                await msg.add_reaction(x)

            reaction = await wait_for_reaction(ctx, msg, ['📱', '👛', '🔒'])
            if reaction == '🔒':
                await send_embed(channel, 'TICKET CLOSED', discord.Color.red())
                await channel.delete()
                return

            elif reaction == '📱':
                if str(ctx.author.id) not in data or data[str(ctx.author.id)] < 0.85:
                    await send_embed(msg, 'INSUFFICIENT BALANCE', discord.Color.red())
                    return

                embed = discord.Embed(description=f'May I know which country number should you take?\n\n🇮🇩 Indonesia\n🇻🇳 Vietnam\n🔒 Close', color=discord.Color.blue())
                await msg.delete()
                msg = await channel.send(embed=embed)
                for x in ('🇮🇩', '🇻🇳', '🔒'):
                    await msg.add_reaction(x)

                reaction = await wait_for_reaction(ctx, msg, ['🇮🇩', '🇻🇳', '🔒'])
                if reaction == '🇮🇩':
                    COUNTY = 6
                elif reaction == '🇻🇳':
                    COUNTY = 10
                else:
                    await send_embed(channel, 'TICKET CLOSED', discord.Color.red())
                    await channel.delete()
                    return

                CANCEL = -1
                CONFIRM = 1
                RESEND = 3
                END = 6

                while True:
                    url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={KEY}&action=getNumber&service=nz&country={COUNTY}&freePrice=false&maxPrice=1000'
                    r = requests.get(url)
                    content = r.text.split(':')
                    if len(content) < 3:
                        continue

                    STATUS, ID, NUMBER = content[0], content[1], content[2]
                    embed = discord.Embed(title=f"{COUNTY_CODE}{NUMBER}", description='Please click Waiting Code when you’re waiting for it.\n\nRemark:\n\nIf you do not want to use this number, click Reset. If not, we will deduct your balance after 20 mins.\n⏳ Waiting Code\n❌ Reset', color=discord.Color.blue())
                    await msg.delete()
                    msg = await channel.send(embed=embed)
                    for x in ('⏳', '❌'):
                        await msg.add_reaction(x)

                    reaction = await wait_for_reaction(ctx, msg, ['⏳', '❌'])
                    if reaction == '❌':
                        url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={KEY}&action=setStatus&status=-1&id={ID}'
                        requests.get(url)
                        break

                    elif reaction == '⏳':
                        url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={KEY}&action=setStatus&status=1&id={ID}'
                        requests.get(url)
                        embed = discord.Embed(description='Please wait for a moment ya. During seeking for your code.\n\nIt may take up to 30sec to 1 minute.', color=discord.Color.blue())
                        await msg.delete()
                        msg = await channel.send(embed=embed)
                        endTime = datetime.datetime.now() + datetime.timedelta(minutes=1)

                        while True:
                            url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={KEY}&action=getStatus&id={ID}'
                            r = requests.get(url)
                            status_response = r.text.split(':')
                            status = status_response[0]
                            code = status_response[1] if len(status_response) > 1 else None

                            if status == 'STATUS_OK':
                                embed = discord.Embed(title=f'Woahh! I found your code: [{code}]', description='Remember key in Voucher Code before page order ya.\n\nFor the voucher, you may refer to #VoucherChannel', color=discord.Color.blue())
                                await msg.delete()
                                msg = await channel.send(embed=embed)
                                await msg.add_reaction('🔒')
                                data[str(ctx.author.id)] -= 0.85 if COUNTY == 6 else 1
                                save_json('Data.json', data)

                                reaction = await wait_for_reaction(ctx, msg, ['🔒'])
                                if reaction == '🔒':
                                    await send_embed(channel, 'TICKET CLOSED', discord.Color.red())
                                    await channel.delete()
                                    return

                                url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={KEY}&action=setStatus&status=6&id={ID}'
                                requests.get(url)

                            if datetime.datetime.now() >= endTime:
                                cont = 'Uh-Oh~ I did’t get your code. Can you press resend for 1 time?\n\nOr click Reset get another new number.\n\nThanks ^-^ Still no code? Please refer to #Help-Channel'
                                embed = discord.Embed(description=cont, color=discord.Color.blue())
                                await msg.delete()
                                msg = await channel.send(embed=embed)
                                for x in ('⏳', '❌'):
                                    await msg.add_reaction(x)

                                reaction = await wait_for_reaction(ctx, msg, ['⏳', '❌'])
                                if reaction == '❌':
                                    break

                            await asyncio.sleep(1)

@bot.command()
async def add(ctx, amount: float):
    data = load_json('Data.json')
    data[str(ctx.author.id)] = data.get(str(ctx.author.id), 0) + amount
    save_json('Data.json', data)
    await send_embed(ctx, f"Added {amount} points to your balance.", discord.Color.green())

@bot.command()
async def check_balance(ctx):
    data = load_json('Data.json')
    balance = data.get(str(ctx.author.id), 0)
    await send_embed(ctx, f"You have {balance} points.", discord.Color.green())

if __name__ == "__main__":
    bot.run("YOUR_DISCORD_BOT_TOKEN")

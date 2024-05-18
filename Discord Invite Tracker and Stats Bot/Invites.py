import discord
from discord.ext import commands, tasks
import json
import requests
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import os

gld = 0
invites = {}
last = ""

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

async def fetch():
    global last, invites
    await bot.wait_until_ready()
    guild = await bot.fetch_guild(gld)
    while True:
        try:
            invs = await guild.invites()
            tmp = []
            for i in invs:
                for s in invites:
                    if s[0] == i.code and int(i.uses) > s[1]:
                        usr = guild.get_member(int(last))
                        author = str(i.inviter.id)
                        with open('Data.json') as f:
                            data = json.load(f)
                        if author not in data:
                            data[author] = 0
                        data[author] += 1
                        with open('Data.json', 'w') as f:
                            json.dump(data, f, indent=3)
                tmp.append((i.code, i.uses))
            invites = tmp
        except Exception as e:
            print(f"Error fetching invites: {e}")
        await asyncio.sleep(2)

@bot.event
async def on_ready():
    print("Bot is ready!")
    await bot.change_presence(activity=discord.Activity(name="joins", type=2))

@bot.event
async def on_member_join(member):
    global last
    last = str(member.id)
    gld = member.guild.id

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command()
async def invites(ctx, member: discord.Member):
    with open('Data.json') as f:
        data = json.load(f)
    total_invites = sum(i.uses for i in await member.guild.invites() if i.inviter == member)
    msg = f'You currently have **{total_invites}** invites.'
    embed = discord.Embed(color=discord.Color.dark_blue(), title=str(member), description=msg)
    await member.send(embed=embed)

@bot.command(aliases=['top'])
async def leaderboard(ctx):
    with open('Data.json') as f:
        data = json.load(f)
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    msg = '\n'.join(f"{num+1}: {await bot.fetch_user(int(user_id))} - **{points}** Invites"
                    for num, (user_id, points) in enumerate(sorted_data[:20]))
    embed = discord.Embed(color=discord.Color.dark_blue(), title='TOP Inviters', description=msg)
    await ctx.send(embed=embed)

@bot.command()
async def reset(ctx, confirm: str = None):
    if confirm == "confirm":
        with open('Data.json', 'w') as f:
            json.dump({}, f, indent=3)
        await ctx.send(':white_check_mark: Leaderboard Reset!')
    else:
        await ctx.send(':warning: The leaderboard will reset. Type: !reset confirm to reset the data.')

@bot.command()
async def stats(ctx):
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options)

    driver.get(url2)
    await asyncio.sleep(2)

    try:
        txs_1 = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div/div[2]/table/tbody/tr[1]/td[2]/span/a').text
        contract_1 = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div/div[2]/table/tbody/tr[1]/td[9]/a/span[1]/font').text

    
    except NoSuchElementException as e:
        await ctx.send("Error fetching transaction details.")
        driver.quit()
        return

    embed = discord.Embed(color=discord.Color.green())
    url = 'https://api.bscscan.com/api?module=account&action=balance&address=0x000000000000000000000000000000000000dead&apikey=3VDH63XMTZ1EBSEV17MKQ4GJDWT2YSGC8X'
    r = requests.get(url).json()
    bal = r['result']
    embed.add_field(name='BNB Balance', value=bal, inline=False)
    embed.add_field(name='ERC-720 Last Burn', value=f'**Hash:** __{txs_1}__\n**Contract:** __{contract_1}__', inline=False)
    await ctx.send(embed=embed)
    driver.quit()

bot.loop.create_task(fetch())
bot.run(os.environ['TOKEN'])

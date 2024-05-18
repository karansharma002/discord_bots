import discord 
from discord.ext import commands
import json
import re
import os
from datetime import datetime, timedelta
import requests
import asyncio
import random
from discord_slash import SlashCommand

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)



# Configuration
CHANNEL_ID = 0 # CHANNEL ID WHERE COMMAND USED LOGS GOES
DEFAULT_BCH_VALUE = 0.0001
SPAM_CHANNEL_ID = 713279940971331635  
WITHDRAWAL_FEE = 25  # in Pocket Coins
PAYPAL_WITHDRAWAL_FEE_PERCENT = 0.035
PAYPAL_DEPOSIT_FEE_PERCENT = 0.015
bch = 0.0001

# Load Data
try:
    with open('Config/Data.json') as f:
        data = json.load(f)
    with open('Config/Transactions.json') as f:
        transactions = json.load(f)
except FileNotFoundError:
    data = {}
    transactions = {"Deposited": 0, "Withdrawn": 0, "Sent": 0}

bot.remove_command('help')

async def ch_pr():
  await bot.wait_until_ready()
  while not bot.is_closed():
    with open('Config/Transactions.json') as f:
      transactions = json.load(f)
      deposits = transactions['Deposited']

    response_API = requests.get('https://api.binance.com/api/v3/avgPrice?symbol=BCHUSDT')
    data = response_API.json()
    price = float(data['price'])
    usd = price * .0001
    pdeposits = deposits * usd
    statuses = [f"Monitoring Trades Across {len(bot.guilds)} Servers", "!help For Commands", "v2.5", f"{round(deposits, 2)} Deposited Since Launch"]
    status = random.choice(statuses)
    await bot.change_presence(activity=discord.Game(name=status))
    await asyncio.sleep(45)

@bot.event
async def on_message(m):
  if m.author == bot.user or m.author.bot:
    return

  chance = 25
  if m.channel.id == 713279940971331635:
    if random.randrange(100) <= chance:
      with open('Config/Data.json') as f:
        data = json.load(f)

      id_ = str(m.author.id)
      if id_ not in data:
        data[id_] = {}
        data[id_]['Coins'] = 0

      coins = random.randint(10, 50)

      await m.channel.send(f"{m.author.mention} has found {coins} <:PocketCoin:883693571792842802>")

      data[id_]['Coins'] += coins
      data['559799889039589386']['Coins'] -= coins
      with open('Config/Data.json', 'w') as f:
        json.dump(data, f, indent=3)

  await bot.process_commands(m)


@bot.event
async def on_ready():
  print('-------------- PocketBot is alive ---------------')
  guild_count = 0
  for guild in bot.guilds:
    print(f"-{guild.id} (name: {guild.name})")
    guild_count += 1
  print("PocketBot is in " + str(guild_count) + " servers.")


@bot.event
async def on_slash_command(command):
  embed = discord.Embed(color=discord.Color.green())
  embed.set_author(name=f"{command.author} used a command")
  embed.add_field(name="Guild Name", value=f"{command.guild}", inline=False)
  embed.add_field(name="Command Name", value=command.name, inline=False)
  embed.timestamp = datetime.utcnow()
  channel = await bot.fetch_channel(CHANNEL)
  await channel.send(embed=embed)


@slash.slash(name="bal", description='Shows the current balance')
async def bal(ctx, member: discord.User = None):
  response_API = requests.get('https://api.binance.com/api/v3/avgPrice?symbol=BCHUSDT')
  data = response_API.json()
  price = float(data['price'])
  usd = price * .0001

  if not member:
    member = ctx.author

  with open('Config/Data.json') as f:
    data = json.load(f)

  id_ = str(member.id)

  if id_ not in data:
    coin_bal = 0
  else:
    coin_bal = round(data[id_]['Coins'], 2)

  embed = discord.Embed(color=discord.Color.green(), description=f'{coin_bal} <:PocketCoin:883693571792842802> **(__Pocket Coins__)**\n{round(coin_bal * bch, 4)} <:BCH:871089657180454932>**(__BCH__)**\n{round(coin_bal * usd, 2)} **$ (USD)**')
  embed.set_author(name=f"{member} | Balance", icon_url=member.avatar_url)
  embed.set_footer(text='Enjoying PocketBot Consider Voting For It With !vote')
  await ctx.send(embed=embed)


@slash.slash(name="deposit", description='Deposit the current coins')
async def deposit(ctx, amount: int = None):
  response_API = requests.get('https://api.binance.com/api/v3/avgPrice?symbol=BCHUSDT')
  data = response_API.json()
  price = float(data['price'])
  usd = price * .0001
  if not amount:
    await ctx.send(':information_source: Usage: !deposit `<AMOUNT OF COINS>`')
    return

  description = '''
  **__Information__**
  *If you have not made a deposit yet, please send the total amount of BCH to the address below or make a ticket in !support to deposit with Paypal.*\n
  **__Note:__** ``Please use: !verify <YOUR HASH ID> to confirm the deposit and receive your balance``.
  '''
  embed = discord.Embed(color=discord.Color.green(), title='Calculator For Depositing Coins', description=description)
  embed.add_field(name='Total <:PocketCoin:883693571792842802>', value=amount, inline=False)
  embed.add_field(name='Total <:BCH:871089657180454932>', value=round(amount * bch, 4), inline=False)
  embed.add_field(name='Total $', value=round(amount * usd, 2), inline=False)
  embed.add_field(name='Address', value='qrfh5807ynvcpvm8ykatd4pmkel84e4jcv4l9z3ehm **(Copy Paste With !address)**', inline=False)
  embed.set_footer(text='This is only a calculator for user purpose to see coin worth. Any amount deposited to the address will be the amount you receive.  Not the number you put into the !deposit command.')
  await ctx.send(embed=embed)


@slash.slash(name="send", description='Send user coins')
async def send(ctx, member: discord.User = None, val: float = None):
  if not member or not val:
    await ctx.send(':information_source: Usage: !send `<@user>` `<AMOUNT OF COINS>`')
    return
  with open('Config/Data.json') as f:
    data = json.load(f)

  id_1 = str(member.id)
  id_2 = str(ctx.author.id)
  if id_2 not in data:
    await ctx.send(":warning: You don't have enough COINS.")
    return

  elif data[id_2]['Coins'] < val or val < 0:
    await ctx.send(':warning: Make sure you have enough COINS.')
    return

  def check(m):
    return m.author == ctx.author and m.channel == ctx.channel

  try:
    await ctx.send('Have you received your trade yet? `(Reply with Yes/No)`')
    confirmation = await bot.wait_for('message', check=check, timeout=30)
    if confirmation.content.lower() in ('yes', 'y', 'Yes'):
      pass
    else:
      await ctx.send('Trade Cancelled')
      return

  except asyncio.TimeoutError:
    await ctx.send('----- Request Timedout ---')
    return

  if id_1 not in data:
    data[id_1] = {}
    data[id_1]['Coins'] = val
  else:
    data[id_1]['Coins'] += val

  data[id_2]['Coins'] -= val if not data[id_2]['Coins'] - val < 0 else 0
  with open('Config/Data.json', 'w') as f:
    json.dump(data, f, indent=3)

  await ctx.send('Trade Successful')

  with open('Config/Transactions.json') as f:
    transactions = json.load(f)

  transactions['Sent'] += val

  with open('Config/Transactions.json', 'w') as f:
    json.dump(transactions, f, indent=3)


@slash.slash(name="withdraw", description='Withdraw the available coins')
async def withdraw(ctx, amount: float = None, *, address: str = None):
  response_API = requests.get('https://api.binance.com/api/v3/avgPrice?symbol=BCHUSDT')
  data = response_API.json()
  price = float(data['price'])
  usd = price * .0001
  if not amount or not address:
    await ctx.send(':information_source: Usage: !withdraw `<AMOUNT OF COINS TO WITHDRAW>` `<WALLET ADDRESS FOR BCH/PAYPAL EMAIL>` ')
    return

  amount = amount
  id_1 = str(ctx.author.id)
  with open('Config/Data.json') as f:
    data = json.load(f)

  val = round((amount - 25) * 0.0001, 6)
  pfee = round(((amount * usd) * 0.035), 4)
  pval = round((amount * usd) - pfee, 2)

  payfee = round(((amount * usd) * 0.015), 4)
  profit = round((pfee - payfee), 4)
  profitpc = round(profit / usd, 0)
  
  if not id_1 in data:
    data[id_1] = {}
    data[id_1]['Coins'] = val
  else:
    data[id_1]['Coins'] += val

  data[id_1]['Coins'] -= val if not data[id_1]['Coins'] - val < 0 else 0
  with open('Config/Data.json', 'w') as f:
    json.dump(data, f, indent=3)

  await ctx.send('Trade Successfull')

  with open('Config/Transactions.json') as f:
    transactions = json.load(f)

  transactions['Sent'] += val

  with open('Config/Transactions.json','w') as f:
    json.dump(transactions,f,indent = 3)


@slash.slash(name="withdraw", description = 'Withdraw the available coins')
async def withdraw(ctx, amount: float = None, *, address: str = None):
  response_API = requests.get('https://api.binance.com/api/v3/avgPrice?symbol=BCHUSDT')
  data = response_API.text
  price_json = json.loads(data)
  price = price_json['price']    
  price = float(price)
  usd = price * .0001
  if not amount or not address:
    await ctx.send(':information_source: Usage: !withdraw `<AMOUNT OF COINS TO WITHDRAW>` `<WALLET ADDRESS FOR BCH/PAYPAL EMAIL>` ')
    return
  try:
    amount = amount
    id_ = str(ctx.author.id)
    with open('Config/Data.json') as f:
      data = json.load(f)

    val = round((amount - 25) * 0.0001,6)
    pfee = round(((amount * usd) * 0.035),4)
    pval = round((amount * usd) - pfee,2)

    payfee = round(((amount * usd) * 0.015), 4)
    profit = round((pfee - payfee), 4) 
    profitpc = round(profit / usd,0)
    profitbch = round(profitpc * .0001,4)
    pwith = round(amount * usd,2)

      
    if not id_ in data:
      await ctx.send(':warning: You have insufficient Balance')
      return
    
    if amount > data[id_]['Coins'] or amount <= 0:
      await ctx.send(':warning: You have insufficient Balance')
      return
    

    data[id_]['Coins'] -= amount if not data[id_]['Coins'] - amount < 0 else 0
    
    msg = f'{ctx.author.mention} Your request for withdrawing {amount} Pocket Coins has been received.'
    embed = discord.Embed(color=discord.Color.green(), description=msg)
    embed.add_field(
		    name='BCH Fees',
		    value='25 <:PocketCoin:883693571792842802> **(.0025 <:BCH:871089657180454932>)**',
		    inline=False)
    embed.add_field(name='BCH Output', value=f"{val} <:BCH:871089657180454932>**(__BCH__)**",inline=False)
    embed.add_field(name='Paypal Withdrawal Amount', value=f"${pwith} **(USD)**",inline=False)
    embed.add_field(name='Paypal Fee', value=f"${pfee} **(USD)**",inline=False)
    embed.add_field(name='Paypal Output', value=f"${pval} **(USD)**",inline=False)
    embed.set_footer(
		    text='It can take up to 24 hours for the payment to transfer. Please check !info for exact PayPal rates.')
    await ctx.send(embed=embed)
    
    channel = await bot.fetch_channel(871242552496504883)
    embed = discord.Embed(color=discord.Color.dark_green(),title=f'{ctx.author} | Withdrawl Request')
    embed.add_field(name='Withdrawal Amount',value=f"{amount} <:PocketCoin:883693571792842802>",inline=False)
    embed.add_field(name='Paypal Withdrawal Amount', value=f"${pwith} **(USD)**",inline=False)
    embed.add_field(name='BCH Output',value=f"{val} <:BCH:871089657180454932>**(__BCH__)**",inline=False)
    embed.add_field(name='Paypal Output', value=f"${pval} **(USD)**",inline=False)
    embed.add_field(name='Address', value=address, inline=False)
    embed.add_field(name='Paypal Withdrawal Fees', value=f"${payfee}",inline=False)
    embed.add_field(name='Profit', value=f"${profit}",inline=False)
    embed.add_field(name='Profit <:PocketCoin:883693571792842802>',value=f"{profitpc} <:PCW:884423185116852315> +25<:PocketCoin:883693571792842802>",inline=False)
    embed.add_field(name='Profit BCH', value=f"{profitbch} <:BCH:871089657180454932> +.0025<:BCH:871089657180454932>",inline=False)
    await channel.send(embed=embed)
    with open('Config/Transactions.json') as f:
      transactions = json.load(f)
      
    transactions['Withdrawn'] += val * 10000
    
    with open('Config/Transactions.json','w') as f:
      json.dump(transactions,f,indent = 3)
      
      
  except:
    await ctx.send('Transaction FAILED Please retry.')


@slash.slash(name="remove", description = 'Removes the amount of coins from user account')
@commands.is_owner()
async def remove(ctx, member: discord.User = None, val: float = None):
	if not member or not val:
		await ctx.send(
		    ':information_source: Usage: !remove `<@user>` `<AMOUNT OF COINS>`'
		)
		return

	with open('Config/Data.json') as f:
		data = json.load(f)

	id_ = str(member.id)

	if not id_ in data:
		data[id_] = {}
		data[id_]['Coins'] = 0
	else:
		if not data[id_]['Coins'] - val < 0:
			data[id_]['Coins'] -= val
		else:
			data[id_]['Coins'] = 0

	with open('Config/Data.json', 'w') as f:
		json.dump(data, f, indent=3)

	await ctx.send(f':white_check_mark: Coins has been removed from {member}')


@slash.slash(name="add", description = 'Addss the coins to user account')
@commands.is_owner()
async def add(ctx, member: discord.User = None, val: float = None):
	if not member or not val:
		await ctx.send(
		    ':information_source: Usage: !add `<@user>` `<AMOUNT OF COINS>`')
		return

	with open('Config/Data.json') as f:
		data = json.load(f)

	id_ = str(member.id)
	if not id_ in data:
		data[id_] = {}
		data[id_]['Coins'] = val

	else:
		data[id_]['Coins'] += val

	with open('Config/Data.json', 'w') as f:
		json.dump(data, f, indent=3)

	await ctx.send(f':white_check_mark: Coins has been added to {member}')



@slash.slash(name="verify", description = 'Verify a transaction hash')
async def verify(ctx,*,id:str = None):
  if not id:
    await ctx.send(':information_source: Usage: !verify `<HASH ID>`')
    return
  else:
    with open('Config/Transactions.json') as f:
      transactions = json.load(f)
  
  if id in transactions:
    await ctx.send('This transaction ID has already been used please message @𝕃𝕚𝕓#0012 if it was not done by you.')
    return
  msg = await ctx.send('-- Verifying the Transaction --')
  hash_ = ''
  block_time = ''
  try:
    content = requests.get('https://bch-chain.api.btc.com/v3/address/qrfh5807ynvcpvm8ykatd4pmkel84e4jcv4l9z3ehm/tx?verbose=3')
    data = json.loads(content.text)
    price = str(426101).zfill(9)
    price = re.sub(price[0], f"{price[0]}.", price, 1)
    price = float(price)
    
    for x in data['data']['list']:
      block_time = x['block_time']
      if 'qrfh5807ynvcpvm8ykatd4pmkel84e4jcv4l9z3ehm' in x['outputs'][0]['addresses'][0]:
        value = x['outputs'][0]['value']
        if x['hash'] == id:
          price = str(value).zfill(9)
          price = re.sub(price[0], f"{price[0]}.", price, 1)
          price = float(price)
          hash_ = id
          break
        else:
          hash_ = ''
      else:
        hash_ = ''
    if hash_ == '':
      await ctx.send(':warning: Invalid HASH ID')
      return
    
    dt_object = datetime.fromtimestamp(block_time)
    if dt_object > datetime.now() - timedelta(hours = 48):
      with open('Config/Transactions.json') as f:
        transactions = json.load(f)
      
      transactions[hash_] = 'CONFIRMED'
      with open('Config/Transactions.json','w') as f:
        json.dump(transactions,f,indent = 3)
        
      with open('Config/Data.json','r') as f:
        data = json.load(f)
      
      id_ = str(ctx.author.id)
      amount = float(price)
      val = float(amount) / 0.0001
      transactions['Deposited'] += val
      with open('Config/Transactions.json','w') as f:
        json.dump(transactions,f,indent = 3)
      
      if not id_ in data:
        data[id_] = {}
        data[id_]['Coins'] = val
        
      else:
        data[id_]['Coins'] += val
      
      with open('Config/Data.json', 'w') as f:
        json.dump(data, f,indent= 3)
      
      embed = discord.Embed(color = discord.Color.green(),description = f'{ctx.author.mention} You have deposited {val} Pocket Coins <:PocketCoin:883693571792842802>')
      embed.add_field(name = 'Total BCH Deposited <:BCH:871089657180454932>',value = price,inline = False)
      embed.set_footer(text = 'Use command !bal to check your balance at anytime.')
      await ctx.send(embed  = embed)
      await msg.delete()
      
      channel = await bot.fetch_channel(874906183792742451)
      embed = discord.Embed(color=discord.Color.dark_green(),title=f'{ctx.author} | Deposit Total')
      embed.add_field(name='Deposit Amount',value=f"{val} <:PocketCoin:883693571792842802>",inline=False)
      await channel.send(embed=embed)
    
    else:
      await ctx.send(':warning: Transaction create date is higher than 48 hours. Please contact 𝕃𝕚𝕓#0012 to approve!')
      return
  
  except Exception as e:
    import traceback
    traceback.print_exc()
    await msg.delete()
    await ctx.send('Failed to verify. Please retry after sometime or make sure the ID is valid.')


@slash.slash(name="invite", description = 'Generate an invite link')
async def invite(ctx):
	msg = '''
https://discord.com/api/oauth2/authorize?client_id=931360549911027813&permissions=11264&scope=bot'''
	embed = discord.Embed(
	    title='<:PCW:884423185116852315> Add PocketBot To Your Server <:PCW:884423185116852315>',
	    description=msg)

	await ctx.send(embed=embed)


@slash.slash(name="vote", description = 'Vote the pocket bot')
async def vote(ctx):
	msg = '''
https://top.gg/bot/837369346949906463/vote'''
	embed = discord.Embed(
	    title=
	    '<a:UpArrow:874257776111673405> Vote PocketBot Up With The Link Below To Help Support The Bot <a:UpArrow:874257776111673405>',
	    description=msg)
	await ctx.send(embed=embed)

@slash.slash(name="support", description = 'Opens a support ticket')
async def support(ctx):
  msg = '''
  https://discord.gg/fZt2GyFTm3
  '''
  embed = discord.Embed(
  title= '<:PocketBot:874254234009362473> Need Support For PocketBot Make A Support Ticket In This Server', description=msg)
  embed.set_footer(
	    text=
	    'Enjoying PocketBot Consider Voting For It With !vote'
	)
  await ctx.send(embed=embed)


@slash.slash(name="ping", description = 'Check bot latency')
async def ping(ctx):
    await ctx.send(f':ping_pong:{round(bot.latency * 1000)}ms!')

@slash.slash(name="address", description = 'Shows address')
async def address(ctx):
    await ctx.send('qrfh5807ynvcpvm8ykatd4pmkel84e4jcv4l9z3ehm')
	
@slash.slash(name="helpdeposit", description = 'Get a help about deposit')
async def helpdeposit(ctx):
    await ctx.send('https://www.youtube.com/watch?v=dIOAfa0nHJk')

@slash.slash(name="help", description = 'Commands Help')
async def help(ctx):
    msg = '''
**!address**
(Copy Paste The Deposit Address)

**!bal**
(Check Your Coin Balance)

**!deposit** `<AMOUNT OF COINS>`
(Calculate Depositing Coin To Your Discord Wallet)

**!helpdeposit**
(Full Video Walk Through On How To Deposit)

**!info**
(More Information About PocketBot)

**!invite** 
(Add PocketBot To Your Server)

**!pbch**
(Check The Current Price Of Bitcoin Cash)

**!pc**
(Check The Current Price of Pocket Coin)

**!send** `<@user>` `<AMOUNT OF COINS>`
(Send Other Discord Users Coin)

**!support**
(Provides Link To Support Server)

**!verify** `<HASH ID>`
(Recieve Your Coin After Depositing)

**!vote** 
(Vote For PocketBot To Help Promote The Server)

**!withdraw** `<AMOUNT OF COINS TO WITHDRAW>` `<WALLET ADDRESS FOR BCH/PAYPAL EMAIL>`
(Return Coin Back To Your Home Wallet)
'''
    embed = discord.Embed(title='Bot Commands', description=msg)
    await ctx.send(embed=embed)

message1 = '''
Thank you everyone who has used PocketBot for their transactions.  All of your support is what keeps me motivated to keep making PocketBot better. Check out the other pages inside the info command with the reactions below!:arrow_lower_left:'''

message3 = '''
One Pocket Coin (<:PocketCoin:883693571792842802>) is equivalent to .0001 <:BCH:871089657180454932> (Bitcoin Cash).

Make sure you are typing everything in correct when writing commands you do not want to send or withdraw  <:PocketCoin:883693571792842802> to the wrong person. 

Please note there will be a 25 <:PCW:884423185116852315> fee at withdrawal.

If you want to deposit with Paypal instead of a BCH Wallet open a ticket in !support then go to #❓┆support and we can help you or read over #📥┆depositing (Note you will be charged more fees for a Paypal withdrawal/deposit please check the next page to see exact rates).

PocketBot's fees are used to pay for blockchain fees and security hardware.  PocketBot takes the safety of your coin as a top priority.

Any problems with the bot please make a ticket in !support to be helped.'''

message4 = '''
Deposits using PayPal will have a standard fee of 1.5%

Withdrawals using PayPal will have a standard fee of 3.5%
'''

@slash.slash(name="info", description = 'Pocketbot Stats')
async def info(ctx):
  with open('Config/Transactions.json') as f:
    transactions = json.load(f)
    deposits = transactions['Deposited']
    withdraws = transactions['Withdrawn']
    sent = transactions['Sent']
    message = f'Deposited With PocketBot: {round(deposits,2)} <:PC:883692240793395221>                                     \n\n Withdrawn With PocketBot: {round(withdraws,2)} <:PCW:884423185116852315>                                    \n\n Sent With PocketBot: {round(sent,2)} <:PocketCoin:883693571792842802>                             \n\n Total Servers: {len(bot.guilds)} <:PocketBot:874254234009362473>'
    
  message2 = ('\n'.join(guild.name for guild in bot.guilds))

  buttons = [u"\u23EA",u"\u25C0",u"\u25B6",u"\u23E9"]
  current = 0
  pc_stats = discord.Embed(title = "Total Stats <:PocketCoin:883693571792842802>", description = message, color = discord.Color.green())
  pc_stats.set_author(name = "PocketBot", icon_url = bot.user.avatar_url)
  server_list = discord.Embed(description = message2, color = discord.Color.green())
  server_list.set_author(name = "PocketBot Server List", icon_url = bot.user.avatar_url)
  support = discord.Embed(title = "Thank You For Supporting PocketBot <:PocketBot:874254234009362473>", description = message1, color = discord.Color.green())
  info = discord.Embed(title = "Important Information", description = message3, color = discord.Color.green())
  paypal = discord.Embed(title = "PayPal Deposits and Withdrawals", description = message4, color = discord.Color.blue())
  paypal.set_footer(text= "Note withdrawals made to a BCH wallet only have a fee of 25 Pocket Coin")
  bot.stats_pages = [support, info , paypal , pc_stats , server_list]

  msg = await ctx.send(embed=bot.stats_pages[current])
  for button in buttons:
    await msg.add_reaction(button)
  while True:
    try:
      reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)
    except asyncio.TimeoutError:
      embed = bot.stats_pages[current]
      embed.set_footer(text="Timed Out")
      await msg.clear_reactions()
    else:
      previous_page = current
      if reaction.emoji == u"\u23EA":
        current = 0
      elif reaction.emoji == u"\u25C0":
        if current > 0:
          current -= 1
      elif reaction.emoji == u"\u25B6":
        if current < len(bot.stats_pages)-1:
          current += 1
      elif reaction.emoji == u"\u23E9":
        current = len(bot.stats_pages)-1
      for button in buttons:
        await msg.remove_reaction(button,ctx.author)
      if current != previous_page:
        await msg.edit (embed=bot.stats_pages[current])

@slash.slash(name="pbch", description = 'Check the BSHUSDT Price')
async def pbch(ctx):
  response_API = requests.get('https://api.binance.com/api/v3/avgPrice?symbol=BCHUSDT')
  data = response_API.text
  price_json = json.loads(data)
  price = price_json['price']

  await ctx.send("<:BCH:871089657180454932> price is $" + price)

@slash.slash(name="pc", description = 'Check the Pocket Coin Price')
async def pc(ctx):
    response_API = requests.get('https://api.binance.com/api/v3/avgPrice?symbol=BCHUSDT')
    data = response_API.text
    price_json = json.loads(data)
    price = price_json['price']
    price = float(price)
    pcprice = price * .0001
    
    await ctx.send(f'<:PocketCoin:883693571792842802> price is around ${round(pcprice,3)} per coin')


@slash.slash(name="self_role", description = 'Get a Self Role')
async def self_role(ctx):
    await ctx.send("Answer These Question In Next 2 Minutes!")

    questions = ["Enter Message: ", "Enter Emojis: ", "Enter Roles: ", "Enter Channel: "]
    answers = []

    def check(user):
        return user.author == ctx.author and user.channel == ctx.channel
    
    for question in questions:
        await ctx.send(question)

        try:
            msg = await bot.wait_for('message', timeout=120.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Type Faster Next Time!")
            return
        else:
            answers.append(msg.content)

    emojis = answers[1].split(" ")
    roles = answers[2].split(" ")
    c_id = int(answers[3][2:-1])
    channel = bot.get_channel(c_id)

    bot_msg = await channel.send(answers[0])

    with open("Config/selfrole.json", "r") as f:
        self_roles = json.load(f)

    self_roles[str(bot_msg.id)] = {}
    self_roles[str(bot_msg.id)]["emojis"] = emojis
    self_roles[str(bot_msg.id)]["roles"] = roles

    with open("Config/selfrole.json", "w") as f:
        json.dump(self_roles, f)

    for emoji in emojis:
        await bot_msg.add_reaction(emoji)

@bot.event
async def on_raw_reaction_add(payload):
    msg_id = payload.message_id

    with open("Config/selfrole.json", "r") as f:
        self_roles = json.load(f)

    if payload.member.bot:
        return
    
    if str(msg_id) in self_roles:
        emojis = []
        roles = []

        for emoji in self_roles[str(msg_id)]['emojis']:
            emojis.append(emoji)

        for role in self_roles[str(msg_id)]['roles']:
            roles.append(role)
        
        guild = bot.get_guild(payload.guild_id)

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]

                role = discord.utils.get(guild.roles, name=selected_role)

                await payload.member.add_roles(role)
                await payload.member.send(f"You Gained {selected_role} Role! Check Out The New Channels.")

@bot.event
async def on_raw_reaction_remove(payload):
    msg_id = payload.message_id

    with open("Config/selfrole.json", "r") as f:
        self_roles = json.load(f)
    
    if str(msg_id) in self_roles:
        emojis = []
        roles = []

        for emoji in self_roles[str(msg_id)]['emojis']:
            emojis.append(
                emoji)

        for role in self_roles[str(msg_id)]['roles']:
            roles.append(role)
        
        guild = bot.get_guild(payload.guild_id)

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]

                role = discord.utils.get(guild.roles, name=selected_role)

                member = await(guild.fetch_member(payload.user_id))
                if member is not None:
                    await member.remove_roles(role)

bot.loop.create_task(ch_pr())
bot.run(os.environ['TOKEN'])
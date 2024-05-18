
import string
import random
import discord
import json
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='pb!')

bot.remove_command('help')

@bot.event
async def on_ready():
    print('------------- DISCORD BOT INSTANCE STARTED ---------------')

# Import statements and bot setup...

@bot.event
async def on_message(message):
    if message.author == bot.user or message.content.startswith('pb!'):
        return

    await bot.process_commands(message)

    if message.author.bot or message.webhook_id:
        return

    with open('./Ping_Bot/Rules.json') as f:
        rules = json.load(f)

    guild_id = str(message.guild.id)
    channel_id = str(message.channel.id)

    if guild_id not in rules or channel_id not in rules[guild_id]:
        return

    # Handle rules processing...
    await process_rules(message, rules[guild_id][channel_id])

async def process_rules(message, rules):
    for rule in rules.values():
        keywords = rule['Keyword']
        role_id = rule['Role']
        text = rule['Text']

        if message.embeds:
            for embed in message.embeds:
                if check_embed_for_keywords(embed, keywords):
                    await send_notification(message.channel, role_id, text)
                    break
        else:
            content = message.content
            if all(key_.replace('+', '') in content for key_ in keywords):
                await send_notification(message.channel, role_id, text)
                break

async def send_notification(channel, role_id, text):
    guild = channel.guild
    role = discord.utils.get(guild.roles, id=role_id)
    if role:
        text = text.replace('$', f'{role.mention}')
        await channel.send(text)

def check_embed_for_keywords(embed, keywords):
    for field in embed.fields:
        for value in field.values():
            if all(key_.replace('+', '') in str(value) for key_ in keywords):
                return True
    return False

@bot.command()
async def add(ctx,channel:discord.TextChannel = None,role:discord.Role = None,keyword:str = None,*,msg:str = None):
    if not channel or not role or not keyword:
        await ctx.send(':information_source: Usage: pb!add `<#CHANNEL>` `<@ROLE>` `<KEYWORD or KEYWORDS WITH / SEPARTED>` `<TEXT>`')
        return

    with open('./Ping_Bot/Rules.json') as f:
        rules = json.load(f)

    guild = str(ctx.guild.id)
    id_ = str(channel.id)

    if not guild in rules:
        rules[guild] = {}

    if not id_ in rules[guild]:    
        rules[guild][id_] = {}
    
    if not keyword.startswith('+'):
        await ctx.send('The keyword should begin with `+`')
        return
    
    if msg:
        if not msg.startswith('$'):
            await ctx.send('Text Message should begin with `$`')
            return
    
    if '/' in keyword:
        keyword = keyword.replace(' ','').split('/')
    
    else:
        keyword = [keyword]

    while True:
        hash = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)) 
        hash = str(hash)
        if not hash in rules[guild][id_]:
            break

    rules[guild][id_][hash] = {}
    rules[guild][id_][hash]['Keyword'] = keyword
    rules[guild][id_][hash]['Role'] = role.id
    rules[guild][id_][hash]['Text'] = 'NONE' if not msg else msg

    with open('./Ping_Bot/Rules.json','w') as f:
        json.dump(rules,f,indent = 3)

    await ctx.send(':white_check_mark: Rule Added')


@bot.command()
async def delete(ctx,hash:str = None):
    if not hash:
        await ctx.send(':information_source: Usage: pb!delete `<HASH>`')
        return

    with open('./Ping_Bot/Rules.json') as f:
        rules = json.load(f)
    
    guild = str(ctx.guild.id)

    if guild in rules:
        for x in rules[guild]:
            if hash in rules[guild][x]:
                rules[guild][x].pop(hash)
                with open('./Ping_Bot/Rules.json','w') as f:
                    json.dump(rules,f,indent = 3)
                
                await ctx.send(':white_check_mark: Rule Deleted')
                return
    
    await ctx.send("Hash doesn't exist!")
    
@bot.command()
async def channels(ctx):
    id_ = str(ctx.channel.id)
    
    with open('./Ping_Bot/Rules.json') as f:
        rules = json.load(f)     

    msg = '**Channels with rules in them:**\n```\n'
    channels = []
    old = msg

    guild = str(ctx.guild.id)

    for x in list(rules[guild]):
        for y in list(rules[guild][x]):
            if not rules[guild][x][y]['Keyword'] == []:
                if not x in channels:
                    channel = await bot.fetch_channel(int(x))
                    msg += f"#{channel.name}\n"
                    channels.append(x)

    if not msg == old:
        msg += f"```"
        await ctx.send(msg)
    else:
        await ctx.send('No Rules found for any channel!!')
        
@bot.command()
async def fetchrule(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: pb!fetchrule <#CHANNEL>`')
        return

    with open('./Ping_Bot/Rules.json') as f:
        rules = json.load(f)     

    msg = ''
    last_role = ''
    x = str(channel.id)

    guild = str(ctx.guild.id)

    if not guild in rules:
        await ctx.send('-- No Data Found for the Given Channel!! ---')
        return

    if not x in rules[guild]:
        await ctx.send('--- NO Data Found for the Given Channel!! ---')
        return

    await ctx.send(f'__**Rules List for channel "{channel}"**__')

    for y in rules[guild][x]:        
        if rules[guild][x][y]['Text'] == 'NONE':    
            msg = f"```css\nKeyword(s): {rules[guild][x][y]['Keyword']}\nHash: {y}\n```" 
        else:
            msg = f"```css\nKeyword(s): {rules[guild][x][y]['Keyword']}\nMessage: {rules[guild][x][y]['Text'].replace('$', '')}\nHash: {y}\n```"
        
        role = discord.utils.get(ctx.guild.roles,id = rules[guild][x][y]['Role'])
        if role.id == last_role:
            await ctx.send(msg)
            continue

        else:
            await ctx.send(f'> **@{role.name}**')
            await ctx.send(msg)
            last_role = role.id

@bot.command()
async def backup(ctx,action:str = None):
    await ctx.send(f':white_check_mark: DATA Backup Successful')
    with open("./Ping_Bot/Rules.json", "r") as f:
        rules = json.load(f)
    
    to = rules

    with open("Backup.json", "w") as f:
        json.dump(to,f,indent = 3)

@bot.command()
async def restore(ctx,action:str = None):
    if not 'Backup.json' in os.listdir():
        await ctx.send(':warning: No backup found!!')
        return
        
    await ctx.send(f':white_check_mark: Data Restored')
    with open("Backup.json", "r") as f:
        rules = json.load(f)
    
    to = rules

    with open("./Ping_Bot/Rules.json", "w") as f:
        json.dump(to,f,indent = 3)

@bot.command()
async def help(ctx):
    msg = '''
    __Adding Rules__
    pb!add #channel @Role +keyword $message text

    __Delete Rules__
    pb!delete hash

    __Displaying all channels a Rule is set up in__
    pb!channels

    __Displaying all Rules and Hashes per channel__
    pb!fetchrule #channel

    __Creating a backup of all Data and Rules__
    pb!backup

    __Restoring a backup of all Data and Rules__
    pb!restore

    __Adding a Keyword__
    pb!addkeyword hash +keyword

    __Removing a Keyword__
    pb!removekeyword hash +keyword
    '''
    CUSTOM_GREEN = discord.Color.from_rgb(57,162,68) 
    embed = discord.Embed(title = 'Command List',color = CUSTOM_GREEN,description = msg)
    await ctx.send(embed = embed)

@bot.command()
async def addkeyword(ctx,hash:str = None,keyword:str = None):
    if not hash or not keyword:
        await ctx.send(':information_source: pb!addkeyword `<HASH>` `<KEYWORD>`')
        return
    
    with open('./Ping_Bot/Rules.json') as f:
        rules = json.load(f)

    if not keyword.startswith('+'):
        await ctx.send('The keyword should begin with `+`')
        return

    guild = str(ctx.guild.id)

    if guild in rules:
        for x in rules[guild]:
            if hash in rules[guild][x]:
                rules[guild][x][hash]['Keyword'].append(keyword)
                with open('./Ping_Bot/Rules.json','w') as f:
                    json.dump(rules,f,indent = 3)
                
                await ctx.send(':white_check_mark: Keyword Added')
                return
    
    await ctx.send("Hash doesn't exist!")


@bot.command()
async def removekeyword(ctx,hash:str = None,keyword:str = None):
    if not hash or not keyword:
        await ctx.send(':information_source: pb!removekeyword `<#HASH>` `<KEYWORD>`')
        return
    
    with open('./Ping_Bot/Rules.json') as f:
        rules = json.load(f)
    
    guild = str(ctx.guild.id)

    if guild in rules:
        for x in rules[guild]:
            if hash in rules[guild][x]:
                rules[guild][x][hash]['Keyword'].remove(keyword)
                with open('./Ping_Bot/Rules.json','w') as f:
                    json.dump(rules,f,indent = 3)
                
                await ctx.send(':white_check_mark: Keyword Removed')
                return
        
    await ctx.send("Hash doesn't exist!")

bot.run(os.environ['TOKEN'])
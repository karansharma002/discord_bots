# Version: 1.0.1
import discord
import requests
from PIL import Image, ImageOps, ImageDraw, ImageFont
from discord.ext import commands

bot = commands.Bot(command_prefix=')', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('------------------- STARTED ----------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if not message.guild:
        text = message.content
        embed = discord.Embed(title='Modmail', description=text)
        embed.set_author(name=message.author)
        channel = await bot.fetch_channel(862237911792484362)
        await channel.send(embed=embed)
        await message.author.send('Your message has been forwarded to the staff team.')
        return

    if message.type == discord.MessageType.premium_guild_subscription:
        embed = discord.Embed(title='Thank you for boosting!',
                              description=f"Thanks {message.author.mention} for boosting! DM a staff to claim your perks!")
        embed.set_author(name=message.author)
        embed.set_image(url='https://media.tenor.com/images/55fa611643c2db80b12b64944e127a7d/tenor.gif')
        embed.set_footer(text='Arigato')
        channel = await bot.fetch_channel(849475597377339392)
        await channel.send(embed=embed)
        return

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    try:
        url = member.avatar_url
        with requests.get(url) as r:
            img_data = r.content		
        with open('image_name.webp', 'wb') as handler:
            handler.write(img_data)

        im = Image.open('image_name.webp').convert("RGBA")
        im = im.resize((215, 215))
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)

        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        background = Image.open('Config/Welcome.png').convert("RGBA")
        background.paste(im, (407, 163), im)
        background.save('Config/overlap.png')
        img = Image.open('Config/overlap.png')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("Config/kink.TTF", 60)
        draw.text((300,366),f"{member}",(231,84,128),font=font)
        img.save('Config/sample.png')
        channel = await bot.fetch_channel(787306859970822175)
        await channel.send(file=discord.File('Config/sample.png'))

        embed = discord.Embed(title = 'Ara ara, a new member joined the corps!',description = f'Go to the DM that I sent you to verify!')
        embed.set_image(url = 'https://media1.tenor.com/images/f16b000fce61f3cf1e9ecf5e6e9c3203/tenor.gif?itemid=15668018')
        embed.set_author(name = member)
        embed.set_footer(text = f"You're the #{member.guild.member_count} member!")
        channel = await bot.fetch_channel(867282234776092682)
        await channel.send(embed = embed)

    except Exception as e:
        print(e)

    def order_check(reaction,user):
        return str(reaction.emoji) in ['🎵','🤖','✉️','🤝','❔','✅'] and user == member

    try:
        embed = discord.Embed(title = 'Verification!', description = 'Hi, I see you just joined! Please read the rules and react to the checkmark below to continue! If you skip the rules, you can get banned~')
        embed.set_author(name = member)
        msg = await member.send(embed = embed)
    
    except:
        channel = await bot.fetch_channel(867041084835495936)
        await channel.send(f'{member.mention} Verification Failed due to DM Disabled. Please use )verify once DM are enabled.')
        return

    await msg.add_reaction('✅')
    reaction,user = await bot.wait_for('reaction_add',check = order_check,timeout = 120)
    
    desc = '''
:musical_note: - TikTok
:robot: - Server Listing Websites
:envelope: - Invited by a friend
:handshake: - Server Partnerships
:grey_question: - Others
    '''

    embed = discord.Embed(title = 'How did you join?',description = desc)
    embed.set_author(name = member)
    emojis = ['🎵','🤖','✉️','🤝','❔']
    msg = await member.send(embed = embed)
    for x in emojis:
        await msg.add_reaction(x)
    
    reaction,user = await bot.wait_for('reaction_add',check = order_check,timeout = 120)
    genr = await bot.fetch_channel(787306859970822179)
    embed = discord.Embed(title = 'Verification Complete!',description = f'Now that you have got verified, please execute the command )imnew in {genr.mention} for more info of what to do! Enjoy!')
    embed.set_author(name = member)
    await member.send(embed = embed)

    role1 = discord.utils.get(member.guild.roles,name = 'Human- Unverified')
    role2 = discord.utils.get(member.guild.roles,name = 'Mizunoto- Level 1')
    await member.remove_roles(role1)
    await member.add_roles(role2)

@bot.event
async def on_member_remove(member):
    embed = discord.Embed(title = 'Ara ara, looks like a member got eaten by a demon~',description = f'Sayonara {member.mention}')
    embed.set_image(url = 'https://media1.tenor.com/images/f16b000fce61f3cf1e9ecf5e6e9c3203/tenor.gif?itemid=15668018')
    embed.set_author(name = member)
    embed.set_footer(text = 'We will miss you~')
    channel = await bot.fetch_channel(867282234776092682)
    await channel.send(embed = embed)

@bot.command()
async def imnew(ctx):
    gr = await bot.fetch_channel(851067645817651240)
    cr = await bot.fetch_channel(851036235128635422)
    knyr = await bot.fetch_channel(851067705180422174)
    intro = await bot.fetch_channel(849573417102606349)
    desc = f'''
• Go to {gr.mention} to get general roles!
• Go to {cr.mention} to get color roles!
• Go to {knyr.mention} to get Demon Slayer roles!
• Go to {intro.mention} to introduce yourself!
    '''

    embed = discord.Embed(title = "Hi! Welcome to the server! Now to get started, here's what you should do!",description = desc)
    await ctx.send(embed = embed)

@bot.command()
async def verify(ctx,channel:discord.TextChannel = None):
    member = ctx.author

    def order_check(reaction,user):
        return str(reaction.emoji) in ['🎵','🤖','✉️','🤝','❔','✅'] and user == member

    embed = discord.Embed(title = 'Verification!', description = 'Hi, I see you just joined! Please read the rules and react to the checkmark below to continue! If you skip the rules, you can get banned~')
    embed.set_author(name = member)
    msg = await member.send(embed = embed)
    await msg.add_reaction('✅')
    reaction,user = await bot.wait_for('reaction_add',check = order_check,timeout = 120)
    
    desc = '''
:musical_note: - TikTok
:robot: - Server Listing Websites
:envelope: - Invited by a friend
:handshake: - Server Partnerships
:grey_question: - Others
    '''

    embed = discord.Embed(title = 'How did you join?',description = desc)
    embed.set_author(name = member)
    emojis = ['🎵','🤖','✉️','🤝','❔']
    msg = await member.send(embed = embed)
    for x in emojis:
        await msg.add_reaction(x)
    
    reaction,user = await bot.wait_for('reaction_add',check = order_check,timeout = 120)
    genr = await bot.fetch_channel(787306859970822179)
    embed = discord.Embed(title = 'Verification Complete!',description = f'Now that you have got verified, please execute the command )imnew in {genr.mention} for more info of what to do! Enjoy!')
    embed.set_author(name = member)
    await member.send(embed = embed)

    role1 = discord.utils.get(member.guild.roles,name = 'Human- Unverified')
    role2 = discord.utils.get(member.guild.roles,name = 'Mizunoto- Level 1')
    await member.remove_roles(role1)
    await member.add_roles(role2)

@commands.has_permissions(manage_members = True)
@bot.command()
async def reply(ctx,user:discord.User = None,*,text:str = None):
    if not user:
        await ctx.send(':information_source: Usage: )reply `@USER` `TEXT`')
    
    embed = discord.Embed(title = 'Staff',description = text)
    embed.set_author(name = user)
    await user.send(embed = embed)
    await ctx.message.add_reaction('✅')

TOKEN = 'TOKEN HERE'
bot.run(TOKEN)
    
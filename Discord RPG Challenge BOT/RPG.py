import asyncio
import discord
from discord.ext import commands
import json
from PIL import Image, ImageDraw, ImageFont


bot = commands.Bot(command_prefix='$')

data = {}
match_data = {}

@bot.event
async def on_ready():
    print('----------- == SERVER HAS STARTED == -------------')

@bot.command()
async def cancel(ctx, val: str = None):
    if not val:
        await ctx.send(':information_source: Usage: $cancel `confirm` to `(CANCEL THE QUEUE)`')
        return
    
    user = str(ctx.author.id)
    if user not in match_data:
        await ctx.send(':warning: You are not in a QUEUE')
        return
    
    match_data.pop(user, None)
    data.pop(user, None)

    await ctx.send(':white_check_mark: You have been removed from the QUEUE')

@commands.has_permissions(administrator=True)
@bot.command()
async def clearqueue(ctx, val: str = None):
    if not val:
        await ctx.send(':information_source: Usage: $clearqueue `confirm` to `(CLEARS THE QUEUE)`')
        return
    
    match_data.clear()
    data.clear()

    await ctx.send(':white_check_mark: Queue has been CLEARED')

@bot.command()
async def fight(ctx):
    user = str(ctx.author.id)
    if user in match_data or user in data:
        await ctx.send(':warning: You are already matched up. You cannot cancel at this stage.')
        return
    
    data.setdefault(user, 0)

    await ctx.send(':white_check_mark: Fight Entry Successful. Waiting to find an Opponent.')
    data[user] = 0

@bot.command()
async def challenge(ctx, user: discord.User = None):
    if not user or user == ctx.author:
        await ctx.send(':warning: Please mention a valid user to challenge.')
        return
    
    author1 = str(ctx.author.id)
    author2 = str(user.id)

    data.setdefault(author1, 0)
    data.setdefault(author2, 0)

    if author1 in match_data or author2 in match_data:
        await ctx.send(':warning: You or the player are already in the QUEUE')
        return     
    
    await ctx.send(f'{user.mention} Will you accept the Challenge? Reply with **`(Y/Yes)`** `(TIMEOUT IN 30 SECONDS)`')
    try:
        msg = await bot.wait_for('message', check=lambda m: m.author == user, timeout=30)
        if msg.content.lower() in ('yes', 'y'):
            match_data[author1] = author2
            await ctx.send(f':crossed_swords: ({ctx.author.mention}) and ({user.mention}) :crossed_swords: will be facing off.')
            return

        await ctx.send(':warning: Invalid Choice or Player Declined the challenge')
    except asyncio.TimeoutError:
        await ctx.send(':warning: The player failed to accept the challenge in the given time!')

@bot.command()
async def rank(ctx):
    user = str(ctx.author.id)
    data.setdefault(user, 0)

    def human_format(num):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '%.0f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

    def get_rank_image_path(current_rank, required):
        percent = (current_rank / required) * 100
        if percent <= 30:
            return 'Images/10.png'
        elif percent <= 50:
            return 'Images/30.png'
        elif percent <= 70:
            return 'Images/50.png'
        elif percent <= 95:
            return 'Images/70.png'
        else:
            return 'Images/100.PNG'

    def paste_image(background, overlay_path, position, resize=None):
        overlay = Image.open(overlay_path).convert("RGBA")
        if resize:
            overlay = overlay.resize(resize, Image.ANTIALIAS)
        background.paste(overlay, position, mask=overlay)

    required_ranks = [5000, 10000, 20000, 30000, 35000, 40000, 50000, 60000, 70000, 100000, 125000, 150000]
    for i, rank in enumerate(required_ranks):
        if data[user] < rank:
            required_rank = required_ranks[i-1] if i > 0 else required_ranks[0]
            break
    else:
        required_rank = required_ranks[-1]

    background = Image.open('Images/r.png').convert("RGBA")

    if required_rank < 5000:
        resize = (85, 80)
        position = (10, 4)
    elif required_rank >= 60000:
        resize = (170, 170)
        position = (-20, -34) if required_rank == 60000 else (-22, -28)
    else:
        resize = (95, 95)
        position = (5, 4)

    if data[user] < 5000:
        overlay_path = 'Images/Unranked.jpg'
    else:
        overlay_path = get_rank_image_path(data[user], required_rank)

    paste_image(background, overlay_path, position, resize=resize)

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("./l_10646.ttf", 14)
    draw.text((117, 30), f"{ctx.author}", (255, 255, 255), font=font)
    font = ImageFont.truetype("./l_10646.ttf", 10)
    draw.text((242, 2), f"{human_format(data[user])}/{human_format(required_rank)} XP", (169, 169, 169), font=font)

    background.save('Images/sample-out.png')
    await ctx.send(file=discord.File('Images/sample-out.png'))



@bot.command()
async def leaderboard(ctx):
    sorted_data = sorted(data, key=data.get, reverse=True)
    msg = '\n'.join(f"{i+1}: {await bot.fetch_user(int(x))} | **Rank: {data[x]}**" for i, x in enumerate(sorted_data[:10]))
    if not msg:
        msg = 'None'
    
    embed = discord.Embed(description=msg, color=0xce2727)
    embed.set_author(name="Top 10 Leaderboard", icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)

bot.run('YOUR_TOKEN')

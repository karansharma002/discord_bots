import discord
from discord.ext import commands
import json
from discord_slash import SlashCommand, SlashContext
from PIL import Image, ImageOps, ImageDraw, ImageFont
import random
import requests
import os


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

guild_ids = [int(os.getenv('GUILD_ID'))]

@bot.event
async def on_ready():
    print('-- XP BOT HAS STARTED --')
    await bot.wait_until_ready()

@bot.event
async def on_message(message):
    if message.author.bot or message.author == bot.user:
        return

    with open('Data.json', 'r') as f:
        data = json.load(f)

    author_id = str(message.author.id)

    if author_id not in data:
        data[author_id] = {'Level': 0, 'XP': 0}
        with open('Data.json', 'w') as f:
            json.dump(data, f, indent=3)

    # XP GAINS
    role = discord.utils.get(message.guild.roles, name='Moderator')
    if role in message.author.roles:
        return

    points = random.randint(3, 15)
    data[author_id]['XP'] += points
    xp = data[author_id]['XP']
    level = data[author_id]['Level']

    if xp >= (level + 1) * 500:
        data[author_id]['Level'] += 1
        await update_roles(message, data, level, author_id)

    with open('Data.json', 'w') as f:
        json.dump(data, f, indent=3)

async def update_roles(message, data, level, author_id):
    next_level = f'Level {level + 1}'
    current_level_role_name = f'Level {level}'
    previous_level_role_name = f'Level {level - 1}'

    try:
        role = discord.utils.get(message.guild.roles, name=next_level) or await message.guild.create_role(name=next_level)

        if role not in message.author.roles:
            await message.author.add_roles(role)

        previous_role = discord.utils.get(message.guild.roles, name=previous_level_role_name)
        if previous_role in message.author.roles:
            await message.author.remove_roles(previous_role)
    except Exception as e:
        print(f"Error updating roles: {e}")

def send_image(level, xp):
    percent = (level / (xp * 1.0)) * 100
    if percent <= 30:
        return 'Images/10.png'
    elif percent <= 50:
        return 'Images/30.png'
    elif percent <= 70:
        return 'Images/50.png'
    elif percent <= 95:
        return 'Images/70.png'
    return 'Images/100.PNG'

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.0f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

@slash.slash(name="rank", description='Check your Current Rank', guild_ids=guild_ids)
async def rank(ctx: SlashContext):
    with open('Data.json', 'r') as f:
        data = json.load(f)

    author_id = str(ctx.author.id)
    level = data[author_id]['Level']
    exp = data[author_id]['XP']
    next_level = (level + 1) * 500

    avatar_url = str(ctx.author.avatar_url)
    img_data = requests.get(avatar_url).content

    with open('image_name.webp', 'wb') as handler:
        handler.write(img_data)

    im = Image.open('image_name.webp').resize((105, 105))
    background = Image.open('Images/r.png')
    background.paste(im, (5, 4))
    image_name = send_image(exp, next_level)
    overlay = Image.open(image_name)
    background.paste(overlay, (115, 84))
    draw = ImageDraw.Draw(background)

    font_large = ImageFont.truetype("./l_10646.ttf", 18)
    font_medium = ImageFont.truetype("./l_10646.ttf", 14)
    font_small = ImageFont.truetype("./l_10646.ttf", 12)

    draw.text((117, 60), str(ctx.author), (255, 255, 255), font=font_large)
    draw.text((190, 85), f"Level {level}", (255, 255, 255), font=font_medium)
    draw.text((245, 2), f"{human_format(exp)}/{human_format(next_level)} XP", (169, 169, 169), font=font_small)

    background.save('Images/sample-out.png')
    await ctx.send(file=discord.File('Images/sample-out.png'))

@commands.has_permissions(administrator=True)
@slash.slash(name="addxp", description='Add XP to the user account', guild_ids=guild_ids)
async def addxp(ctx: SlashContext, user: discord.User, amount: int):
    with open('Data.json', 'r') as f:
        data = json.load(f)

    author_id = str(user.id)
    if author_id not in data:
        data[author_id] = {'XP': 0, 'Level': 0}

    data[author_id]['XP'] += amount
    with open('Data.json', 'w') as f:
        json.dump(data, f, indent=3)

    await ctx.send(f':white_check_mark: Added {amount} XP to {user} account', hidden=True)

@commands.has_permissions(administrator=True)
@slash.slash(name="removexp", description='Remove XP from the user account', guild_ids=guild_ids)
async def removexp(ctx: SlashContext, user: discord.User, amount: int):
    with open('Data.json', 'r') as f:
        data = json.load(f)

    author_id = str(user.id)
    data[author_id]['XP'] -= amount
    with open('Data.json', 'w') as f:
        json.dump(data, f, indent=3)

    await ctx.send(f':white_check_mark: Removed {amount} XP from {user} account', hidden=True)

@commands.has_permissions(administrator=True)
@slash.slash(name="puntaje", description='Shows the TOP XP Users', guild_ids=guild_ids)
async def top(ctx: SlashContext):
    with open('Data.json', 'r') as f:
        users = json.load(f)

    high_score_list = sorted(users, key=lambda x: users[x].get('XP', 0), reverse=True)
    msg = ''

    for number, user in enumerate(high_score_list[:15]):
        author = await bot.fetch_user(int(user))
        xp = users[user]['XP']
        msg += f"**‣ {number + 1}**. {author} ⁃ XP: **{xp}**\n"

    embed = discord.Embed(
        title=":money_with_wings: Puntaje",
        color=0x05ffda,
        description=msg
    )
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))

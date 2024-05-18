import discord
import random
import praw
import json
from discord.ext import commands, tasks
import asyncio
import os

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

GUILD_ID = 937414943786024960
invites = {}
last_member_id = ""

# Load Reddit credentials from environment variables
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = "Karma breakdown 1.0 by /u/_Daimon_ github.com/Damgaard/Reddit-Bots/"
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent=REDDIT_USER_AGENT)  # Initialize Reddit API

async def fetch_invites():
    global last_member_id, invites
    await bot.wait_until_ready()
    
    while True:
        guild = await bot.fetch_guild(GUILD_ID)
        current_invites = await guild.invites()
        new_invites = [(invite.code, invite.uses) for invite in current_invites]

        for current_invite in current_invites:
            for saved_invite in invites:
                if saved_invite[0] == current_invite.code and current_invite.uses > saved_invite[1]:
                    with open('Config.json') as f:
                        config = json.load(f)

                    if 'Invite_Channel' in config:
                        logs_channel = await bot.fetch_channel(int(config['Invite_Channel']))
                        inviter = await bot.fetch_user(int(last_member_id))
                        message = f"{inviter.name} **joined**; Invited by **{current_invite.inviter.name}** (**{str(current_invite.uses)}** invites)"
                        await logs_channel.send(message)
        
        invites = new_invites
        await asyncio.sleep(2)

@bot.command()
async def setinviteschannel(ctx, channel: discord.TextChannel = None):
    if not channel:
        await ctx.send('Usage: .setinviteschannel <#CHANNEL WHERE MEMES ARE SENT>')
        return
    
    update_config('Invite_Channel', channel.id)
    await ctx.send(':white_check_mark: Channel Added')

@bot.command()
async def setmemechannel(ctx, channel: discord.TextChannel = None):
    if not channel:
        await ctx.send('Usage: .setmemechannel <#CHANNEL WHERE MEMES ARE SENT>')
        return
    
    update_config('Meme_Channel', channel.id)
    await ctx.send(':white_check_mark: Channel Added')

def update_config(key, value):
    with open('Config.json', 'r') as f:
        config = json.load(f)
    
    config[key] = value

    with open('Config.json', 'w') as f:
        json.dump(config, f, indent=3)

@bot.event
async def on_member_join(member):
    global last_member_id
    last_member_id = str(member.id)

@tasks.loop(minutes=30)
async def post_meme():
    with open('Config.json') as f:
        config = json.load(f)
    
    if 'Meme_Channel' not in config:
        return

    channel = await bot.fetch_channel(int(config['Meme_Channel']))
    memes_submissions = reddit.subreddit('memes').hot()

    for _ in range(random.randint(1, 10)):
        submission = next(submission for submission in memes_submissions if not submission.stickied)

    embed = discord.Embed(color=0xff8000)
    embed.set_author(name=submission.title, url=submission.url)
    embed.set_image(url=submission.url)
    await channel.send(embed=embed)

@bot.command()
async def invites(ctx):
    total_invites = sum(invite.uses for invite in await ctx.guild.invites() if invite.inviter == ctx.author)
    
    embed = discord.Embed(
        color=discord.Color.dark_blue(), 
        title=f"{ctx.author} | Total Invites", 
        description=f'You currently have **{total_invites}** invites.'
    )
    await ctx.send(embed=embed)

bot.loop.create_task(fetch_invites())
post_meme.start()

bot.run('ODE4MDk1MzY3Njc2NjI0OTA5.YETErw.RokmAgVoNk-DR1FGsnKAAJzdvrg')

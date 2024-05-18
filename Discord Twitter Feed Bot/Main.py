import tweepy
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import json

# Twitter API configuration
TWITTER_CONSUMER_KEY = 'YOUR_TWITTER_CONSUMER_KEY'
TWITTER_CONSUMER_SECRET = 'YOUR_TWITTER_CONSUMER_SECRET'
TWITTER_ACCESS_TOKEN = 'YOUR_TWITTER_ACCESS_TOKEN'
TWITTER_ACCESS_SECRET = 'YOUR_TWITTER_ACCESS_SECRET'

# Discord Bot configuration
DISCORD_BOT_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

# Initialize Twitter API
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)

# Initialize Discord Bot
bot = commands.Bot(command_prefix='$')
OLD_TWEETS = []

# Function to handle fetching and sending tweets
async def handle_tweets():
    global OLD_TWEETS

    # Load stored tweet data
    with open('ST.json') as f:
        tweet_data = json.load(f)

    # Get user timeline tweets
    tweets = api.user_timeline(screen_name='fxvitali')
    for tweet in tweets:
        tweet_text = tweet.text
        if tweet_text in OLD_TWEETS:
            continue
        else:
            OLD_TWEETS.append(tweet_text)
            if 'Channel' not in tweet_data:
                return

            channel = await bot.fetch_channel(tweet_data['Channel'])
            embed = discord.Embed(description=tweet_text, color=discord.Colour.blue())
            if 'media' in tweet.entities:
                for x in tweet.entities['media']:
                    embed.set_image(url=x['media_url_https'])

            await channel.send(embed=embed)

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print('Bot started')
    await fetch_tw.start()

# Task to periodically fetch tweets
@tasks.loop(seconds=60)
async def fetch_tw():
    await handle_tweets()

# Command to set the tweet channel
@has_permissions(administrator=True)
@bot.command()
async def setchannel(ctx, channel: discord.TextChannel = None):
    if not channel:
        return

    # Update tweet channel in config
    with open('ST.json') as f:
        tweet_data = json.load(f)

    tweet_data['Channel'] = channel.id
    with open('ST.json', 'w') as f:
        json.dump(tweet_data, f, indent=3)

    await ctx.send(':white_check_mark: Channel has been marked as Active!')

# Command to clear messages
@has_permissions(administrator=True)
@bot.command()
async def clear(ctx, amount: int = None):
    if amount is None:
        amount = 1
    await ctx.channel.purge(limit=amount)

bot.run(DISCORD_BOT_TOKEN)

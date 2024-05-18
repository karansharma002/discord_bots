import discord
from discord.ext import commands
from discord_slash import SlashCommand
import json
import tweepy
from discord_slash.context import ComponentContext
import os

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

# Constants
CONFIG_FILE = 'Config.json'
ITEMS_FILE = 'Items.json'
DATA_FILE = 'Data.json'
GUILD_IDS = [947183460123025428]
CURRENCY = 'Gold'

# Error Handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required arguments. Command usage: !raid <channel> <points> <tweet url>")
    else:
        await ctx.send(f"An error occurred: {error}")

# Helper Functions
def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=3)

# Command: Raid
@bot.command()
async def raid(ctx, channel: discord.TextChannel = None, points: int = None, url = None):
    if not channel or not points or not url:
        await ctx.send(':information_source: Command Usage: !raid <channel> <points> <tweet url>')
        return
    
    # Send Embed
    embed = discord.Embed(title='Twitter Activity Rewards', color=discord.Color.blue())
    embed.add_field(name=':paperclips: Tweet Link :paperclips:', value=url)
    embed.add_field(name=':coin: Reward :coin:', value=url)
    await ctx.send(embed=embed)

    # Update Config
    config = load_json(CONFIG_FILE)
    config['Tweet'] = {'Url': url, 'Points': points, 'Channel': channel.id}
    save_json(config, CONFIG_FILE)
@bot.event
async def on_component(ctx: ComponentContext):
    try:
        label = ctx.component['label']
        with open('Config.json') as f:
            config = json.load(f)
        
        #! VERIFY FOLLOWING

        if label == 'Claim Like Points':
            username = ''

            #! TWITTER VERIFICATIONS HERE
            api = tweepy.API(auth, wait_on_rate_limit=True)

            #! STEP 2

            cases = [] #! TWITTER CHECKS, AND PASSES

            user = api.get_user(screen_name = username)
            user = user.id

            with open('Tweets.json') as f:
                tw = json.load(f)


            #! CHECK IF USER HAS LIKED IT?

            tweets = api.user_timeline(screen_name = 'animeragame')
            try:
                for tweet in tweets:
                    for x in api.get_favorites(screen_name = username):
                        if x.id == tweet.id:
                            cases.append('Passed')
                            break

            except:
                pass

        elif label == 'Claim Retweet Points':
            #! CHECK IF USER HAS RETWEETED IT?

            try:
                for tweet in tweets:
                    for x in api.user_timeline(screen_name = username):
                        if 'animeragame' in x.text and 'RT' in x.text:
                            cases.append('Passed')
                            break
            except:
                pass


        elif label == 'Claim Comment Points':
            try:
                for tweet in tweets:
                    for x in api.user_timeline(screen_name = username):
                        if hasattr(x, 'in_reply_to_status_id_str'):
                            if x.in_reply_to_status_id == tweet.id:
                                cases.append('Passed')
                                break

            except:
                pass

    except:
        import traceback
        traceback.print_exc()

# Command: Set Channel
@commands.has_permissions(administrator=True)
@slash.slash(name="setchannel", description='Set the Consumable Items Notifications Channel', guild_ids=GUILD_IDS)
async def set_channel(ctx, channel: discord.TextChannel = None):
    config = load_json(CONFIG_FILE)
    config['Channel'] = channel.id
    save_json(config, CONFIG_FILE)
    await ctx.send(":white_check_mark: Channel Added", hidden=True)


bot.run(os.getenv('TOKEN'))
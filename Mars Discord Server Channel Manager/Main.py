import discord
from discord.ext import commands, tasks
import datetime
from discord.ui import create_actionrow
from discord_components import ComponentContext
from discord_components import create_button
from discord_slash import SlashCommand
import os

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

# Configuration (Replace with your actual IDs)
guild_id = 1234567890  
dt_channel_id = 0
tm_channel_id = 0
online_channel_id = 0
members_channel_id = 0
verification_channel_id = 0  # Channel for rule reading
unverified_role_name = 'Unverified'
member_role_name = 'Member'

@bot.event
async def on_ready():
    print('Bot started!')
    update_channels.start()

@tasks.loop(minutes=1)
async def update_channels():
    try:
        guild = bot.get_guild(guild_id)
        
        # Update date/time channels
        dt_channel = guild.get_channel(dt_channel_id)
        tm_channel = guild.get_channel(tm_channel_id)
        await dt_channel.edit(name=f'📅 · {datetime.datetime.utcnow().strftime("%A %B %d")} (UTC)')
        await tm_channel.edit(name=f'🕒 · {datetime.datetime.utcnow().strftime("%I:%M %p")} UTC')

        # Update online/member count channels
        online_count = sum(1 for m in guild.members if m.status != discord.Status.offline and not m.bot)
        await guild.get_channel(online_channel_id).edit(name=f'🟢 · Total Online: {online_count}')
        await guild.get_channel(members_channel_id).edit(name=f'👤 · Total Members: {guild.member_count}')
    except discord.HTTPException as e:
        print(f"Error updating channels: {e}")

@bot.event
async def on_component(ctx: ComponentContext):
    if ctx.custom_id == "verify_button":
        member = ctx.author
        role = discord.utils.get(member.guild.roles, name=member_role_name)
        unverified_role = discord.utils.get(member.guild.roles, name=unverified_role_name)

        if unverified_role in member.roles:
            await member.add_roles(role)
            await member.remove_roles(unverified_role)
            await ctx.reply(':tada: You have been verified!', hidden=True)  

@slash.slash(name="setupverify", description="Set up the verification message")
async def setupverify(ctx):
    embed = discord.Embed(
        color=discord.Color.magenta(),
        description=f'__**Welcome to {ctx.guild.name} Community!**__\n\nPlease read the <#{verification_channel_id}> before proceeding.\n'
    )
    embed.set_author(name='Server Verification', icon_url=bot.user.avatar_url)
    embed.set_image(url='https://nabpilot.org/wp-content/uploads/2017/05/Verify.jpg')

    await ctx.send(embed=embed, components=[
        create_actionrow(create_button(style=5, label="VERIFY", custom_id="verify_button"))
    ])

bot.run(os.getenv('TOKEN'))

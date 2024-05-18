import datetime
import json
import asyncio
import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand
import traceback

intents = discord.Intents().messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = "NTcwMzY3MzkwNDA0MDUwOTQ2.GZ3d2x.-FPELXLYg0BzB2DEb7YjE2TcPsUu_o10LzmRII"  # Live build
slash = SlashCommand(bot, sync_commands=True)

startup_extensions = ["Cog.help", "Cog.main_commands"]

@bot.event
async def on_ready():
    print(f"Connecting...\nConnected {bot.user}")
    stauts_task.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    with open("count.json") as f:
        counts = json.load(f)

    for count in counts:
        if count["channel"] == message.channel.id:
            try:
                int(message.content)
            except:
                await message.delete()

            if count["count"] < count["number"]:
                try:
                    if count["member"] != message.author.id:
                        int_message = int(message.content)
                        if int_message == count["count"] + 1:
                            count["count"] += 1
                            count["member"] = message.author.id
                            if int_message == count["number"]:
                                embed = discord.Embed(description=f"This channel has reached its limit ({count['number']})!",
                                                        color=discord.Color.green())
                                embed.set_author(name=f"Game over!")
                                await message.channel.send(embed=embed)
                                counts.remove(count)

                            with open("count.json", "w") as f:
                                json.dump(counts, f, indent=2)
                            return

                        else:
                            await message.delete()
                    else:
                        await message.delete()

                except ValueError:
                    await message.delete()

    with open("guess.json") as f:
        guesses = json.load(f)
        
    for guess in guesses:
        if guess["channel"] == message.channel.id:
            channel = message.channel
            guess_number = guess["guess_number"]
            max_number = guess["max_number"]
            min_number = guess["min_number"]

            try:
                int(message.content)
            except:
                embed = discord.Embed(description=f"{message.author.mention}, `{message.content}` is not a number.",
                                        color=discord.Color.red())
                embed.set_author(name=f"That is not a number!")
                await channel.send(embed=embed)
                return

            guessed_number = int(message.content)

            if guessed_number == guess_number:
                embed = discord.Embed(description=f"{message.author.mention} has guessed the correct number",
                                        color=discord.Color.green())
                embed.set_author(name=f"Congratulations!")
                await channel.send(embed=embed)
                guesses.remove(guess)
                with open("guess.json", "w") as f:
                    json.dump(guesses, f, indent=2)
                return

            elif guessed_number > max_number or guessed_number < min_number:
                embed = discord.Embed(
                    description=f"{message.author.mention}, the max number is `{max_number}` and the min number is `{min_number}`. "
                                f"Please stick to these numbers!",
                    color=discord.Color.red())
                embed.set_author(name=f"Stick in the boundaries!")
                await channel.send(embed=embed)
                return

@tasks.loop()
async def stauts_task():
    await status_loop()

async def status_loop():
    while True:
        guild_count = len(bot.guilds)
        activity = discord.Activity(name=f'{bot.command_prefix}help | {guild_count} servers!',
                                    type=discord.ActivityType.playing)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(10)

@bot.event
async def on_command_error(ctx, error):
    # if command has local error handler, return
    if hasattr(ctx.command, 'on_error'):
        return

    # get the original exception
    error = getattr(error, 'original', error)

    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.BotMissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        _message = 'I need the **{}** permission(s) to run this command.'.format(', '.join(missing))
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=_message,
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return
    
    if isinstance(error, commands.DisabledCommand):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description="This command has been disabled",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.CommandOnCooldown):
        remaining = "{}".format(str(datetime.timedelta(seconds=error.retry_after)))
        embed = discord.Embed(title=f"Click here to vote",
                              description=f"This command is on cooldown, please try again in "
                                          f"{remaining[0:1]} hours, "
                                          f"{remaining[3:4]} minutes, "
                                          f"{remaining[6:7]} seconds!\n"
                                          f"To avoid getting these cooldowns please vote by clicking above! This will "
                                          f"kick in within 1 minute and 30 seconds!",
                              url="https://top.gg/bot/700793365754806402/vote",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, discord.HTTPException):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"Sadly I could not send a message. This can be because it was too long or "
                                          f"it didnt form a url correctly. Check below to see the real error!",
                              color=discord.Color.red())
        embed.set_footer(text=error)
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"{_message}",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.CommandError):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"Invalid user input. "
                                          f"Please use `{bot.command_prefix}help {ctx.command.name}`. Check what arguments are "
                                          f"needed underneath it and retry this command!",
                              color=discord.Color.red())
        embed.set_footer(text=f"Debug error message: {error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.UserInputError):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"Invalid user input. "
                                          f"Please use `{bot.command_prefix}help {ctx.command.cog_name}` "
                                          f"and locate the `{ctx.command}` command. Check what arguments are "
                                          f"needed underneath it and retry this command!",
                              color=discord.Color.red())
        embed.set_footer(text=f"Debug error message: {error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.NoPrivateMessage):
        try:
            embed = discord.Embed(title=f"{ctx.command} error",
                                  description="This command cannot be sued in direct messages",
                                  color=discord.Color.red())
            embed.set_footer(text=f"{error}")
            await ctx.author.send(embed=embed)
        except discord.Forbidden:
            pass
        return
    
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(title=f"{ctx.command} error",
                              description=f"You do not have permission to use this command",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)

    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


if __name__ == "__main__":
    bot.remove_command("help")
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}'.format(extension, e))

bot.run(TOKEN)
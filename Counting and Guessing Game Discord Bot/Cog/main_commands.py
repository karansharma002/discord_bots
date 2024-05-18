from itertools import count
import json
import datetime
import random

import discord
from discord.ext import commands
from discord_slash import cog_ext

# Yeah this isn't my code either. Here's a link to the original source https://gist.github.com/StudioMFTechnologies/ad41bfd32b2379ccffe90b0e34128b8b


class MainCommands(commands.Cog, name="Main Commands"):
    """All the main commands!"""

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="guess",description="Guess the Number Game")
    async def guess(self, ctx, min_number: int, max_number: int, guess_number, *, channel: discord.TextChannel):
        if not ctx.author.guild_permissions.administrator: 
            embed = discord.Embed(title=f"{ctx.command} error",
                                description=f"You do not have permission to use this command",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        """Create a guessing game for a specific text channel"""
        try:
            guess_number = int(guess_number)
        except ValueError:
            if guess_number.lower() == "random":
                guess_number = random.randint(min_number, max_number)
            else:
                embed = discord.Embed(description=f"It seems you didnt enter a number for the guess number!",
                                      color=discord.Color.red())
                embed.set_author(name=f"Whoops!")
                await ctx.send(embed=embed)
                return

        if guess_number > max_number or guess_number < min_number:
            embed = discord.Embed(description=f"It seems you misstyped and made the guess number bigger than the max number. That wouldn't be fair would it? Please try again",
                                  color=discord.Color.red())
            embed.set_author(name=f"Whoops!")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(description=f"Go to <#{channel.id}> and start guessing there!",
                              color=discord.Color.green())
        embed.set_author(name=f"Game has started!")
        await ctx.send(embed=embed, hidden = True)

        #delete_array = [ctx.message]
        #await ctx.channel.delete_messages(delete_array)
        embed = discord.Embed(description=f"Try to guess the correct number between `{min_number}` and `{max_number}`",
                              color=discord.Color.green())
        embed.set_author(name=f"Game has started")
        await channel.send(embed=embed)

        # channel = await ctx.guild.create_text_channel(name=channel_name, category=ctx.channel.category)

        with open("guess.json") as f:
            guesses = json.load(f)

        new_guess = {
            "channel": channel.id,
            "min_number": min_number,
            "max_number": max_number,
            "guess_number": guess_number
        }

        guesses.append(new_guess)
        with open("guess.json", "w") as f:
            json.dump(guesses, f, indent=2)

    @cog_ext.cog_slash(name="count",description="Count To a specific number")
    async def count(self, ctx, count_to, *, channel: discord.TextChannel):
        if not ctx.author.guild_permissions.administrator: 
            embed = discord.Embed(title=f"{ctx.command} error",
                                description=f"You do not have permission to use this command",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            return


        try:
            int(count_to)
        except:

            embed = discord.Embed(title=f"{ctx.command} error",
                                description=f"Count To Value should be an integer.",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        """Count to a number"""
        if str(count_to).lower() == "infinite":
            count_to = 99999999999999999999999999999999999999999999999999999999999999999999999999999999999
            embed = discord.Embed(description=f"Try to count to `infinity` 1 by 1.",
                                  color=discord.Color.green())
            embed.set_author(name=f"Game has started")
            await channel.send(embed=embed)


        else:
            count_to = int(count_to)
            embed = discord.Embed(description=f"Try to count to `{count_to}` 1 by 1.",
                                  color=discord.Color.green())
            embed.set_author(name=f"Game has started")
            await channel.send(embed=embed)

        



        embed = discord.Embed(description=f"Go to <#{channel.id}> and start counting there!",
                              color=discord.Color.green())
        embed.set_author(name=f"Game has started!")
        await ctx.send(embed=embed)
        with open("count.json") as f:
            counts = json.load(f)
        
        
        new_count = {
            "channel": channel.id,
            "number": count_to,
            "count": 0,
            "member": None
        }

        counts.append(new_count)
        with open("count.json", "w") as f:
            json.dump(counts, f, indent=2)

    @cog_ext.cog_slash(name="cancel",description="Cancel a game in a specific channel")
    async def cancel(self, ctx, channel: discord.TextChannel):
        if not ctx.author.guild_permissions.administrator: 
            embed = discord.Embed(title=f"{ctx.command} error",
                                description=f"You do not have permission to use this command",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            return


        try:
            channel.name
            embed = discord.Embed(description = f"Looking for active games in the {channel.name}", color = discord.Color.green())
            msg = await ctx.send(embed = embed)
        
        except:
            embed = discord.Embed(title=f"{ctx.command} error",
                                description=f"The bot doesn't have permission to view the mentioned channel.",
                                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        """Cancel a game in a specific channel"""
        with open("count.json") as f:
            counts = json.load(f)
        
        for count in counts:
            if count["channel"] == channel.id:
                counts.remove(count)
                with open("count.json", "w") as f:
                    json.dump(counts, f, indent=2)

                embed = discord.Embed(description=f"The counting game in channel {channel.mention} has been stopped!",
                                      color=discord.Color.green())
                embed.set_author(name=f"The game is over")
                await msg.edit(embed=embed)
                return

        with open("guess.json") as f:
            guesses = json.load(f)

        for guess in reversed(guesses):
            if guess["channel"] == channel.id:
                guesses.remove(guess)
                with open("guess.json", "w") as f:
                    json.dump(guesses, f, indent=2)

                embed = discord.Embed(description=f"The guessing game in channel {channel.mention} has been stopped!",
                                      color=discord.Color.green())
                embed.set_author(name=f"The game is over")
                await msg.edit(embed=embed)
                return


        embed = discord.Embed(description=f"There was no game found in {channel.mention}",
                              color=discord.Color.red())
        embed.set_author(name=f"No game found")
        await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(MainCommands(bot))



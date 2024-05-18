import json
from types import MappingProxyType

import discord
from discord.ext import commands
from discord_slash import cog_ext
import discord_slash

# Yeah this isn't my code either. Here's a link to the original source https://gist.github.com/StudioMFTechnologies/ad41bfd32b2379ccffe90b0e34128b8b

TOKEN = "NTcwMzY3MzkwNDA0MDUwOTQ2.GZ3d2x.-FPELXLYg0BzB2DEb7YjE2TcPsUu_o10LzmRII"

class Help(commands.Cog, name="Help"):
    """The help command!"""

    def __init__(self, bot):
        self.bot = bot
        self.discord_slash = discord_slash

    @cog_ext.cog_slash(name="help",description="Commands Help")
    async def help(self, ctx, *, command=None):
        
        """Gets all category and commands of mine."""
        prefix = self.bot.command_prefix
        try:
            if command is None:
                a = {"guess": "MainCommands", "cancel": "MainCommands", "count": "MainCommands", "help": "Commands Help"}
                """Command listing.  What more?"""
                halp = discord.Embed(color=discord.Color.green())
                halp.set_author(name="All commands", icon_url=self.bot.user.avatar_url)
                all_commands = []
                import discord_slash
                for x in await discord_slash.utils.manage_commands.get_all_commands(self.bot.user.id, TOKEN):
                    halp.add_field(name=f"`{x['name']}`", value=a[x['name'].lower()], inline=False)
                halp.set_footer(text=f"To find out more about a command please do: {prefix}help <command name>")
                await ctx.send(embed=halp)

            else:
                """Command listing within a category."""
                found = False
                import discord_slash
                for x in await discord_slash.utils.manage_commands.get_all_commands(self.bot.user.id, TOKEN):
                    if x['name'].lower() == command.lower():
                        params = []
                        if 'options' in x:
                            for y in x['options']:
                                params += f"({y['name']}) - "

                        halp = discord.Embed(color=discord.Color.green())
                        halp.set_author(name=f"/{x['name']} info", icon_url=self.bot.user.avatar_url)
                        halp.add_field(name="Description:", value=x['description'], inline=False)
                        halp.add_field(name="Usage:", value=f"`/{x['name']} {' '.join(params)}`", inline=False)
                        await ctx.send(embed=halp)
                        return

                if not found:
                    """Reminds you if that category doesn't exist."""
                    halp = discord.Embed(title='Error!', description='How do you even use "' + command + '"?',
                                         color=discord.Color.red())
                    await ctx.send(embed=halp)
                else:
                    # await ctx.message.add_reaction(emoji='✔️')
                    pass
        except ValueError:
            await ctx.send("Excuse me, I can't send embeds.")


def setup(bot):
    bot.add_cog(Help(bot))

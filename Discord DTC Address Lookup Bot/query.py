import discord
from discord.ext import commands
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Google Sheets configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1f5StbK-fTtRsfOzwtmlH_k22NoPQQYqwi8HWMSdOwl0'
RANGE_NAME = 'Zero48 DTC Address!A1:B'
SERVICE_ACCOUNT_FILE = 'keys.json'

@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.command()
async def query(ctx, address: str = None):
    if not address:
        await ctx.send(":information_source: Command Usage: `!query <address>`")
        return

    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get('values', [])

        for row in reversed(values[1:]):
            if row[0] == address:
                embed = discord.Embed(color=discord.Color.dark_blue())
                embed.set_author(name=f'{ctx.author} | QUERY', icon_url=ctx.author.avatar_url)
                embed.add_field(name='Address', value=address, inline=False)
                embed.add_field(name='DTC Type', value=row[1], inline=False)
                await ctx.send(embed=embed)
                return

        await ctx.send(":warning: Your address is not currently DTC.")

    except Exception as e:
        print(f"An error occurred: {e}")  # Log any errors
        await ctx.send(":x: An error occurred while processing your request.")

bot.run(os.getenv('TOKEN'))  # Load token from environment variable

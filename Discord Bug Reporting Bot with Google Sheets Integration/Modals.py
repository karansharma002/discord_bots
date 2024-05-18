from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
import discord
from discord.ext import commands
import imgbbpy
import os

range_value = 2

class BugReportView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    @discord.ui.button(label="SUBMIT BUG REPORT", style=discord.ButtonStyle.green, custom_id="role_button")
    async def submit_bug_report(self, interaction: discord.Interaction, button: discord.ui.Button):
        global range_value
        guild = interaction.guild
        member = interaction.user

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        category = discord.utils.get(guild.categories, id=1061829492223529061)
        
        channel = await guild.create_text_channel(f'bug-report-{interaction.user}', overwrites=overwrites, category=category)
        embed = discord.Embed(description=channel.mention, color=0xe70d0d)
        await interaction.response.send_message(embed=embed, ephemeral=True)

        def check(m):
            return m.author == interaction.user

        def check2(m):
            return m.author == interaction.user and m.attachments

        await channel.send(f'{interaction.user.mention}')
        while True:
            msg1 = await channel.send('1) What is the severity level of the bug? (High/Medium/Low)')
            msg1 = await client.wait_for('message', check=check, timeout=300)
            reply1 = msg1.content.lower()
            if reply1 not in ('high', 'medium', 'low'):
                await channel.send('> :warning: Replies should be from `[High / Medium / Low]`')
            else:
                break

        try:
            await channel.send('2) Description of the bug')
            msg2 = await client.wait_for('message', check=check, timeout=300)
            reply2 = msg2.content

            await channel.send('3) Upload a screenshot/picture of bug.')
            msg3 = await client.wait_for('message', check=check2, timeout=300)
            for attachment in msg3.attachments:
                await attachment.save(f'{interaction.user}.png')
        
        except asyncio.TimeoutError:
            await channel.send(':warning: REQUEST Timedout')
            await asyncio.sleep(5)
            await channel.delete()

        embed = discord.Embed(description='Thank you; the report has been submitted (this channel will be auto-deleted in 10 seconds) \n\n`[AUTO DELETING CHANNEL IN 10 SECONDS]`', color=0xe70d0d)
        await channel.send(embed=embed)

        client_1 = imgbbpy.SyncClient('1a42cc295f3915eb3526291672acd280')
        image = client_1.upload(file=f'{interaction.user}.png')
        link = image.url

        embed = discord.Embed(title='BUG REPORT', description=f'New bug report submitted by {interaction.user}', color=0xe70d0d)
        embed.add_field(name="Severity (High/Medium/Low)", value=reply1, inline=False)
        embed.add_field(name="Bug Description", value=reply2, inline=False)
        embed.add_field(name="Bug Found By", value=str(interaction.user), inline=False)
        embed.set_image(url=link)
        channel2 = await client.fetch_channel(1061220580671619142)
        await channel2.send(embed=embed)

        val = [[str(datetime.utcnow()), str(interaction.user.id), reply1, reply2, link]]

        url = '1re9M1S72PzB99Nzm-1CMHG8Hn0invFOZ0gT5hQzSl5Y'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'keys.json'
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        SAMPLE_SPREADSHEET_ID = url
        SAMPLE_RANGE_NAME = f'Sheet1!A{range_value}'
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()

        value_range_body = {
            'majorDimension': 'ROWS',
            'values': val}
        
        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"Sheet1!A{range_value}", valueInputOption="USER_ENTERED", body={"values": val}).execute()
        await channel.delete()
        range_value += 1
        os.remove(f'{interaction.user}.png')

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False 
        self.added = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: 
            await tree.sync(guild=discord.Object(id=974514942877261886)) 
            self.synced = True
        if not self.added:
            self.add_view(BugReportView())
            self.added = True
        print(f"We have logged in as {self.user}.")

client = MyClient()
tree = commands.CommandTree(client)

@tree.command(guild=discord.Object(id=974514942877261886), name='verify', description='Launches a button!')
async def verify(interaction: discord.Interaction): 
    if not interaction.user.id == 710462115831611444:
        return

    embed = discord.Embed(title='Bug Report', description='Please use the button below to to report a BUG', color=0xe70d0d)
    await interaction.response.send_message(embed=embed, view=BugReportView())

client.run(os.getenv('TOKEN'))

import discord
from discord.ext import commands, tasks
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json

bot = commands.Bot(command_prefix='mr.')

roles = {
    'graph': 906512127026659400,
    'concept': 906512159264079882,
    'supp': 906523858826326037,
    'comm': 906512164876091462
}

questions = {
    'graph': {
        'title': 'QUESTIONS DE GRAPHISME :',
        'description': '''6 ┊ Exposez-moi un projet professionnel dont vous êtes particulièrement fier et inversement
7 ┊ Quelle est votre pire faiblesse ?
8  ┊ Quels sont vos points forts ?
9  ┊ Combien de temps vous voyez-vous travailler pour nous ?
10 ┊ Décrivez votre/vos styles / thèmes que vous aimez.
11 ┊ Aimez-vous travailler en équipe ?
12 ┊ Savez-vous travailler sous la pression ?
13 ┊ Comment comptez-vous compenser votre manque d’expérience ?
14 ┊ Pourquoi pensez-vous réussir dans ce poste ?'''
    },
    'concept': {
        'title': 'QUESTIONS DE CONCEPTION :',
        'description': '''6 ┊ Exposez-moi un projet professionnel dont vous êtes particulièrement fier et inversement
7 ┊ Quelle est votre pire faiblesse ?
8  ┊ Quels sont vos points forts ?
9  ┊ Combien de temps vous voyez-vous travailler pour nous ?
10 ┊ Quels sont le/les thèmes dans lesquels vous êtes le plus à l'aise.
11 ┊ Aimez-vous travailler en équipe ?
12 ┊ Savez-vous travailler sous la pression ?
13 ┊ Comment comptez-vous compenser votre manque d’expérience ?
14 ┊ Pourquoi pensez-vous réussir dans ce poste ?'''
    },
    'supp': {
        'title': 'QUESTIONS DE SUPPORT :',
        'description': '''11 ┊ Parlez-moi de vous.
2 ┊ Que savez-vous de notre serveur ?
3 ┊ En quoi le poste à pourvoir vous intéresse-t-il ?
4 ┊ Comment envisagez-vous votre carrière au sein de MISTIA ?
5 ┊ Pourquoi êtes-vous le candidat idéal ?'''
    },
    'comm': {
        'title': 'QUESTIONS DE PUBLICITE :',
        'description': '''1 ┊ Parlez-moi de vous.
2 ┊ Que savez-vous de notre serveur ?
3 ┊ En quoi le poste à pourvoir vous intéresse-t-il ?
4 ┊ Comment envisagez-vous votre carrière au sein de MISTIA ?
5 ┊ Pourquoi êtes-vous le candidat idéal ?'''
    }
}

@bot.event
async def on_ready():
    print('----- GOOGLE FORMS FORWARDING HAS STARTED -----')
    fetch_form.start()

@bot.command()
async def graph(ctx):
    await send_questions(ctx, 'graph')

@bot.command()
async def concept(ctx):
    await send_questions(ctx, 'concept')

@bot.command()
async def supp(ctx):
    await send_questions(ctx, 'supp')

@bot.command()
async def comm(ctx):
    await send_questions(ctx, 'comm')

@tasks.loop(seconds=30)
async def fetch_form():
    try:
        with open('Data.json') as f:
            settings = json.load(f)

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        SAMPLE_SPREADSHEET_ID = '1yYztCS8Ju2a99QNNzbdmbKBUkSQl_ZAEyEaqzVDkVlg'

        SERVICE_ACCOUNT_FILE = 'keys.json'

        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)

        forms = ['🔧', '✏️', '📣', '⚔️']
        for form in forms:
            range_name = f'{form}!A1:L'
            result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_name).execute()
            values = result.get('values', [])
            if not values:
                continue

            msg = ''
            for num, x in enumerate(reversed(values)):
                if num == 5:
                    break

                if x[0] in settings[f'SENT_FORMS{form}']:
                    continue

                title = "NOUVELLE CANDIDATURE:"
                fields = [
                    {'name': 'CANDIDAT', 'value': f'• Prénom : {x[1]}\n• Pseudo : {x[3]}\n• Age : {x[2]} ans'},
                    {'name': 'TEMPS & DISPONIBILITES', 'value': f'• Temps sur Discord : {x[4]}\n• Semaine : {x[5]}\n• Week-end : {x[6]}\n• Vacances : {x[7]}'},
                    {'name': 'QUESTIONS', 'value': x[8]},
                    {'name': 'COMMENTAIRE CANDIDAT', 'value': x[9]},
                    {'name': 'RAID / HACK / FISHING', 'value': x[10]}
                ]

                embed = discord.Embed(title=title, color=discord.Color.from_rgb(34, 34, 34))
                embed.set_image(url=f'https://zupimages.net/up/22/06/{form}.gif')

                for field in fields:
                    embed.add_field(name=field['name'], value=field['value'], inline=False)

                channel = await bot.fetch_channel(906969517970833429)
                await channel.send(embed=embed)

                settings[f'SENT_FORMS{form}'].append(x[0])

        with open('Data.json', 'w') as f:
            json.dump(settings, f, indent=2)

    except Exception as e:
        print(e)
        return

async def send_questions(ctx, category):
    await ctx.message.delete()
    role = discord.utils.get(ctx.guild.roles, id=roles[category])
    if role not in ctx.author.roles:
        return

    title = questions[category]['title']
    description = questions[category]['description']

    embed = discord.Embed(title=title, description=description, color=discord.Color.from_rgb(34, 34, 34))
    embed.set_image(url='https://zupimages.net/up/22/04/b758.png')

    await ctx.send(embed=embed)

bot.run('YOUR_BOT_TOKEN')

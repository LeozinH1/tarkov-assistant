import discord
import random
import requests
import os
from dotenv import load_dotenv

from discord.ext import commands
from discord import app_commands
from dateutil import parser
from datetime import datetime, timedelta

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name = "mapa", description = "Comando teste") 
async def mapa_cmd(interaction):
    maps = ['Interchange', 'Woods', 'Customs', 'Factory', 'Reserva', 'Lighthouse', 'Shoreline']
    horario = ['Dia', 'Noite']

    await interaction.response.send_message(f'Eu escolho **{random.choice(maps)}** durante o(a) **{random.choice(horario)}**!')

@tree.command(name = "goons", description = "Comando teste") 
async def goons_cmd(interaction):
    response = requests.get("https://gentle-anchorage-57300.herokuapp.com/goonDetectors/current")

    goons_location = ''
    last_reported = ''

    if response.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        goons_location = response.json()['location']
        last_reported = response.json()['lastReported']

    yourdate = parser.parse(last_reported) - timedelta(hours=3)
    dia = yourdate.strftime('%d/%m/%y')
    hora = yourdate.strftime('%H:%M:%S')

    await interaction.response.send_message(f'Os Goons foram vistos pela última vez na **{goons_location}** ás **{hora}** do dia **{dia}**.')

@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Game('Em desenvolvimento'))


client.run(os.getenv('DISCORD_TOKEN'))
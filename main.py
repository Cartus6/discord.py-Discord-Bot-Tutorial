import discord
from discord.ext import commands 

bc = commands.Bot(command_prefix='#')

@bc.event
async def on_ready():
  print('bot is ready')

@bc.event
async def on_member_join(member):
  print(f'{member} has joined a server with your bot')

@bc.event
async def on_member_remove(member):
  print(f'{member} has left a server with your bot')

bc.run('YOUR_TOKEN_HERE')

import discord
from discord.ext import commands 
import random
from random import choice

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

@bc.command(aliases=['eightball', '8ball'])
async def _8ball(ctx, *, question):
  responses = [
      "It is certain.", "It is decidedly so.", "Without a doubt.",
      "Yes - definitely.", "As I see it, yes.", "Most likely.",
      "Outlook good.", "Yes.", "Signs point to yes.",
      "Reply hazy, try again.", "Ask again later.",
      "Better not tell you now.", "Concentrate and ask again.",
      "Don't count on it.", "My reply is no.", "My sources say no.",
      "Outlook not so good.", "Very doubtful."
  ]
  await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@bc.command()
async def ping(ctx):
  await ctx.send(f'Pong! `{round(bc.latency * 1000)}ms`')
  
bc.run('YOUR_TOKEN_HERE')

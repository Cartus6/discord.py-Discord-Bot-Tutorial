import discord
from discord.ext import commands

class Fun(commands.Cog):
  def __init__(self,bc):
    self.bc = bc

  @commands.command(aliases=['eightball', '8ball'])
  async def _8ball(self,ctx, *, question):
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

  @commands.command()
  async def ping(self,ctx):
    await ctx.send(f'Pong! `{round(self.bc.latency * 1000)}ms`')

def setup(bc):
  bc.add_cog(Fun(bc))

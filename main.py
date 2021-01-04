import discord
from discord.ext import commands 
import random
from random import choice
import asyncio

bc = commands.Bot(command_prefix='#')

async def chpr():
    await bc.wait_until_ready()

    stats = [
        f"with Beer", f"with Fire", f"in {len(bc.guilds)} servers"
    ]

    while not bc.is_closed():

        status = random.choice(stats)

        await bc.change_presence(activity=discord.Game(name=status))

        await asyncio.sleep(10)


bc.loop.create_task(chpr())

@bc.event()
async def on_ready():
  print('bot is ready')

@bc.event()
async def on_member_join(member):
  print(f'{member} has joined a server with your bot')

@bc.event()
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
  await ctx.send(f'Pong! `{round(self.bc.latency * 1000)}ms`')
  
@bc.command(pass_context=True)
@commands.has_permissions(manage_guild=True)
async def addrole(ctx, member:discord.Member, *, role:discord.Role = None):
  await ctx.message.delete()
  await member.add_roles(role)
  await ctx.send(f'{member} Was Given {role}')

@bc.command(pass_context=True)
@commands.has_permissions(manage_guild=True)
async def takerole(ctx, member:discord.Member, *, role:discord.Role = None):
  await ctx.message.delete()
  await member.remove_roles(role)
  await ctx.send(f'{role} was taken from {member}')
  
@bc.command()
@commands.has_permissions(manage_guild=True)
async def kick(ctx, member: discord.Member, *, Reason="No reason specified"):
  user = member
  await ctx.message.delete()
  await ctx.send(f'successfully kicked {user}')
  await user.send(f"you were kicked from `{ctx.guild.name}` for the following reason:\n\n**{reason}**")
  await member.kick(reason=reason)

@bc.command()
@commands.has_permissions(manage_guild=True)
async def kick(ctx, member: discord.Member, *, Reason="No reason specified"):
  user = member
  await ctx.message.delete()
  await ctx.send(f'successfully banned {user}')
  await user.send(f"you were banned from `{ctx.guild.name}` for the following reason:\n\n**{reason}**")
  await member.ban(reason=reason) 

@bc.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, member):
  member = await self.bc.fetch_user(int(member))
  await ctx.guild.unban(member)
  await ctx.send(f"unbanned {member.name}")

@bc.command()
@commands.has_permissions(manage_guild=True)
async def kick(ctx, member: discord.Member, *, Reason="No reason specified"):
  user = member
  await ctx.message.delete()
  await ctx.send(f'successfully kicked {user}')
  await user.send(f"you were kicked from `{ctx.guild.name}` for the following reason:\n\n**{reason}**")
  await member.kick(reason=reason)

@bc.command()
@commands.has_permissions(manage_guild=True)
async def kick(ctx, member: discord.Member, *, Reason="No reason specified"):
  user = member
  await ctx.message.delete()
  await ctx.send(f'successfully banned {user}')
  await user.send(f"you were banned from `{ctx.guild.name}` for the following reason:\n\n**{reason}**")
  await member.ban(reason=reason) 

@bc.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, member):
  member = await bc.fetch_user(int(member))
  await ctx.guild.unban(member)
  await ctx.send(f"unbanned {member.name}")
  

  
bc.run('YOUR_TOKEN_HERE')

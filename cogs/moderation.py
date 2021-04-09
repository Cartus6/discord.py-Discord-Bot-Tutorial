import discord
from discord.ext import commands

class Moderation(commands.Cog):
   def __init__(self,bc):
    self.bc = bc
    
  @commands.command()
  @commands.has_permissions(manage_guild=True)
  async def addrole(self, ctx, member:discord.Member, *, role:discord.Role = None):
    await ctx.message.delete()
    await member.add_roles(role)
    await ctx.send(f'{member} Was Given {role}')

  @commands.command()
  @commands.has_permissions(manage_guild=True)
  async def takerole(self, ctx, member:discord.Member, *, role:discord.Role = None):
    await ctx.message.delete()
    await member.remove_roles(role)
    await ctx.send(f'{role} was taken from {member}')


  @commands.command()
  @commands.has_permissions(manage_guild=True)
  async def kick(self, ctx, member: discord.Member, *, Reason="No reason specified"):
    user = member
    await ctx.message.delete()
    await ctx.send(f'successfully banned {user}')
    await user.send(f"you were kicked from `{ctx.guild.name}` for the following reason:\n\n**{reason}**")
    await member.kick(reason=reason) 

  @commands.command()
  @commands.has_permissions(manage_guild=True)
  async def ban(self, ctx, member: discord.Member, *, Reason="No reason specified"):
    user = member
    await ctx.message.delete()
    await ctx.send(f'successfully banned {user}')
    await user.send(f"you were banned from `{ctx.guild.name}` for the following reason:\n\n**{reason}**")
    await member.ban(reason=reason) 

  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx, member):
    member = await self.bc.fetch_user(int(member))
    await ctx.guild.unban(member)
    await ctx.send(f"unbanned {member.name}")

  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def purge(self, ctx,amount=5):
    await ctx.channel.purge(limit=1 + amount)

def setup(bc):
   bc.add_cog(Moderation(bc))

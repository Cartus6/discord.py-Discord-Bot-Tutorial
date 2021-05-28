import discord
from discord.ext import commands

class Config(commands.Cog):
    def __init__(self, bc):
        self.bc = bc

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix=None):
        if prefix is None:
            return await ctx.send("Put in a prefix for me to change to!")

        data = await self.bc.prefixes.find(ctx.guild.id)
        if data is None or "prefix" not in data:
            data = {"_id": ctx.guild.id, "prefix": prefix}
        data["prefix"] = prefix
        await self.bc.prefixes.upsert(data)
        await ctx.send("I have changed the server's prefix to {}".format(prefix))

    @commands.command(aliases=["dp"])
    @commands.has_permissions(manage_guild=True)
    async def deleteprefix(self,ctx):
        await self.bc.prefixes.unset({"_id": ctx.guild.id, "prefix": 1})
        await ctx.send("The server's prefix has been set to default")

def setup(bc):
    bc.add_cog(Config(bc))

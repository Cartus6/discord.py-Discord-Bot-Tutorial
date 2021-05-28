import discord
from discord.ext import commands, tasks
import datetime
import json
import re
from copy import deepcopy
from dateutil.relativedelta import relativedelta
import asyncio

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d||))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400, "": 1}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] + float(key)
            except KeyError:
                raise commands.BadArgument(
                    f"{value} is an invalid time key! use (d|h|m|s) for converting time"
                )
            except ValueError:
                raise commands.BadArgument(
                    f"{key} is not a number"
                )
        return round(time)

class Moderation(commands.Cog):
    def __init__(self, bc):
        self.bc = bc
        self.mute_task = self.check_current_mutes.start()

    def cog_unload(self):
        self.mute_task.cancel()

    @tasks.loop(seconds=15)
    async def check_current_mutes(self):
        currentTime = datetime.datetime.now()
        mutes = deepcopy(self.bc.mute_data)
        for key, value in mutes.items():
            if value["muteDuration"] is None:
                continue

            unmuteTime = value["mutedAt"] + relativedelta(seconds=value["muteDuration"])
            if currentTime >= unmuteTime:
                guild = self.bc.get_guild(value["guildID"])
                member = guild.get_member(value["_id"])

                role = discord.utils.get(guild.roles, id=835490758072991744)
                if role in member.roles:
                    await member.remove_roles(role)

                await self.bc.mutes.delete(member.id)
                try:
                    self.bc.mute_data.pop(member.id)
                except KeyError:
                    pass

    @check_current_mutes.before_loop
    async def before_check_current_mutes(self):
        await self.bc.wait_until_ready()

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, time: TimeConverter=None):
        muterole = discord.utils.get(ctx.guild.roles, id=835490758072991744)
        pos1 = ctx.guild.roles.index(ctx.author.top_role)
        pos2 = ctx.guild.roles.index(member.top_role)
        if pos1 == pos2:
            return await ctx.send("Both of you have the same power so i can not mute this user for you!")
        if pos1 < pos2:
            return await ctx.send("This person has more power than you so i can not mute him for you!")

        try:
            if self.bc.mute_data[member.id]:
                return await ctx.send("This user is already muted!")
        except KeyError:
            pass

        data = {
            "_id": member.id,
            "mutedAt": datetime.datetime.now(),
            "muteDuration": time or None,
            "mutedBy": ctx.author.id,
            "guildID": ctx.guild.id
        }
        await self.bc.mutes.upsert(data)
        self.bc.mute_data[member.id] = data

        await member.add_roles(muterole)

        if not time:
            return await ctx.send("I have muted this person infinitely")
        else:
            minutes, seconds = divmod(time, 60)
            hours, minutes = divmod(minutes, 60)
            if int(hours):
                await ctx.send("Muted {} for {} hours, {} minutes, and {} seconds".format(member.display_name,hours,minutes,seconds))
            elif int(minutes):
                await ctx.send("Muted {} for {} minutes, and {} seconds".format(member.display_name,minutes,seconds))
            elif int(seconds):
                await ctx.send("Muted {} for {} seconds".format(member.display_name,seconds))

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member:discord.Member):
        muterole = discord.utils.get(ctx.guild.roles, id=835490758072991744)

        await self.bc.mutes.delete(member.id)
        try:
            self.bc.mute_data.pop(member.id)
        except KeyError:
            pass

        if muterole not in member.roles:
            return await ctx.send("This user is not muted")

        await member.remove_roles(muterole)
        await ctx.send("Unmuted this user!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount):
      await ctx.channel.purge(limit=1 + amount)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def addrole(self, ctx, member:discord.Member = None, *, role:discord.Role = None):
        if member == None:
            await ctx.send("Please specify a member")
        if role == None:
            await ctx.send("Please specify a role")
        await ctx.message.delete()
        await member.add_roles(role)
        await ctx.send(f'{member} was given "{role}"')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_guild=True)
    async def takerole(self, ctx, member:discord.Member = None, *, role:discord.Role = None):
        if member == None:
            await ctx.send("Please specify a member")
        if role == None:
            await ctx.send("Please specify a role")
        await ctx.message.delete()
        await member.remove_roles(role)
        await ctx.send(f'"{role}" was taken from {member}')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx, member: discord.Member, *, reason="No Reason Specified"):
        user = member
        await ctx.message.delete()
        await ctx.send(f'Successfully kicked {user}')
        await user.send(f'You were kicked from `{ctx.guild.name}` for the following reason:\n\n**{reason}**')
        await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, member: discord.Member, *, reason="No Reason Specified"):
        user = member
        await ctx.message.delete()
        await ctx.send(f'Successfully bannes {user}')
        await user.send(f'You were banned from `{ctx.guild.name}` for the following reason:\n\n**{reason}**')
        await member.ban(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx, member):
        member = await self.bc.fetch_user(int(member))
        await ctx.guild.unban(member, reason=None)
        await ctx.send(f"Successfully unbanned {member.name}")

def setup(bc):
    bc.add_cog(Moderation(bc))

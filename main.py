import discord
from discord.ext import commands
import random
from random import choice
import os
import asyncio
import json
import discordmongo
import motor.motor_asyncio

async def get_prefix(bc, message):
    if not message.guild:
        return commands.when_mentioned_or(bc.DEFAULT_PREFIX)(bc,message)

    try:
        data = await bc.prefixes.find(message.guild.id)

        if not data or "prefix" not in data:
            return commands.when_mentioned_or(bc.DEFAULT_PREFIX)(bc, message)
        return commands.when_mentioned_or(data["prefix"])(bc, message)
    except:
        return commands.when_mentioned_or(bc.DEFAULT_PREFIX)(bc, message)

bc = commands.Bot(command_prefix = get_prefix, owner_id=485513915548041239, intents=discord.Intents.all())
bc.remove_command("help")
bc.DEFAULT_PREFIX = "#"
bc.blacklisted = {}
bc.mute_data = {}

async def chpr():
    await bc.wait_until_ready()

    stats = [
        "With Beer", "With Fire", f"in {len(bc.guilds)} servers"
    ]

    while not bc.is_closed():

        status = random.choice(stats)

        await bc.change_presence(activity=discord.Game(name=status))

        await asyncio.sleep(10)

bc.loop.create_task(chpr())

@bc.event
async def on_ready():
    data = read_json("blacklist")
    bc.blacklisted = data["blacklistedUsers"]
    current_mutes = await bc.mutes.get_all()

    for mute in current_mutes:
        bc.mute_data[mute["_id"]] = mute
    print('bot online')

@bc.event
async def on_member_join(member):
    print(f'{member} joined a server with your bot!')

@bc.event
async def on_member_remove(member):
    print(f'{member} left a server with your bot :(')

@bc.event
async def on_message(msg):
    data = read_json("blacklist")
    bc.blacklisted = data["blacklistedUsers"]
    if not msg.author.bot:
        if not msg.guild:
            channel = bc.get_channel(744176742540771371)
            await channel.send(f"User **{msg.author}** sent a report saying `{msg.content}`")
        await bc.process_commands(msg)

@bc.command()
@commands.is_owner()
async def blacklist(ctx,user:discord.Member):
    data = read_json("blacklist")
    data["blacklistedUsers"].append(user.id)
    write_json(data,"blacklist")
    await ctx.send("I have blacklisted {} for you!".format(user))

@bc.command()
@commands.is_owner()
async def unblacklist(ctx,user:discord.Member):
    data = read_json("blacklist")
    data["blacklistedUsers"].remove(user.id)
    write_json(data,"blacklist")
    await ctx.send("I have unblacklisted {} for you!".format(user))


def read_json(filename):
    with open(f"{filename}.json", "r") as f:
        data = json.load(f)
    return data

def write_json(data, filename):
    with open(f"{filename}.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    bc.mongo = motor.motor_asyncio.AsyncIOMotorClient("MONGO-URL")
    bc.db = bc.mongo["example"]
    bc.prefixes = discordmongo.Mongo(connection_url=bc.db, dbname="prefixes")
    bc.mutes = discordmongo.Mongo(connection_url=bc.db, dbname="mutes")
    for filename in os.listdir("cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            bc.load_extension(f"cogs.{filename[:-3]}")

bc.run("TOKEN")

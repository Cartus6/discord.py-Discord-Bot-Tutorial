import discord
from discord.ext import commands 
import random
from random import choice
import asyncio
import json
import os

bc = commands.Bot(command_prefix='#')
bc.blacklisted_users = {}


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

@bc.event
async def on_ready():
  data = read_json("blacklist")
  bc.blacklisted_users = data["blacklistedUsers"]
  print('bot is ready')

@bc.event
async def on_member_join(member):

   print(f'{member} has joined a server with your bot')

@bc.event
async def on_member_remove(member):
  print(f'{member} has left a server with your bot')

@bc.event
async def on_message(msg):
    if not msg.author.bot:
        if msg.author.id in bc.blacklisted_users and msg.content.lower().startswith("PREFIX"): # Replace prefix with your prefix
            return await msg.channel.send("It appears you are blacklisted!")
        
        if not msg.guild:
            channel = bc.get_channel(CHANNEL) # Replace CHANNEL with your modmail channel id
            await channel.send(f"User **{msg.author}** sent a report saying `{msg.content}`")
        await bc.process_commands(msg)
           
@bc.command()
async def blacklist(ctx, user:discord.Member):
    data = read_json("blacklist")
    data["blacklistedUsers"].append(user.id)
    write_json(data, "blacklist")
    
@bc.command()
async def unblacklist(ctx, user:discord.Member):
    data = read_json("blacklist")
    data["blacklistedUsers"].remove(user.id)
    write_json(data, "blacklist")
  
def read_json(filename):
    with open(f"{filename}.json", "r") as f:
        data = json.load(f)
    return data

def write_json(data, filename):
    with open(f"{filename}.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            bc.load_extension(f"cogs.{filename[:-3]}")
bc.run('YOUR_TOKEN_HERE')

import discord
from discord.ext import commands
from utils.util import Pag

class Help(commands.Cog):
    def __init__(self,bc):
        self.bc = bc
        self.cmds_per_page = 5

    def get_command_signature(self, command:commands.Command, ctx:commands.Context):
        aliases = "|".join(command.aliases)
        cmd_invoke = f"[{command.name}|{aliases}]" if command.aliases else command.name

        full_invoke = command.qualified_name.replace(command.name, "")

        signature = f"{ctx.prefix}{full_invoke}{cmd_invoke} {command.signature}"
        return signature

    async def return_filtered_commands(self,walkable,ctx):
        filtered = []

        for c in walkable.walk_commands():
            try:
                if c.hidden:
                    continue

                elif c.parent:
                    continue

                await c.can_run(ctx)
                filtered.append(c)
            except commands.CommandError:
                continue

        return self.return_sorted_commands(filtered)

    def return_sorted_commands(self,commandList):
        return sorted(commandList, key=lambda x: x.name)

    async def setup_help_page(self,ctx,entity=None,title=None):
        entity = entity or self.bc
        title = title or self.bc.description

        pages = []

        if isinstance(entity, commands.Command):
            filtered_commands = (
                list(set(entity.all_commands.values()))
                if hasattr(entity, "all_commands")
                else []
            )
            filtered_commands.insert(0, entity)

        else:
            filtered_commands = await self.return_filtered_commands(entity,ctx)

        for i in range(0, len(filtered_commands), self.cmds_per_page):
            next_commands = filtered_commands[i: i + self.cmds_per_page]
            commands_entry = ""

            for cmd in next_commands:
                desc = cmd.short_doc or cmd.description
                signature = self.get_command_signature(cmd,ctx)
                subcommand = "Has subcommands" if hasattr(cmd, "all_commands") else ""

                commands_entry += (
                    f"**__{cmd.name}__**\n```\n{signature}\n```\n{desc}\n"
                    if isinstance(entity, commands.Command)
                    else f"**__{cmd.name}__**\n{desc}\n     {subcommand}"
                )
            pages.append(commands_entry)

        await Pag(title=title, color=0xff000, entries=pages, length=1).start(ctx)

    @commands.command(name="help",description="The help command")
    async def help_command(self,ctx,*,entity=None):
        if not entity:
            await self.setup_help_page(ctx)

        else:
            cog = self.bc.get_cog(entity)
            if cog:
                await self.setup_help_page(ctx,cog,f"{cog.qualified_name}'s commands")

            else:
                command = self.bc.get_command(entity)
                if command:
                    await self.setup_help_page(ctx,command,command.name)

                else:
                    return await ctx.send("Entity not found.")

def setup(bc):
    bc.add_cog(Help(bc))
